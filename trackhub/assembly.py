import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from validate import ValidationError
from base import HubComponent
from genome import Genome
from genomes_file import GenomesFile
from trackdb import TrackDb
from constants import assembly_fields


class GroupDefinition(object):
    def __init__(self, name, label, priority=1, default_is_closed=0):
        """
        Represents a group of tracks in a trackhub.

        Instances of this class are provided to an assembly.

        :param name:
            String; name for the group (e.g., "celltype").

        :param label:
            String; the label that will be displayed (e.g., "Cell_Type")

        :param priority:
            Orders this track group with the other track groups

        :param default_is_closed:
            Determines if this track group is expanded or closed by default. Values to use are 0 or 1
        """
        self.name = str(name)
        self.label = str(label)
        self.priority = int(priority)
        if default_is_closed in (0, 1):
            self.default_is_closed = default_is_closed
        else:
            raise ValueError("default_is_closed must be 1 or 0")

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <GroupDefinition> object"
        s = [
                'name %s' % self.name,
                'label %s' % self.label,
                'priority %s' % self.priority,
                'defaultIsClosed %s' % self.default_is_closed
        ]
        s.extend('%s %s' % (k, v) for k, v in self.mapping.items())
        return '\n'.join(s) + '\n'

class GroupsFile(HubComponent):
    def __init__(self, groups=None):
        Hubcomponent.__init__(self)
        if groups is not None:
            self.add_groups(groups)

    def add_groups(self, groups):
        """
        Add a list of GroupDefinition objects to this composite.

        :param groups:
            List of GroupDefinition objects.
        """
        if groups is None:
            groups = {}
        _groups = {}
        for g in groups:
            assert isinstance(sg, GroupDefinition)
            _groups[g.name] = g
        self.groups = _groups

    def __str__(self):
        """
        Render groups.txt file.
        """
        return '\n'.join(g.__str__() for g in self.groups)

    def _render(self):
        raise NotImplementedError("GroupsFile needs a render method")

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn

        if self.genome is None:
            return None

        if self.genome.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genome.genomes_file.remote_fn),
                                self.genome.genome, "groups.txt")

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    def validate(self):
        for g in self.groups:
            g.validate()
        return True

class Assembly(Genome):

    # Dictionary where keys are parameter names (e.g., "color") and values are
    # Parameter objects.  These are defined in the constants module.

    params = OrderedDict()
    params.update(assembly_fields)

    def __init__(self, genome, twobit_local_fn=None, groups=None, trackdb=None, genome_file_obj=None, **kwargs):
        """
        Represents a genome stanza within a "genomes.txt" file for a non-UCSC genome.

        The file itself is represented by a :class:`GenomesFile` object.
        """
        HubComponent.__init__(self)
        Genome.__init__(self, genome, trackdb=trackdb, genome_file_obj=genome_file_obj)
        if genome_obj is not None:
            self.genome = genome
        if twobit_local_fn is not None:
            self.local_fn = local_fn
        # Use HTMLDoc container ?
        if html_description is not None:
            self.html_description = html_description
        self.add_groups(groups)

        self.kwargs = kwargs
        self._orig_kwargs = kwargs.copy()
        self.add_params(self, **kwargs)

    def add_trackdb(self, trackdb):
        self.children = filter(self.children, not isinstance(TrackDb))
        self.add_child(trackdb)
        self.trackdb = trackdb

    def add_html_doc(self, hmtl_doc):
        self.children = filter(self.children, not isinstance(HTMLDoc))
        self.add_child(html_doc)
        self.html_doc = html_doc

    def add_groups_file(self, groups_file):
        self.children = filter(self.children, not isinstance(GroupsFile))
        self.add_child(groups_file)
        self.groups_file = groups_file

    def add_params(self, **kw):
        """
        Add [possibly many] parameters to the Assembly.

        Parameters will be checked against known UCSC parameters and their
        supported formats.
        """
        for k, v in kw.items():
            if (k not in self.params) and (k not in self.specific_params):
                raise ParameterError('"%s" is not a valid parameter for %s'
                                     % (k, self.__class__.__name__))
            try:
                self.params[k].validate(v)
            except KeyError:
                self.specific_params[k].validate(v)

        self._orig_kwargs.update(kw)
        self.kwargs = self._orig_kwargs.copy()

    def remove_params(self, *args):
        """
        Remove [possibly many] parameters from the track.

        E.g.,

        remove_params('color', 'visibility')
        """
        for a in args:
            self._orig_kwargs.pop(a)
        self.kwargs = self._orig_kwargs.copy()

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <Assembly> object"

        s = []

        s.append('genome %s' % self.genome)
        s.append('trackDb %s' % self.trackdb.remote_fn)
        s.append('twoBitPath %s' % self.remote_fn)
        if getattr(self, groups_file, None):
            s.append('groups %s' % self.groups_file.remote_fn)

        for name, parameter_obj in self.params.items():
            value = self.kwargs.pop(name, None)
            if value is not None:
                if parameter_obj.validate(value):
                    s.append("%s %s" % (name, value))

        if getattr(self, html_doc, None):
            s.append('htmlDocumentation %s' % self.html_doc.remote_fn)

        return '\n'.join(s) + '\n'

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn

        if self.genome is None:
            return None

        if self.genome.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genome.genomes_file.remote_fn),
                                self.genome.genome,
                                '%s.2bit' % self.genome.genome)

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    def validate(self):
        Genome.validate(self)
        # check for necessary params?

class AssemblyHTMLDoc(HTMLDoc):
    # overload track-specific methods in HTMLDoc
    @property
    def local_fn(self):
        if (self.genomes_file is None) or (self.genome is None):
            return None
        return os.path.join(
            os.path.dirname(self.genomes_file.local_fn),
            self.genome.genome,
            '%s_info.html' % self.genome.genome)

    @property
    def remote_fn(self):
        if (self.trackdb is None) or (self.track is None):
            return None
        return os.path.join(
            os.path.dirname(self.genomes_file.remote_fn),
            self.genome.genome,
            '%s_info.html' % self.genome.genome)

    @property
    def genomes_file(self):
        obj, level = self.root(cls=GenomesFile)
        return obj

    @property
    def assembly(self):
        obj, level = self.root(cls=Assembly)
        return obj

    def validate(self):
        if not self.genomes_file:
            raise ValueError("HTMLDoc object must be connected to a "
                             "BaseTrack subclass instance and a TrackDb "
                             "instance")
        return True

