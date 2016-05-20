import os
from validate import ValidationError
from base import HubComponent
from genome import Genome
from genomes_file import GenomesFile

class GroupDefinition(object):

    def __init__(self, name, label=None, priority=1, default_is_closed=0):
        """
        Represents a group of tracks in a trackhub.

        Instances of this class are provided to an assembly.

        :param name:
            String; name for the group (e.g., "map").

        :param label:
            String; the label that will be displayed (e.g., "Mapping")

        :param priority:
            Orders this track group with the other track groups

        :param default_is_closed:
            Determines if this track group is expanded or closed by default. Values to use are 0 or 1
        """
        self.name = str(name)
        if label is None:
            label = name
        self.label = str(label)
        self.priority = int(priority)
        if default_is_closed in (0, 1):
            self.default_is_closed = default_is_closed
        else:
            raise ValueError("default_is_closed must be 1 or 0")

    def __str__(self):
        s = [
            'name %s' % self.name,
            'label %s' % self.label,
            'priority %s' % self.priority,
            'defaultIsClosed %s' % self.default_is_closed
        ]
        return '\n'.join(s) + '\n'

class GroupsFile(HubComponent):
    def __init__(self, groups):
        HubComponent.__init__(self)
        self._local_fn = None
        self._remote_fn = None
        self.groups = []
        self.add_groups(groups)

    def add_groups(self, groups):
        """
        Add a list of GroupDefinition objects.

        :param groups:
            List of GroupDefinition objects.
        """
        self.groups.extend(groups)

    def __str__(self):
        """
        Render groups.txt file.
        """
        return '\n'.join(g.__str__() for g in self.groups)

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
                                self.genome.genome, 'groups.txt')

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

        return os.path.join(os.path.dirname(self.genomes_file.remote_fn),
                            self.genome.genome, "groups.txt")

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

    def validate(self):
        if self.genome is None:
            raise ValidationError("GroupsFile object must be attached to an Genome instance or subclass")
        pass

    def _render(self):
        """
        Renders the children GroupDefinition objects to file
        """
        fout = open(self.local_fn, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name

