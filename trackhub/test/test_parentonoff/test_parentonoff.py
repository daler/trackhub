import trackhub
import os

HERE = os.path.abspath(os.path.dirname(__file__))

def test_parentonoff():

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="TestHub",
        short_label="TestHub",
        long_label="TestHub",
        email="karen.kapur@novartis.com",
        genome="hg19"
    )

    testcomposite = trackhub.track.CompositeTrack(
        name="testcomposite",
        short_label="testlabelshort",
        long_label="testlabellong",
        tracktype="bigWig",
        visibility="full"
    )

    viewtrack = trackhub.track.ViewTrack(
        name="testviewtrack",
        view="view1",
        tracktype="bigWig",
        visibility="full",
        parent="on",
    )

    trackoff = trackhub.track.Track(
        name="E003DNase",
        url=("http://egg2.wustl.edu/roadmap/data/byFileType/signal/"
             "consolidated/macs2signal/pval/E003-DNase.pval.signal."
             "bigwig"),
        tracktype="bigWig",
        short_label="E003DNase",
        long_label="E003DNase",
        visibility="full",
        parent="off"
        )
    trackon = trackhub.track.Track(
        name="E004DNase",
        url=("http://egg2.wustl.edu/roadmap/data/byFileType/signal/"
             "consolidated/macs2signal/pval/E004-DNase.pval.signal"
             ".bigwig"),
        tracktype="bigWig",
        short_label="E004DNase",
        long_label="E004DNase",
        visibility="full",
        parent="on"
        )
    trackdefault = trackhub.track.Track(
        name="E005DNase",
        url=("http://egg2.wustl.edu/roadmap/data/byFileType/signal/"
             "consolidated/macs2signal/pval/E005-DNase.pval.signal"
             ".bigwig"),
        tracktype="bigWig",
        short_label="E005DNase",
        long_label="E005DNase",
        visibility="full"
        )

    viewtrack.add_tracks(trackoff)
    viewtrack.add_tracks(trackon)
    viewtrack.add_tracks(trackdefault)

    testcomposite.add_view(viewtrack)
    trackdb.add_tracks(testcomposite)

    tmpdir, linknames = trackhub.upload.stage_hub(hub)

    assert(
        open(os.path.join(tmpdir, 'hg19/trackDb.txt')).read() ==
        open(os.path.join(HERE, 'expected/hg19/trackDb.txt')).read()
    )
