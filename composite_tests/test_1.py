"""test_1.py: write a test that creates a composite track that sets bigwig parameters to be inherited by child tracks."""

import trackhub
trackhub.settings.VALIDATE = True
hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="test_1",
    defaultPos='chr1:1-5000',
    genome="hg38",
    email="eva.jason@nih.gov")

composite = trackhub.CompositeTrack(
    name='composite_test1',
    short_label='test1',
    tracktype='bigWig',
    autoScale='on',
    color='119,10,233',
    viewLimits='5:50',
    visibility='full'
)
trackdb.add_tracks(composite)

bw_view = trackhub.ViewTrack(
    name='viewtrack',
    view='signal',
    tracktype='bigWig',
    viewLimits='5:50',
    short_label='view'
)
composite.add_view(bw_view)

track0 = trackhub.Track(
    name='sine0',
    source='/data/NICHD-core0/infrastructure/trackhub/trackhub/test/data/sine-hg38-0.bedgraph.bw',
    visibility='full',
    color='124, 233, 10',
    tracktype='bigWig',
)
bw_view.add_tracks(track0)

track1 = trackhub.Track(
    name='sine1',
    source='/data/NICHD-core0/infrastructure/trackhub/trackhub/test/data/sine-hg38-1.bedgraph.bw',
    visibility='full',
    tracktype='bigWig',
)
bw_view.add_tracks(track1)
trackhub.upload.upload_hub(staging = 'staging', hub=hub, host="biowulf.nih.gov", remote_dir="/data/NICHD-core0/datashare/example_hubs/composite")
