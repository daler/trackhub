
.. _barchart_example:

bigBarChart example
-------------------
You can read more about preparing the files necessary for a bigBarChart track
on `UCSC's bigBarChart help page
<https://genome.ucsc.edu/goldenPath/help/barChart.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgHubConnect?hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgHub_do_firstDb=1&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_assembly_hub/assembly_hub.hub.txt&position=chr14%3A95060967%2D95501030>`_.


.. code-block:: python

    import trackhub

    # Initialize the components of a track hub, already connected together
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="barchart_hub",
        short_label='example barChart',
        long_label='example barChart',
        genome="hg38",
        email="dalerr@niddk.nih.gov")

    track = trackhub.Track(
        name='bar1',
        tracktype='bigBarChart',
        barChartBars='adiposeSubcut breastMamTissue colonTransverse muscleSkeletal wholeBlood',
        barChartColors='#FF6600 #33CCCC #CC9955 #AAAAFF #FF00BB',
        url='http://genome.ucsc.edu/goldenPath/help/examples/barChart/hg38.gtexTranscripts.bb',
        barChartMatrixUrl='http://genome.ucsc.edu/goldenPath/help/examples/barChart/exampleMatrix.txt',
        barChartSampleUrl='http://genome.ucsc.edu/goldenPath/help/examples/barChart/exampleSampleData.txt',
        barChartLabel='Tissues',
        barChartMetric='median',
        visibility='pack',
    )
    trackdb.add_tracks(track)

    # Example of "uploading" the hub locally, to be pushed to github later:
    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_barchart_hub')
