.. _bigNarrowPeak:

bigNarrowPeak example
---------------------
You can read more about preparing the files necessary for a bigGenePred track
on `UCSC's bigInteract help page
<https://genome.ucsc.edu/goldenPath/help/bigNarrowPeak.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigNarrowPeak_hub/bigNarrowPeak.hub.txt>`_

.. code-block:: python

    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="bigNarrowPeak",
        short_label="bigNarrowPeak",
        long_label="bigNarrowPeak",
        genome="hg38",
        email="eva.jason@nih.gov")

    track = trackhub.Track(
        tracktype='bigNarrowPeak',
        name='bigNarrowPeak', 
        bigDataUrl='http://genome.ucsc.edu/goldenPath/help/examples/bigNarrowPeak.bb',
        shortLabel='bigNarrowPeak',
        longLabel='bigNarrowPeak',
        visibility='full')
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigNarrowPeak_hub')
