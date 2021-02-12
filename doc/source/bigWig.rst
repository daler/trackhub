.. _bigWig:

bigWig example
----------------
You can read more about preparing the files necessary for a bigWig track
on `UCSC's bigWig help page
<https://genome.ucsc.edu/goldenPath/help/bigWig.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <>http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigWig_hub/bigWig.hub.txt&position=chr21:33031597-33041570>`_.

.. code-block:: python

    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name='bigWig',
        defaultPos = 'chr21:33031597-33041570',
        short_label='bigWig',
        long_label='bigWig',
        genome='hg19',
        email='eva.jason@nih.gov')

    track = trackhub.Track(
        name = 'bigWig',
        tracktype = 'bigWig',
        bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigWigExample.bw',
        shortLabel = 'Example Hub',
        longLabel ='Example Hub',
        visibility = 'full')
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigWig_hub')
