import trackhub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="bigWig",
    defaultPos = 'chr21:33031597-33041570',
    short_label="bigWig",
    long_label="bigWig",
    genome="hg19",
    email="eva.jason@nih.gov")

track = trackhub.Track(
    name = 'bigWig',
    tracktype = 'bigWig',
    bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigWigExample.bw',
    shortLabel = 'Example Hub',
    longLabel ='Example Hub',
    visibility = 'full')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigWig_hub')