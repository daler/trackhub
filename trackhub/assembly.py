from __future__ import absolute_import

import os
from collections import OrderedDict
from .validate import ValidationError
from .base import HubComponent
from .genome import Genome
from .genomes_file import GenomesFile
from .groups import GroupsFile
from .trackdb import TrackDb
from .constants import assembly_fields
from .track import HTMLDoc


class Assembly(Genome):

    # Dictionary where keys are parameter names (e.g., "color") and values are
    # Parameter objects.  These are defined in the constants module.

    params = OrderedDict()
    params.update(assembly_fields)

    def __init__(self,
                 genome,
                 twobit_file=None,
                 remote_fn=None,
                 groups=None,
                 trackdb=None,
                 genome_file_obj=None,
                 html_string=None,
                 **kwargs):
        """
        Represents a genome stanza within a "genomes.txt" file for a non-UCSC genome.

        The file itself is represented by a :class:`GenomesFile` object.
        """
        HubComponent.__init__(self)
        Genome.__init__(self, genome, trackdb=trackdb, genome_file_obj=genome_file_obj)
        self.local_fn = twobit_file
        self.remote_fn = remote_fn
        self.html_string = html_string

        if groups is not None:
            self.add_groups(groups)
        else:
            self.groups = None

        self._orig_kwargs = kwargs
        self.add_params(**kwargs)

    def add_trackdb(self, trackdb):
        self.children = [x for x in self.children if not isinstance(x, TrackDb)]
        self.add_child(trackdb)
        self.trackdb = trackdb

    def add_groups(self, groups):
        self.children = [x for x in self.children if not isinstance(x, GroupsFile)]
        self.add_child(groups)
        self.groups = groups

    def add_params(self, **kw):
        """
        Add [possibly many] parameters to the Assembly.

        Parameters will be checked against known UCSC parameters and their
        supported formats.
        """
        for k, v in kw.items():
            if k not in self.params:
                raise ValidationError(
                    '"%s" is not a valid parameter for %s'
                    % (k, self.__class__.__name__))
            self.params[k].validate(v)

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
        _html = AssemblyHTMLDoc(self.html_string)
        _html.add_parent(self)
        return _html

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <Assembly> object"

        s = []

        s.append('genome %s' % self.genome)
        s.append('trackDb %s' % self.trackdb.remote_fn)
        s.append('twoBitPath %s' % self.remote_fn)
        if self.groups is not None:
            s.append('groups %s' % self.groups.remote_fn)

        for name, parameter_obj in self.params.items():
            value = self.kwargs.pop(name, None)
            if value is not None:
                if parameter_obj.validate(value):
                    s.append("%s %s" % (name, value))

        if self._html is not None:
            s.append('htmlDocumentation %s' % self._html.remote_fn)

        self.kwargs = self._orig_kwargs.copy()
        return '\n'.join(s) + '\n'

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn

        if self.parent is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.parent.remote_fn),
                                self.genome,
                                '%s.2bit' % self.genome)

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
        if (self.genomes_file is None) or (self.genome is None):
            return None
        return os.path.join(
            os.path.dirname(self.genomes_file.remote_fn),
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
