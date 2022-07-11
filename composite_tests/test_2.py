"""test_2.py:composite, set composite's tracktype and include a parameter from that tracktype (e.g. for bigwig, viewLimits or something)"""

import trackhub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="test_1",
    genome="hg38",
    email="eva.jason@nih.gov")

composite = trackhub.CompositeTrack(
    name='composite_test1',
    short_label='test1',
    tracktype='bigWig',
    autoScale='on',
    viewLimits='10:50',
    visibility='full'
)
trackdb.add_tracks(composite)

bw_view = trackhub.ViewTrack(
    name='viewtrack',
    view='signal',
    visibility='full',
    tracktype='bigWig',
    short_label='view'
)
composite.add_view(bw_view)

track0 = trackhub.Track(
    name='sine0',
    source='/data/NICHD-core0/infrastructure/trackhub/trackhub/test/data/sine-hg38-0.bedgraph.bw',
#visibility='full',
    tracktype='bigWig',
)
bw_view.add_tracks(track0)

track1 = trackhub.Track(
    name='sine1',
    source='/data/NICHD-core0/infrastructure/trackhub/trackhub/test/data/sine-hg38-1.bedgraph.bw',
#    visibility='full',
    tracktype='bigWig',
)
bw_view.add_tracks(track1)
trackhub.upload.upload_hub(staging = 'staging', hub=hub, host="biowulf.nih.gov", remote_dir="/data/NICHD-core0/datashare/example_hubs/composite")
