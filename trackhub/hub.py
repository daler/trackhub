import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from validate import ValidationError
from base import HubComponent


class Hub(HubComponent):
    # map proper track hub stanza field names to pythonic attribute names in
    # this class.
    _field_order = OrderedDict([
        ('hub', 'hub'),
        ('shortLabel', 'short_label'),
        ('longLabel', 'long_label'),
        ('genomesFile', 'genomes_filename'),
        ('email', 'email'),
    ]
    )

    def __init__(self, hub, short_label="", long_label=None,
                 genomes_file=None, genomes_filename=None, email="",
                 url=None):
        """
        Represents a top-level track hub container.
        """
        HubComponent.__init__(self)
        self.url = url
        self._local_fn = None
        self._remote_fn = None
        self._local_dir = None
        self._remote_dir = None
        self.hub = hub
        self.short_label = short_label
        if not long_label:
            long_label = short_label
        self.long_label = long_label
        self.email = email

        self.genomes_file = None
        if genomes_file is not None:
            self.add_genomes_file(genomes_file)

    @property
    def local_fn(self):
        if self._local_fn is not None:
            return self._local_fn
        return os.path.join(self.local_dir, self.hub + '.hub.txt')

    @local_fn.setter
    def local_fn(self, fn):
        self._local_fn = fn

    @property
    def local_dir(self):
        if self._local_dir is not None:
            return self._local_dir
        return ""

    @local_dir.setter
    def local_dir(self, fn):
        self._local_dir = fn

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn
        return os.path.join(self.remote_dir, self.hub + '.hub.txt')

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    @property
    def remote_dir(self):
        if self._remote_dir is not None:
            return self._remote_dir
        return ""

    @remote_dir.setter
    def remote_dir(self, fn):
        self._remote_dir = fn

    def validate(self):
        if self.genomes_file is None:
            raise ValidationError(
                'No GenomesFile attached to Hub (use add_genomes_file())')
        self.genomes_file.validate()
        return True

    def add_genomes_file(self, genomes_file):
        """
        If a GenomesFile object was not provided upon instantiating this
        object, attach one now
        """
        self.genomes_file = self.add_child(genomes_file)

    def __str__(self):
        s = []
        for field, attr in self._field_order.items():
            if field == 'genomesFile':
                if self.genomes_file:
                    value = os.path.relpath(
                        self.genomes_file.local_fn,
                        start=os.path.dirname(self.local_fn))
                else:
                    value = None
            else:
                value = getattr(self, attr)
            s.append('%s %s' % (field, value))
        return '\n'.join(s)

    def _render(self):
        """
        Render just this object, and not all the underlying GenomeFiles and
        their TrackDb.
        """
        fout = open(self.local_fn, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name
