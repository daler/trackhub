import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from validate import ValidationError
from base import HubComponent
from genome import Genome


class Assembly(Genome):
    def __init__(self, genome, twobit_fn, trackdb=None, genome_file_obj=None, genome_info=None):
        """
        Represents a genome stanza within a "genomes.txt" file for a non-UCSC genome.

        The file itself is represented by a :class:`GenomesFile` object.
        """
        HubComponent.__init__(self)
        Genome.__init__(self, genome, trackdb=None, genome_file_obj=None)
        self.twobit_fn = twobit_fn
        self.genome_info = dict()
        if genome_info:
            self.genome_info.update(genome_info)

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <Assembly> object"
        s = []
        s.append('genome %s' % self.genome)
        trackdb_relpath = os.path.relpath(self.trackdb.local_fn,
                                          start = os.path.dirname(
                                                    self.parent.parent.local_fn)) #local_fn of hub file
        s.append('trackDb %s' % trackdb_relpath)
        twobit_relpath = os.path.relpath(self.twobit_fn,
                                          start = os.path.dirname(
                                                    self.parent.parent.local_fn)) #local_fn of hub file
        s.append('twoBitPath %s' % twobit_relpath)
        for k, v in self.genome_info.iteritems():
            s.append(str(k) + ' ' + str(v))
        return '\n'.join(s) + '\n'

