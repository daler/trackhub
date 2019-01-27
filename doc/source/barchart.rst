

.. code-block:: python

    import trackhub

    # Initialize the components of a track hub, already connected together
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="barchartexample",
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
        visibility='full',
    )
    trackdb.add_tracks(track)

    # Example of "uploading" the hub locally, to be pushed to github later:
    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_barchart_hub')
