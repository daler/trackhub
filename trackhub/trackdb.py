from __future__ import absolute_import

import os
from .base import HubComponent
from .genomes_file import GenomesFile
from .hub import Hub
from .genome import Genome


class TrackDb(HubComponent):
    def __init__(self, tracks=None, filename=None):
        """
        Represents the file containing one or more Track objects (which each
        represent a stanza).

        tracks : list
            If provided, these tracks will be added

        filename : str
            Path to trackdb, relative to top-level hub. If None, default is to
            use "<genome>/trackDb.txt"
        """
        HubComponent.__init__(self)

        if tracks is None:
            tracks = []

        self._tracks = []
        for track in tracks:
            self.add_track(track)

        self._filename = filename

    @property
    def hub(self):
        return self.root(cls=Hub)

    @property
    def genomes_file(self):
        genomes_file, level = self.root(GenomesFile)
        if level is None:
            return None
        if level != -2:
            raise ValueError("GenomesFile is level %s, not -2" % level)
        return genomes_file

    @property
    def genome(self):
        genome, level = self.root(Genome)
        if level is None:
            return None
        if level != -1:
            raise ValueError('Genome is level %s, not -1' % level)
        return genome

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename

        if self.genome is None:
            return None

        if self.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genomes_file.filename),
                                self.genome.genome, 'trackDb.txt')

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    def add_tracks(self, track):
        """
        Add a track or iterable of tracks.

        Parameters
        ----------

        track : iterable or Track
            Iterable of :class:`Track` objects, or a single :class:`Track`
            object.
        """
        from trackhub import BaseTrack
        if isinstance(track, BaseTrack):
            self.add_child(track)
            self._tracks.append(track)
        else:
            for t in track:
                self.add_child(t)
                self._tracks.append(t)

    @property
    def tracks(self):
        from trackhub import Track
        return [i for i, level in self.leaves(Track)]

    def add_genome(self, genome):
        self.add_parent(genome)

    def __str__(self):
        s = []
        for track in self._tracks:
            s.append(str(track) + '\n')
        return '\n'.join(s)

    def validate(self):
        if len(self.children) == 0:
            raise ValueError("No Track objects specified")

    def _render(self, staging='staging'):
        rendered_filename = os.path.join(staging, self.filename)
        self.makedirs(rendered_filename)
        fout = open(rendered_filename, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name
