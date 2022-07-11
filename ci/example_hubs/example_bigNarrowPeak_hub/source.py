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
    shortLabel='bigNPk',
    longLabel='bigNarrowPeakExample',
    visibility='full')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigNarrowPeak_hub')