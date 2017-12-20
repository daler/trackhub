import pytest
from trackhub import Hub, GenomesFile, Genome, Track, CompositeTrack, \
    TrackDb, ViewTrack, SuperTrack, AggregateTrack
import os


class TestComponents(object):
    def setup(self):
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
        self.setup()

    def test_self_connection(self):
        """
        meta test: make sure the test class's connect/disconnect is working
        """
        assert self.hub.genomes_file is None

        self.CONNECT()
        assert self.hub.genomes_file is self.genomes_file

        self.DISCONNECT()
        assert self.hub.genomes_file is None

    # Filenames ---------------------------------------------------------------

    def test_hub_fns(self):
        # Default unconnected
        assert self.hub.filename == 'example_hub.hub.txt'

        # Connecting components should not change hub
        self.CONNECT()
        assert self.hub.filename == 'example_hub.hub.txt'
        self.DISCONNECT()

    def test_genome_file_fns(self):
        with pytest.raises(AttributeError):
            getattr(self.genomes_file, 'url')

        # When unconnected, filenames should be None
        assert self.genomes_file.filename is None

        #...though you can set them manually
        self.genomes_file.filename = 'local.genomes'
        assert self.genomes_file.filename == 'local.genomes'
        self.genomes_file.filename = None

        self.CONNECT()
        assert self.genomes_file.filename == 'example_hub.genomes.txt'

        # when connected, overriding works
        self.genomes_file.filename = 'local.genomes'
        assert self.genomes_file.filename == 'local.genomes'
        self.genomes_file.filename = None

        # disconnecting brings it back to None
        self.DISCONNECT()
        assert self.genomes_file.filename is None

        # set the hub's local_dir; genomes_file should follow.
        self.CONNECT()

        # what happens if the hub's local FN is changed?
        self.hub.filename = 'localhub/hub.txt'
        assert self.genomes_file.filename == 'localhub/example_hub.genomes.txt'

    def test_trackdb_fns(self):

        # when unconnected, no defaults
        assert self.trackdb.filename is None

        self.CONNECT()
        assert self.trackdb.filename == 'dm3/trackDb.txt'

        # setting filename overrides
        self.trackdb.filename = 'mytrackdb.txt'
        assert self.trackdb.filename == 'mytrackdb.txt', self.trackdb.filename

        # genomes_file fn overrides
        self.trackdb.filename = None
        self.genomes_file.filename = 'anotherdir/genomes.txt'
        assert self.trackdb.filename == 'anotherdir/dm3/trackDb.txt'

        # reset parent hub and genomes file to get back to the default
        self.genomes_file.filename = None
        assert self.trackdb.filename == 'dm3/trackDb.txt'

    def test_track_fns(self):

        self.CONNECT()
        # local fns should still be None
        for track in self.tracks:
            assert track.source is None

        # filename is relative to the hub's filename
        assert self.tracks[0].filename == 'dm3/track1.bam'
        assert self.tracks[1].filename == 'dm3/track2.bigWig'

        # URL is relative to the trackDb
        assert self.tracks[0].url == 'track1.bam'


    def test_track_creation(self):
        track = Track(name='track0', tracktype='bam', source='t0.bam')
        assert track.source == 't0.bam'
