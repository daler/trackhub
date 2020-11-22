from __future__ import absolute_import

import tempfile
from . import track
from . import settings
from .hub import Hub
from . import helpers
from . import upload
from .genomes_file import GenomesFile
from .genome import Genome
from .assembly import Assembly
from .groups import GroupsFile, GroupDefinition
from .trackdb import TrackDb
from .track import BaseTrack, Track, SubGroupDefinition, CompositeTrack, \
    ViewTrack, SuperTrack, AggregateTrack
from .version import version as __version__


def default_hub(hub_name, genome, email, short_label=None, long_label=None, defaultPos=None):
    """
    Returns a fully-connected set of hub components using default filenames.

    Parameters
    ----------

    hub_name : str
        Name of the hub

    genome : str
        Assembly name (hg38, dm6, etc)

    email : str
        Email to include with hub.

    short_label : str
        Short label for the hub. If None, defaults to the value of `hub_name`

    long_label : str
        Long label for the hub. If None, defaults to the value of `short_label`.

    defaultPos : str
        Default position for the hub
    """
    if short_label is None:
        short_label = hub_name
    if long_label is None:
        long_label = short_label

    hub = Hub(
        hub=hub_name,
        short_label=short_label,
        long_label=long_label,
        email=email)

    genome_kwargs = {}
    if defaultPos:
        genome_kwargs['defaultPos'] = defaultPos
    genome = Genome(genome, **genome_kwargs)
    genomes_file = GenomesFile()
    trackdb = TrackDb()
    hub.add_genomes_file(genomes_file)
    genomes_file.add_genome(genome)
    genome.add_trackdb(trackdb)
    return hub, genomes_file, genome, trackdb
