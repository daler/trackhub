from __future__ import absolute_import

import os
from .hub import Hub
from .base import HubComponent


class GenomesFile(HubComponent):
    def __init__(self, genome=None, filename=None):
        """
        Represents the genomes file on disk.  Can contain multiple `Genome`
        objects, each of which represent a stanza in this file.

        Parameters
        ----------

        genome : list
            List of Genome objects

        filename : str
            Filename relative to the hub file. If None, defaults to
            "<hubname>.genomes.txt"
        """
        HubComponent.__init__(self)
        self.filename = filename
        self.genomes = []
        if genome is None:
            genome = []
        for genome in genome:
            self.add_genome(genome)

        self._filename = filename

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename
        if self.hub is None:
            return None
        return os.path.join(
            os.path.dirname(self.hub.filename),
            self.hub.hub + '.genomes.txt')

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    @property
    def hub(self):
        hub, level = self.root(Hub)
        if level is None:
            return None
        if level != -1:
            raise ValueError(
                "Found a hub at %s levels away -- needs to be -1" % level)
        return hub

    def add_genome(self, genome):
        self.add_child(genome)
        self.genomes = self.children

    def __str__(self):
        s = []
        for genome in self.genomes:
            s.append(str(genome))
        return '\n'.join(s) + '\n'

    def _render(self, staging='staging'):
        rendered_filename = os.path.join(staging, self.filename)
        self.makedirs(rendered_filename)
        fout = open(rendered_filename, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name

    def validate(self):
        if len(self.children) == 0:
            raise ValueError(
                "No defined Genome objects to use")
