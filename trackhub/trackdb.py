import os
from validate import ValidationError
from base import HubComponent
from genomes_file import GenomesFile
from genome import Genome
import track as _track

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

class TrackDb(HubComponent):
    def __init__(self, tracks=None):
        """
        Represents the file containing one or more Track objects (which each
        represent a stanza).
        """
        HubComponent.__init__(self)
        if tracks is None:
            tracks = []

        self._tracks = []
        for track in tracks:
            self.add_track(track)

        self._local_fn = None
        self._remote_fn = None

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
    def local_fn(self):
        if self._local_fn is not None:
            return self._local_fn

        if self.genome is None:
            return None

        if self.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genomes_file.local_fn),
                                self.genome.genome, 'trackDb.txt')

    @local_fn.setter
    def local_fn(self, fn):
        self._local_fn = fn

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn

        if self.genome is None:
            return None

        if self.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genomes_file.remote_fn),
                                self.genome.genome, 'trackDb.txt')

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    def add_tracks(self, track):
        """
        Add a track or iterable of tracks.

        :param track:
            Iterable of :class:`Track` objects, or a single :class:`Track`
            object.
        """
        if isinstance(track, _track.BaseTrack):
            self.add_child(track)
            self._tracks.append(track)
        else:
            for t in track:
                self.add_child(t)
                self._tracks.append(t)

    @property
    def tracks(self):
        return [i for i, level in self.leaves(_track.Track)]

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

    def _render(self):
        dirname = os.path.dirname(self.local_fn)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        fout = open(self.local_fn, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name
