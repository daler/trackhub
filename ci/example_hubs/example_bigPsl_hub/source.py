import trackhub

hub, genome, genomes_file,trackdb = trackhub.default_hub(
    hub_name='bigPsl',
    short_label='bigPsl',
    long_label='bigPsl',
    genome='hg38',
    email='eva.jason@nih.gov')

track = trackhub.Track(
    name = 'bigPsl',
    tracktype ='bigPsl',
    bigDataUrl='http://genome.ucsc.edu/goldenPath/help/examples/bigPsl.bb')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigPsl_hub')