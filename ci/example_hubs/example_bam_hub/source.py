import trackhub
hub, genomes_file, genome, trackdb = trackhub.default_hub(
     hub_name="bam",
     short_label="bam",
     long_label="bam",
     genome="hg18",
     defaultPos = "chr21:33038946-33039092",
     email="eva.jason@nih.gov")

track = trackhub.Track(
     tracktype='bam',
     name="bam",
     description="bam ex. 1: 1000 genomes read alignments (individual na12878)",
     pairEndsByName=".",
     pairSearchRange='10000',
     chromosomes='chr21',
     maxWindowToDraw='200000',
     visibility='pack',
     bigDataUrl='http://genome.ucsc.edu/goldenPath/help/examples/bamExample.bam')
trackdb.add_tracks(track)
trackhub.upload.upload_hub(hub=hub, host="localhost", remote_dir="example_hubs/example_bam_hub")