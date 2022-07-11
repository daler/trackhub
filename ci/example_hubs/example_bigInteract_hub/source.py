import trackhub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="bigInteract",
    defaultPos = 'chr3:63820967-63880091',
    short_label="bigInteract",
    long_label="bigInteract",
    genome="hg19",
    email="eva.jason@nih.gov")

track = trackhub.Track(
    name = 'bigInteract',
    tracktype = 'bigInteract',
    bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/interact/interactExample3.inter.bb',
    shortLabel = 'bigInteract',
    longLabel ='bigInteract',
    visibility = 'pack',
    spectrum = 'on',
    scoreMin = '175',
    maxHeightPixels = '300:150:20')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigInteract_hub')