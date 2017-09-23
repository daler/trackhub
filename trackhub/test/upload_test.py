import os
import pytest
import tempfile
from trackhub import upload
from trackhub.helpers import data_dir
from trackhub import Hub, GenomesFile, Genome, Track, CompositeTrack, \
    TrackDb, ViewTrack, SuperTrack, AggregateTrack

d = data_dir()

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
                tracktype='bigBed',
                local_fn=os.path.join(d, 'random-dm3-0.bigBed')
            ),
            Track(
                name='track2',
                tracktype='bigWig',
                local_fn=os.path.join(d, 'sine-dm3-10000.bedgraph.bw'),
            ),
        ]
        self.hub.add_genomes_file(self.genomes_file)
        self.genomes_file.add_genome(self.genome)
        self.genome.add_trackdb(self.trackdb)
        self.trackdb.add_tracks(self.tracks)


    #@unittest.skipUnless(os.path.exists('data/track1.bam'), 'No test data')
    def test_upload(self):
        d = tempfile.mkdtemp()
        self.hub.remote_fn = os.path.join(
            d,
            'uploaded_version',
            self.hub.remote_fn)
        self.hub.render()
        upload.upload_hub(
            hub=self.hub,
            user=None,
            host=None,
        )

    def test_render(self):
        trackdb = str(self.trackdb)
        # make sure some of the trackdb rendered correctly
        assert 'track track1' in trackdb
        assert 'bigDataUrl track1.bigBed' in trackdb
