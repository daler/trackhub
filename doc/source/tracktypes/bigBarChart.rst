.. _bigBarChart-example:

bigBarChart example
-------------------

You can read more about preparing the files necessary for a bigBarChart track
on `UCSC's bigBarChart help page
<https://genome.ucsc.edu/goldenPath/help/barChart.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigBarChart_hub/bigBarChart.hub.txt&position=chr14:95081796-95436280>`_.

.. code-block:: python

    import trackhub
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="bigBarChart",
        short_label="bigBarChart",
        long_label="bigBarChart",
        genome="hg38",
        defaultPos="chr14:95081796-95436280",
        email="eva.jason@nih.gov")
    track = trackhub.Track(
        name="bigBarChart",
        tracktype="bigBarChart",
        visibility="full",
        shortLabel="bigBarChart",
        longLabel="Simple example bar chart track",
        barChartBars="adiposeSubcut breastMamTissue colonTransverse muscleSkeletal wholeBlood",
        barChartColors="#FF6600 #33CCCC #CC9955 #AAAAFF #FF00BB",
        barChartLabel="Tissues",
        barChartMetric="median",
        barChartUnit="RPKM",
        bigDataUrl="http://genome.ucsc.edu/goldenPath/help/examples/barChart/hg38.gtexTranscripts.bb",
        barChartMatrixUrl="http://genome.ucsc.edu/goldenPath/help/examples/barChart/exampleMatrix.txt",
        barChartSampleUrl="http://genome.ucsc.edu/goldenPath/help/examples/barChart/exampleSampleData.txt")
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub=hub, host="localhost",
                               remote_dir="example_hubs/example_bigBarChart_hub")
