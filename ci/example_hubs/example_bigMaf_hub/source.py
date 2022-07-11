import trackhub

hub, genome, genomes_file, trackdb = trackhub.default_hub(
    hub_name="bigMaf",
    short_label="bigMaf",
    long_label="bigMaf",
    genome="hg38",
    email="eva.jason@nih.gov",
)

track = trackhub.Track(
    name="bigMaf",
    frames="http://genome.ucsc.edu/goldenPath/help/examples/bigMafFrames.bb",
    bigDataUrl="http://genome.ucsc.edu/goldenPath/help/examples/bigMaf.bb",
    tracktype="bigMaf",
)
trackdb.add_tracks(track)

trackhub.upload.upload_hub(
    hub=hub, host="localhost", remote_dir="example_hubs/example_bigMaf_hub"
)
