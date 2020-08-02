from __future__ import absolute_import

import os
from collections import OrderedDict
from .validate import ValidationError
from .base import HubComponent, deprecation_handler
from .genome import Genome
from .genomes_file import GenomesFile
from .groups import GroupsFile
from .trackdb import TrackDb
from . import constants
from .track import HTMLDoc


class TwoBitFile(HubComponent):
    def __init__(self, source, filename=None, assembly_obj=None, **kwargs):
        source, filename = deprecation_handler(source, filename, kwargs)
        HubComponent.__init__(self)
        self.source = source
        self._filename = filename
        self.assembly_obj = assembly_obj

    @property
    def assembly(self):
        obj, level = self.root(cls=Assembly)
        if level is None:
            return None
        if level != -1:
            raise ValueError("Assembly is level %s, not -1" % level)
        return obj

    @property
    def source(self):
        if self._source is not None:
            return self._source
        return None

    @source.setter
    def source(self, fn):
        self._source = fn

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename

        # If filename hasn't been assigned then make one automatically based
        # on the assembly's parent genomes_file and the assembly's genome.
        if not self.assembly:
            return None
        if not self.assembly.genomes_file:
            return None
        return os.path.join(
            os.path.dirname(self.assembly.genomes_file.filename),
            self.assembly.genome,
            self.assembly.genome + '.2bit')

    def validate(self):
        if not os.path.exists(self.source):
            raise ValueError("Local filename {0} does not exist".format(self.source))

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    def _render(self, staging='staging'):
        pass


class Assembly(Genome):
    def __init__(self,
                 genome,
                 twobit_file=None,
                 groups=None,
                 trackdb=None,
                 genome_file_obj=None,
                 html_string=None,
                 html_string_format='rst',
                 **kwargs):
        """
        Represents a genome stanza within a "genomes.txt" file for a non-UCSC genome.

        The file itself is represented by a :class:`GenomesFile` object.

        Parameters
        ----------
        genome : str
            The genome assembly name to use for this assembly

        twobit_file : str
            Local path to 2bit file.
        """
        Genome.__init__(self, genome, trackdb=trackdb, genome_file_obj=genome_file_obj)

        if twobit_file is not None:
            self.add_twobit(TwoBitFile(twobit_file))

        self.html_string = html_string
        self.html_string_format = html_string_format

        if groups is not None:
            self.add_groups(groups)
        else:
            self.groups = None

        self._orig_kwargs = kwargs

        self.track_field_order = []
        self.track_field_order.extend(constants.track_fields['assembly'])

        self.add_params(**kwargs)

    def add_twobit(self, twobit):
        self.children = [x for x in self.children if not isinstance(x, TwoBitFile)]
        self.add_child(twobit)
        self.twobit = twobit

    def add_trackdb(self, trackdb):
        self.children = [x for x in self.children if not isinstance(x, TrackDb)]
        self.add_child(trackdb)
        self.trackdb = trackdb

    def add_groups(self, groups):
        self.children = [x for x in self.children if not isinstance(x, GroupsFile)]
        self.add_child(groups)
        self.groups = groups

    @property
    def genomes_file(self):
        obj, level = self.root(cls=GenomesFile)
        if level is None:
            return None
        if level != -1:
            raise ValueError("GenomesFile is level %s, not -1" % level)
        return obj

    def add_params(self, **kw):
        """
        Add [possibly many] parameters to the Assembly.

        Parameters will be checked against known UCSC parameters and their
        supported formats.
        """
        for k, v in kw.items():
            if k not in self.track_field_order:
                raise ParameterError(
                    '"{0}" is not a valid parameter for {1} with '
                    'tracktype {2}'
                    .format(k, self.__class__.__name__, self.tracktype)
                )
            constants.param_dict[k].validate(v)

        self._orig_kwargs.update(kw)
        self.kwargs = self._orig_kwargs.copy()

    def remove_params(self, *args):
        """
        Remove [possibly many] parameters from the Assembly.

        E.g.,

        remove_params('color', 'visibility')
        """
        for a in args:
            self._orig_kwargs.pop(a)
        self.kwargs = self._orig_kwargs.copy()

    @property
    def _html(self):
        if not self.html_string:
            return None
        _html = AssemblyHTMLDoc(self.html_string, self.html_string_format)
        _html.add_parent(self)
        return _html

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <Assembly> object"

        s = []

        s.append('genome %s' % self.genome)
        s.append('trackDb %s' % self.trackdb.filename)
        s.append('twoBitPath %s' % self.twobit.filename)
        if self.groups is not None:
            s.append('groups %s' % self.groups.filename)

        for name in self.track_field_order:
            value = self.kwargs.pop(name, None)
            if value is not None:
                if constants.param_dict[name].validate(value):
                    s.append("%s %s" % (name, value))

        if self._html is not None:
            s.append('htmlDocumentation %s' % self._html.filename)

        self.kwargs = self._orig_kwargs.copy()
        return '\n'.join(s) + '\n'

    def validate(self):
        Genome.validate(self)
        # check for necessary params?


class AssemblyHTMLDoc(HTMLDoc):
    # overload track-specific methods in HTMLDoc
    @property
    def filename(self):
        if (self.genomes_file is None) or (self.genome is None):
            return None
        return os.path.join(
            os.path.dirname(self.genomes_file.filename),
            self.genome.genome,
            '%s_info.html' % self.genome.genome)

    @property
    def genomes_file(self):
        obj, level = self.root(cls=GenomesFile)
        if level is None:
            return None
        if level != -2:
            raise ValueError("GenomesFile is level %s, not -2" % level)
        return obj

    @property
    def genome(self):
        obj, level = self.root(cls=Assembly)
        if level is None:
            return None
        if level != -1:
            raise ValueError("Assembly is level %s, not -1" % level)
        return obj

    def validate(self):
        if not self.genome:
            raise ValueError("HTMLDoc object must be connected to an"
                             "Assembly subclass instance")
        return True
