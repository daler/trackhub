.. _bigGenePred:

bigGenePred example
-------------------
You can read more about preparing the files necessary for a bigGenePred track
on `UCSC's bigBarChart help page
<https://genome.ucsc.edu/goldenPath/help/bigGenePred.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigGenePred_hub/bigGenePred.hub.txt&position=chr10:67884600-67884900>`_. 

.. code-block:: python

    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name='bigGenePred',
        short_label='bigGenePred',
        long_label='bigGenePred',
        defaultPos='chr10:67884600-67884900',
        genome='hg38',
        email='eva.jason@nih.gov')

    track = trackhub.Track(
        name='bigGenePred',
        bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigGenePredEx4.bb',
        shortLabel = 'bigGenePred',
        longLabel ='bigGenePred',
        tracktype = 'bigGenePred',
        visibility = 'pack')
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_bigGenePred_hub')
