.. _bigLolly:

bigLolly example
----------------
You can read more about preparing the files necessary for a bigLolly track
on `UCSC's bigLolly help page
<https://genome.ucsc.edu/goldenPath/help/bigLolly.html>`_. The following code uses the example files provided by UCSC.
This track type uses non-standard names for some parameters. These paramters can be added as a dictionary and setting
`trackhub.settings.VALIDATE = False`.

This code is automatically run and the built trackhub is uploaded to the `trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db = hg38&hubUrl = https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigLolly_hub/bigLolly.hub.txt&position = chr21:25891755-25891870>`_.

.. code-block:: python

    import trackhub

    trackhub.settings.VALIDATE = False
    hub, genome, genomes_file, trackdb = trackhub.default_hub(
        hub_name="bigLolly",
        short_label="bigLolly",
        long_label="bigLolly",
        genome="hg38",
        defaultPos="chr21:25891755-25891870",
        email="eva.jason@nih.gov",
    )

    add_kwargs = {"yAxisLabel.1": "0 on 30,30,190 0", "yAxisLabel.1": "5 on 30,30,190 5"}

    track = trackhub.Track(
        tracktype="bigLolly",
        bigDataUrl="http://genome.ucsc.edu/goldenPath/help/examples/bigLollyExample3.bb",
        name="bigLolly",
        lollySizeField="lollySize",
        visibility="full",
        noStems="on",
        lollyMaxSize=10,
        **add_kwargs
    )
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(
        hub=hub, host="localhost", remote_dir="example_hubs/example_bigLolly_hub"
    )
