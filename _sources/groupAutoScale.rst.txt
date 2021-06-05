.. _groupAutoScale:

groupAutoScale example
----------------
You can read more about preparing the files necessary for a track that auto scales as a group
on `UCSC's Configuring graph based-tracks help page <https://genome.ucsc.edu/goldenPath/help/hgWiggleTrackHelp.html>`_.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_groupAutoScale_hub/groupAutoScale.hub.txt&position=chr1>`_.

.. code-block:: python

    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
         hub_name="groupAutoScale",
         short_label="groupAutoScale",
         long_label="groupAutoScale",
         genome="hg38",
         email="eva.jason@nih.gov")

    composite = trackhub.CompositeTrack(
         name='composite',
         short_label='Group AutoScale',
         tracktype='bigWig',
         visibility='full')

    trackdb.add_tracks(composite)

    signal_view = trackhub.ViewTrack(
         name='group',
         view='group_view',
         visibility='full',
         tracktype='bigWig',
         short_label='Signal')
    composite.add_tracks(signal_view)

    track_1 = trackhub.Track(
         tracktype='bigWig',
         name='Track_1', 
         color='199,122,118',
         visibility='full',
         source = 'sine-hg38-0.bedgraph.bw',
         autoScale='group')
    signal_view.add_tracks(track_1)

    track_2 = trackhub.Track(
         tracktype='bigWig',
         name='Track_2', 
         color='118,199,122',
         visibility='full',
         source = 'sine-hg38-1.bedgraph.bw',
         autoScale='group')

    signal_view.add_tracks(track_2)

    track_3 = trackhub.Track(
         tracktype='bigWig',
         name='Track_3', 
         color='122,118,199',
         visibility='full',
         source = 'sine-hg38-2.bedgraph.bw',
         autoScale='group')
    signal_view.add_tracks(track_3)

    trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_autoGroupScale_hub'
