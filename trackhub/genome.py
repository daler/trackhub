from __future__ import absolute_import

import os
from .validate import ValidationError
from .base import HubComponent


class Genome(HubComponent):
    def __init__(self, genome, trackdb=None, genome_file_obj=None):
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
