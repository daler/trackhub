import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from validate import ValidationError
from hub import Hub
from base import HubComponent


class GenomesFile(HubComponent):
    def __init__(self, genome=None):
        """
        Represents the genomes file on disk.  Can contain multiple
        :class:`Genome` objects, each of which represent a stanza in this
        file.

        The file ultimately created (with the self.render() method) will be
        determined by the parent Hub's `genome_filename` attribute.  By
        default, this is the hub name, plus ".genomes.txt"
        """
        HubComponent.__init__(self)
        self._local_fn = None
        self._remote_fn = None
        self.genomes = []
        if genome is None:
            genome = []
        for genome in genome:
            self.add_genome(genome)

    @property
    def hub(self):
        hub, level = self.root(Hub)
        if level is None:
            return None
        if level != -1:
            raise ValueError(
                "Found a hub at %s levels away -- needs to be -1" % level)
        return hub

    @property
    def local_fn(self):
        if self._local_fn is not None:
            return self._local_fn
        if self.hub is None:
            return None
        return os.path.join(
            os.path.dirname(self.hub.local_fn),
            self.hub.hub + '.genomes.txt')

    @local_fn.setter
    def local_fn(self, fn):
        self._local_fn = fn

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn
        if self.hub is None:
            return None
        return os.path.join(
            os.path.dirname(self.hub.remote_fn),
            self.hub.hub + '.genomes.txt')

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    def add_genome(self, genome):
        self.add_child(genome)
        self.genomes = self.children

    def __str__(self):
        s = []
        for genome in self.genomes:
            s.append(str(genome))
        return '\n'.join(s) + '\n'

    def _render(self):
        """
        Renders the children Genome objects to file
        """
        fout = open(self.local_fn, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name

    def validate(self):
        if len(self.children) == 0:
            raise ValueError(
                "No defined Genome objects to use")
