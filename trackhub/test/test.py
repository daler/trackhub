from nose.tools import assert_raises
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
        self.hub.add_genomes_file(self.genomes_file)
        self.genomes_file.add_genome(self.genome)
        self.genome.add_trackdb(self.trackdb)
        self.trackdb.add_tracks(self.tracks)

    def DISCONNECT(self):
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
        assert self.hub.local_fn == 'example_hub.hub.txt'
        assert self.hub.remote_fn == 'example_hub.hub.txt'
        assert self.hub.url is None

        # Connecting components should not change hub
        self.CONNECT()
        assert self.hub.local_fn == 'example_hub.hub.txt'
        assert self.hub.remote_fn == 'example_hub.hub.txt'
        assert self.hub.url is None
        self.DISCONNECT()

        # set local/remote dir and fns should follow
        self.hub.local_dir = '/data/hubs'
        self.hub.remote_dir = '/remote/hubs'
        assert self.hub.local_fn == '/data/hubs/example_hub.hub.txt', \
            self.hub.local_fn
        assert self.hub.remote_fn == '/remote/hubs/example_hub.hub.txt', \
            self.hub.remote_fn

        # resetting them should not change
        self.hub.local_dir = None
        self.hub.remote_dir = None
        assert self.hub.local_fn == 'example_hub.hub.txt'
        assert self.hub.remote_fn == 'example_hub.hub.txt'

        # changing local_fn or remote_fn should stick -- and should override
        # any set local/remote dir
        self.hub.local_fn = 'dummy.txt'
        self.hub.remote_fn = 'remote.txt'
        self.hub.local_dir = 'no_dir'
        self.hub.remote_dir = 'remote_dir'
        assert self.hub.local_fn == 'dummy.txt'
        assert self.hub.remote_fn == 'remote.txt'

    def test_genome_file_fns(self):
        assert_raises(AttributeError, getattr, self.genomes_file, 'url')
        # When unconnected, filenames should be None
        assert self.genomes_file.local_fn is None
        assert self.genomes_file.remote_fn is None

        #...though you can set them manually
        self.genomes_file.local_fn = 'local.genomes'
        assert self.genomes_file.local_fn == 'local.genomes'
        self.genomes_file.local_fn = None

        self.CONNECT()
        assert self.genomes_file.local_fn == 'example_hub.genomes.txt'

        # when connected, overriding works
        self.genomes_file.local_fn = 'local.genomes'
        assert self.genomes_file.local_fn == 'local.genomes'
        self.genomes_file.local_fn = None

        # disconnecting brings it back to None
        self.DISCONNECT()
        assert self.genomes_file.local_fn is None

        # set the hub's local_dir; genomes_file should follow.
        self.CONNECT()
        self.hub.local_dir = 'local/'
        assert self.genomes_file.local_fn == 'local/example_hub.genomes.txt'

        # what happens if the hub's local FN is changed?
        self.hub.local_fn = 'localhub/hub.txt'
        assert self.genomes_file.local_fn == 'localhub/example_hub.genomes.txt'

    def test_genome_fns(self):
        # should be easy -- filenames should raise attribute errors
        assert_raises(AttributeError, getattr, self.genome, 'local_fn')
        assert_raises(AttributeError, getattr, self.genome, 'remote_fn')
        assert_raises(AttributeError, getattr, self.genome, 'url')

    def test_trackdb_fns(self):
        assert_raises(AttributeError, getattr, self.trackdb, 'url')

        # when unconnected, no defaults
        assert self.trackdb.local_fn is None
        assert self.trackdb.remote_fn is None

        self.CONNECT()
        assert self.trackdb.local_fn == 'dm3/trackDb.txt'
        assert self.trackdb.remote_fn == 'dm3/trackDb.txt'

        # setting the local dir on the hub trickles down
        self.hub.local_dir = 'localdir'
        assert self.trackdb.local_fn == 'localdir/dm3/trackDb.txt'

        # setting local_fn overrides
        self.trackdb.local_fn = 'mytrackdb.txt'
        assert self.trackdb.local_fn == 'mytrackdb.txt', self.trackdb.local_fn

        # ...and back to None to reset
        self.trackdb.local_fn = None
        assert self.trackdb.local_fn == 'localdir/dm3/trackDb.txt'

        # genomes_file fn overrides
        self.genomes_file.local_fn = 'anotherdir/genomes.txt'
        assert self.trackdb.local_fn == 'anotherdir/dm3/trackDb.txt'

        # reset parent hub and genomes file to get back to the default
        self.genomes_file.local_fn = None
        self.hub.local_dir = None
        assert self.trackdb.local_fn == 'dm3/trackDb.txt'

    def test_track_fns(self):
        for track in self.tracks:
            assert track.local_fn is None
            assert track.remote_fn is None
            assert track.url is None

        self.CONNECT()
        # local fns should still be None
        for track in self.tracks:
            assert track.local_fn is None

        assert self.tracks[0].remote_fn == 'dm3/track1.bam'
        assert self.tracks[1].remote_fn == 'dm3/track2.bigWig'

        self.hub.remote_fn = '/var/www/hubs/hub.txt'
        self.hub.url = 'http://example.com/hubs/hub.txt'

        print self.tracks[0].remote_fn
        print self.hub.remote_fn
        assert self.tracks[0].url == 'http://example.com/hubs/dm3/track1.bam'


    def test_track_creation(self):
        track = Track(name='track0', tracktype='bam', local_fn='t0.bam')
        assert track.local_fn == 't0.bam'
