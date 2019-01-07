from __future__ import absolute_import

import os
import warnings
from .validate import ValidationError
from .base import HubComponent


class Hub(HubComponent):
    # map proper track hub stanza field names to pythonic attribute names in
    # this class.

    def __init__(self, hub, short_label=None, long_label=None,
                 genomes_file=None, genomes_filename=None, email="",
                 url=None, filename=None):
        """
        Represents a top-level track hub container.

        hub : str
            Top-level name of the hub.

        short_label : str
            Short label for the hub, alias for UCSC parameter shortLabel.

        long_label : str
            Long label for the hub, alias for UCSC parameter longLabel. If
            None, will copy `short_label`.

        genomes_file : GenomesFile
            If you already have a GenomesFile created, you can add it here;
            otherwise when one is created you'll have to add one later with the
            `add_genomes_file` method.

        email : str
            Email that will be provided in the hub for contact info

        url : str
            Deprecated.

        filename : str
            If None, defaults to the value of `hub` plus ".hub.txt". When
            uploaded, the filename is relative to the uploaded location.
        """
        HubComponent.__init__(self)
        if url is not None:
            self.url = url
            warnings.DeprecationWarning(
                'url is no longer used for Hub objects')
        self.hub = hub
        if not short_label:
            short_label = hub
        self.short_label = short_label
        if not long_label:
            long_label = short_label
        self.long_label = long_label
        self.email = email

        self.genomes_file = None
        if genomes_file is not None:
            self.add_genomes_file(genomes_file)

        if filename is None:
            filename = hub + '.hub.txt'
        self.filename = filename

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
        genomes_file = None
        if self.genomes_file:
            genomes_file = self.genomes_file.filename
        for label, value in [
            ('hub', 'hub'),
            ('shortLabel', self.short_label),
            ('longLabel', self.long_label),
            ('genomesFile', genomes_file),
            ('email', self.email),
        ]:
            s.append('{0} {1}'.format(label, value))
        return '\n'.join(s)

    def _render(self, staging='staging'):
        """
        Render just this object, and not all the underlying GenomeFiles and
        their TrackDb.
        """
        rendered_filename = os.path.join(staging, self.filename)
        self.makedirs(rendered_filename)
        fout = open(rendered_filename, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name
