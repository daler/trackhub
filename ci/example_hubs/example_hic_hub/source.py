import trackhub
hub, genomes_file, genome, trackdb = trackhub.default_hub(
     hub_name="hic",
     defaultPos= 'chr21:32000000-35000000',
     short_label="hic_example",
     long_label="hic_example",
     genome="hg19",
     email="eva.jason@nih.gov")

track = trackhub.Track(
     name = 'examplehicTrack',
     tracktype = 'hic',
     visibility = 'dense',
     url = 'http://hgdownload.soe.ucsc.edu/gbdb/hg19/bbi/hic/GSE63525_GM12878_insitu_primary+replicate_combined.hic',
     shortLabel = 'hic example',
     longLabel = 'This hic file shows in situ Hi-C data from Rao et al. (2014) on the GM12878 cell line')

trackdb.add_tracks(track)
trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_hic_hub')