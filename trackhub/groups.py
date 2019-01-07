from __future__ import absolute_import

import os
from .validate import ValidationError
from .base import HubComponent
from .genome import Genome
from .genomes_file import GenomesFile


class GroupDefinition(object):

    def __init__(self, name, label=None, priority=1, default_is_closed=0):
        """
        Represents a group of tracks in a trackhub.

        Instances of this class are provided to an assembly.

        Parameters
        ----------

        name : str
            Name for the group (e.g., "map").

        label : str
            The label that will be displayed (e.g., "Mapping")

        priority : int
            Orders this track group with the other track groups

        default_is_closed : 0 | 1
            Determines if this track group is expanded or closed by default.
            Values to use are 0 or 1
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
            'defaultIsClosed %d' % self.default_is_closed
        ]
        return '\n'.join(s) + '\n'


class GroupsFile(HubComponent):
    def __init__(self, groups, filename=None):
        """
        Represents the groups file on disk, used for assembly hubs.

        Parameters
        ----------
        groups : list
            List of GroupDefinition objects

        filename : str
            Filename to use, relative to the top-level hub. If None, default is
            to use "<genome>/groups.txt"
        """
        HubComponent.__init__(self)
        self.groups = []
        self.add_groups(groups)
        self._filename = filename

    def add_groups(self, groups):
        """
        Add a list of GroupDefinition objects.

        Parameters
        ----------
        groups : list
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
    def filename(self):
        if self._filename is not None:
            return self._filename

        if self.genome is None:
            return None

        if self.genomes_file is None:
            return None

        else:
            return os.path.join(os.path.dirname(self.genomes_file.filename),
                                self.genome.genome, 'groups.txt')

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    def validate(self):
        if self.genome is None:
            raise ValidationError(
                "GroupsFile object must be attached to an Genome instance "
                "or subclass")
        pass

    def _render(self, staging='staging'):
        """
        Renders the children GroupDefinition objects to file
        """
        rendered_filename = os.path.join(staging, self.filename)
        self.makedirs(rendered_filename)
        fout = open(rendered_filename, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name
