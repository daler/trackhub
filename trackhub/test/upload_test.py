from trackhub import upload
import os
import unittest
from trackhub import Hub, GenomesFile, Genome, Track, CompositeTrack, \
    TrackDb, ViewTrack, SuperTrack, AggregateTrack


class TestUpload(object):
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
            Track(
                name='track1',
                tracktype='bam',
                local_fn='data/track1.bam'
            ),
            Track(
                name='track2',
                tracktype='bigWig',
                local_fn='data/track2.bigwig',
            ),
        ]
        self.hub.add_genomes_file(self.genomes_file)
        self.genomes_file.add_genome(self.genome)
        self.genome.add_trackdb(self.trackdb)
        self.trackdb.add_tracks(self.tracks)


    @unittest.skipUnless(os.path.exists('data/track1.bam'), 'No test data')
    def test_upload(self):
        self.hub.remote_fn = os.path.join(
            'uploaded_version',
            self.hub.remote_fn)
        self.hub.render()
        upload.upload_hub(
            'localhost',
            None,
            self.hub,
            symlink=True,
            symlink_dir='staging',
            run_local=True,)
        for t, level in self.hub.leaves(Track):
            upload.upload_track(
                track=t, host='localhost', user=None, run_local=True)

    def test_render(self):
        trackdb = str(self.trackdb)
        # make sure some of the trackdb rendered correctly
        assert 'track track1' in trackdb
        assert 'bigDataUrl track1.bam' in trackdb
