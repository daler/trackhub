from hub import Hub
import helpers
from genomes_file import GenomesFile
from genome import Genome
from trackdb import TrackDb
from track import Track, SubGroupDefinition, CompositeTrack, \
    ViewTrack, SuperTrack, AggregateTrack
from version import version as __version__


def default_hub(hub_name, genome, short_label, long_label, email):
    """
    Returns a fully-connected set of hub components using default filenames.
    """
    hub = Hub(
        hub=hub_name,
        short_label=short_label,
        long_label=long_label,
        email=email)
    genome = Genome(genome)
    genomes_file = GenomesFile()
    trackdb = TrackDb()
    hub.add_genomes_file(genomes_file)
    genomes_file.add_genome(genome)
    genome.add_trackdb(trackdb)
    return hub, genomes_file, genome, trackdb
