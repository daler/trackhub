from __future__ import absolute_import

import os
from .validate import ValidationError
from .base import HubComponent
from . import constants


class Genome(HubComponent):
    def __init__(self, genome, trackdb=None, genome_file_obj=None, **kwargs):
        """
        Represents a 2-line genome stanza within a "genomes.txt" file.

        The file itself is represented by a :class:`GenomesFile` object.

        Parameters
        ----------
        genome : str
            One of the UCSC-supported assembly names (e.g., "hg38")

        trackdb : TrackDb object
            If not None, this object will be attached as the child track db

        genome_file : GenomesFile object
            If not None, this object will be attached as the parent GenomesFile
        """
        HubComponent.__init__(self)
        self.genome = genome
        self.trackdb = None
        if trackdb is not None:
            self.add_trackdb(trackdb)
        if genome_file_obj:
            self.add_parent(genome_file_obj)

        self._orig_kwargs = kwargs

        self.track_field_order = []
        self.track_field_order.extend(constants.track_fields['genome'])

        self.add_params(**kwargs)

    @property
    def genome_file_obj(self):
        try:
            return self.parent
        except AttributeError:
            return None

    def add_trackdb(self, trackdb):
        self.children = []
        self.add_child(trackdb)
        self.trackdb = self.children[0]

    def add_params(self, **kw):
        """
        Add [possibly many] parameters to the Genome.

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
        Remove [possibly many] parameters from the Genome.

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
            return "Unconfigured <Genome> object"
        s = []
        s.append('genome %s' % self.genome)
        s.append(
            'trackDb %s'
            % os.path.relpath(
                self.trackdb.filename,
                os.path.dirname(self.genome_file_obj.filename)
            )
        )

        for name in self.track_field_order:
            value = self.kwargs.pop(name, None)
            if value is not None:
                if constants.param_dict[name].validate(value):
                    s.append("%s %s" % (name, value))

        self.kwargs = self._orig_kwargs.copy()

        return '\n'.join(s) + '\n'

    def validate(self):
        if len(self.children) == 0:
            raise ValidationError(
                "No TrackDb objects provided")
        if self.trackdb is None:
            raise ValidationError("No TrackDb objects provided")

    def _render(self, staging='staging'):
        """
        No file is created from a Genome object -- only from its parent
        GenomesFile object.
        """
        pass
