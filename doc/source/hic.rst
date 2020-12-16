
.. _hic_example:

Hi-C example
------------
You can read more about preparing the files necessary for a bigBarChart track
on `UCSC's hic help page
<https://genome.ucsc.edu/goldenPath/help/hic.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgHubConnect?hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgHub_do_firstDb=1&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_hubs/example_hic_hub/hic_example.hub.txt>`_.


.. code-block:: python

    import trackhub
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="hic",
        defaultPos= 'chr21:32000000-35000000',
        short_label="hic_example",
        long_label="hic_example",
        genome="hg19",
        email="eva.jason@nih.gov")

    track = trackhub.Track(
        name = 'examplehicTrack',
        tracktype = 'hic',
        visibility = 'dense',
        url = 'http://hgdownload.soe.ucsc.edu/gbdb/hg19/bbi/hic/GSE63525_GM12878_insitu_primary+replicate_combined.hic',
        shortLabel = 'hic example',
        longLabel = 'This hic file shows in situ Hi-C data from Rao et al. (2014) on the GM12878 cell line',
        )

    trackdb.add_tracks(track)
    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_hic_hub')
