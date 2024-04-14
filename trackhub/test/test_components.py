import pytest
from trackhub import Hub, GenomesFile, Genome, Track, CompositeTrack, \
    TrackDb, ViewTrack, SuperTrack, AggregateTrack
import os


class Components(object):
    def __init__(self):
        self.hub = Hub(
            hub='example_hub',
            short_label='example hub',
            long_label='an example hub for testing',
            email='none@example.com')
        self.genomes_file = GenomesFile()
        self.genome = Genome('dm3')
        self.trackdb = TrackDb()

        self.tracks = [
            Track(name='track1', tracktype='bam'),
            Track(name='track2', tracktype='bigWig'),
        ]

    def CONNECT(self):
        """
        Connect the components together. The default setup creates the objects
        but does not connect them.
        """
        self.hub.add_genomes_file(self.genomes_file)
        self.genomes_file.add_genome(self.genome)
        self.genome.add_trackdb(self.trackdb)
        self.trackdb.add_tracks(self.tracks)

    def DISCONNECT(self):
        """
        Re-run the setup, which results in unconnected components. Run
        CONNECT() to connect them up.
        """
        self.__init__()


@pytest.fixture
def components():
    return Components()


def test_components_connection(components):
    """
    meta test: make sure the test class's connect/disconnect is working
    """
    assert components.hub.genomes_file is None

    components.CONNECT()
    assert components.hub.genomes_file is components.genomes_file

    components.DISCONNECT()
    assert components.hub.genomes_file is None


# Filenames ---------------------------------------------------------------


def test_hub_fns(components):
    # Default unconnected
    assert components.hub.filename == "example_hub.hub.txt"

    # Connecting components should not change hub
    components.CONNECT()
    assert components.hub.filename == "example_hub.hub.txt"
    components.DISCONNECT()


def test_genome_file_fns(components):
    with pytest.raises(AttributeError):
        getattr(components.genomes_file, "url")

    # When unconnected, filenames should be None
    assert components.genomes_file.filename is None

    # ...though you can set them manually
    components.genomes_file.filename = "local.genomes"
    assert components.genomes_file.filename == "local.genomes"
    components.genomes_file.filename = None

    components.CONNECT()
    assert components.genomes_file.filename == "example_hub.genomes.txt"

    # when connected, overriding works
    components.genomes_file.filename = "local.genomes"
    assert components.genomes_file.filename == "local.genomes"
    components.genomes_file.filename = None

    # disconnecting brings it back to None
    components.DISCONNECT()
    assert components.genomes_file.filename is None

    # set the hub's local_dir; genomes_file should follow.
    components.CONNECT()

    # what happens if the hub's local FN is changed?
    components.hub.filename = "localhub/hub.txt"
    assert components.genomes_file.filename == "localhub/example_hub.genomes.txt"


def test_trackdb_fns(components):

    # when unconnected, no defaults
    assert components.trackdb.filename is None

    components.CONNECT()
    assert components.trackdb.filename == "dm3/trackDb.txt"

    # setting filename overrides
    components.trackdb.filename = "mytrackdb.txt"
    assert components.trackdb.filename == "mytrackdb.txt", components.trackdb.filename

    # genomes_file fn overrides
    components.trackdb.filename = None
    components.genomes_file.filename = "anotherdir/genomes.txt"
    assert components.trackdb.filename == "anotherdir/dm3/trackDb.txt"

    # reset parent hub and genomes file to get back to the default
    components.genomes_file.filename = None
    assert components.trackdb.filename == "dm3/trackDb.txt"


def test_track_fns(components):

    components.CONNECT()
    # local fns should still be None
    for track in components.tracks:
        assert track.source is None

    # filename is relative to the hub's filename
    assert components.tracks[0].filename == "dm3/track1.bam"
    assert components.tracks[1].filename == "dm3/track2.bigWig"

    # URL is relative to the trackDb
    assert components.tracks[0].url == "track1.bam"


def test_track_creation(components):
    track = Track(name="track0", tracktype="bam", source="t0.bam")
    assert track.source == "t0.bam"
