import trackhub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
     hub_name='bigChain',
     short_label='bigChain',
     long_label='bigChain',
     genome='hg38',
     defaultPos = 'chr22:1-150754',
     email='eva.jason@nih.gov')

track = trackhub.Track(
     name = 'bigChain',
     bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigChain.bb',
     shortLabel = 'bigChain',
     longLabel ='bigChain Example Hub',
     tracktype = 'bigChain',
     visibility = 'pack')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_bigChain_hub')