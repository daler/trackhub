import os
from textwrap import dedent
import pytest
import tempfile
from trackhub import upload
from trackhub.helpers import data_dir
from trackhub import (
    Hub,
    GenomesFile,
    Genome,
    Track,
    CompositeTrack,
    TrackDb,
    ViewTrack,
    SuperTrack,
    AggregateTrack,
)

d = data_dir()


class Upload(object):
    def __init__(self):
        self.hub = Hub(
            hub="example_hub",
            short_label="example hub",
            long_label="an example hub for testing",
            email="none@example.com",
        )
        self.genomes_file = GenomesFile()
        self.genome = Genome("dm3")
        self.trackdb = TrackDb()

        self.tracks = [
            Track(
                name="track1",
                tracktype="bigBed",
                source=os.path.join(d, "random-hg38-0.bigBed"),
            ),
            Track(
                name="track2",
                tracktype="bigWig",
                source=os.path.join(d, "sine-hg38-0.bedgraph.bw"),
            ),
            Track(
                name="track3",
                tracktype="bigWig",
                source=os.path.join(d, "sine-hg38-1.bedgraph.bw"),
                filename="3.bw",
            ),
        ]
        self.hub.add_genomes_file(self.genomes_file)
        self.genomes_file.add_genome(self.genome)
        self.genome.add_trackdb(self.trackdb)
        self.trackdb.add_tracks(self.tracks)


@pytest.fixture
def upload_obj():
    return Upload()


def test_staging(upload_obj):
    staging_dir, linknames = upload.stage_hub(upload_obj.hub)

    assert open(os.path.join(staging_dir, "example_hub.genomes.txt")).read() == dedent(
        """\
        genome dm3
        trackDb dm3/trackDb.txt

        """
    )

    assert open(os.path.join(staging_dir, "example_hub.hub.txt")).read() == dedent(
        """\
        hub hub
        shortLabel example hub
        longLabel an example hub for testing
        genomesFile example_hub.genomes.txt
        email none@example.com"""
    )


def test_upload(upload_obj):
    d = tempfile.mkdtemp()
    print(d)
    upload.upload_hub(
        hub=upload_obj.hub,
        remote_dir=d,
        user=None,
        host=None,
    )


def test_render(upload_obj):
    trackdb = str(upload_obj.trackdb)
    # make sure some of the trackdb rendered correctly
    assert "track track1" in trackdb
    assert "bigDataUrl track1.bigBed" in trackdb
    assert "bigDataUrl ../3.bw" in trackdb
