import trackhub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name='bigGenePred',
    short_label='bigGenePred',
    long_label='bigGenePred',
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