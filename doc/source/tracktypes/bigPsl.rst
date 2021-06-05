.. _bigPsl:

bigPsl example
--------------
You can read more about preparing the files necessary for a bigPsl track
on `UCSC's bigPsl help page
<https://genome.ucsc.edu/goldenPath/help/bigPsl.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigPsl_hub/bigPsl.hub.txt&position=chr1:10000-200000>`_.

.. code-block:: python

    import trackhub

    hub, genome, genomes_file, trackdb = trackhub.default_hub(
        hub_name="bigPsl",
        short_label="bigPsl",
        long_label="bigPsl",
        genome="hg38",
        email="eva.jason@nih.gov",
    )

    track = trackhub.Track(
        name="bigPsl",
        tracktype="bigPsl",
        bigDataUrl="http://genome.ucsc.edu/goldenPath/help/examples/bigPsl.bb",
    )
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(
        hub=hub, host="localhost", remote_dir="example_hubs/example_bigPsl_hub"
    )
