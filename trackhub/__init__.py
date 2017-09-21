from __future__ import absolute_import

import tempfile
from .hub import Hub
from . import helpers
from . import upload
from .genomes_file import GenomesFile
from .genome import Genome
from .assembly import Assembly
from .groups import GroupsFile, GroupDefinition
from .trackdb import TrackDb
from .track import Track, SubGroupDefinition, CompositeTrack, \
    ViewTrack, SuperTrack, AggregateTrack
from .version import version as __version__


def default_hub(hub_name, genome, short_label, long_label, email, basedir=None):
    """
    Returns a fully-connected set of hub components using default filenames.

    Parameters
    ----------

    hub_name : str
        Name of the hub

    genome : str
        Assembly name (hg38, dm6, etc)

    short_label, long_label : str
        Labels for the hub

    email : str
        Email to include with hub

    basedir : str or None
        If None, uses a tempdir when rendering the hub files. If str, render
        the files there.
    """
    hub = Hub(
        hub=hub_name,
        short_label=short_label,
        long_label=long_label,
        email=email)

    if basedir is None:
        basedir = tempfile.mkdtemp()

    hub.local_dir = basedir
    genome = Genome(genome)
    genomes_file = GenomesFile()
    trackdb = TrackDb()
    hub.add_genomes_file(genomes_file)
    genomes_file.add_genome(genome)
    genome.add_trackdb(trackdb)
    return hub, genomes_file, genome, trackdb
