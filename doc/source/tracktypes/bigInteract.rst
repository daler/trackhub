.. _bigInteract:

bigInteract example
-------------------
You can read more about preparing the files necessary for a bigInteract track
on `UCSC"s bigInteract help page
<https://genome.ucsc.edu/goldenPath/help/bigInteract.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigInteract_hub/bigInteract.hub.txt&position=chr3:63820967-63880091>`_.

.. code-block:: python

    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="bigInteract",
        defaultPos="chr3:63820967-63880091",
        short_label="bigInteract",
        long_label="bigInteract",
        genome="hg19",
        email="eva.jason@nih.gov")

    track = trackhub.Track(
        name="bigInteract",
        tracktype="bigInteract",
        bigDataUrl="http://genome.ucsc.edu/goldenPath/help/examples/interact/interactExample3.inter.bb",
        shortLabel="bigInteract",
        longLabel="bigInteract",
        visibility="pack",
        spectrum="on",
        scoreMin="175",
        maxHeightPixels="300:150:20")
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub=hub, host="localhost",
                               remote_dir="example_hubs/example_bigInteract_hub")
