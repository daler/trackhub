import trackhub
import re
import sys
import os
import glob

hub = trackhub.Hub(
    "assembly_hub",
    short_label="assembly_hub",
    long_label="an example of an assembly hub",
    email="none@example.com")

genome = trackhub.Assembly(
    genome="newOrg1",
    twobit_file=os.path.join(trackhub.helpers.data_dir(), "newOrg1.2bit"),
    organism="Big Foot",
    defaultPos="chr1:0-1000000",
    scientificName="Biggus Footus",
    description="BigFoot V4",
    html_string="BIGFOOT V4 INFO\n",
    orderKey=4800
)

genomes_file = trackhub.GenomesFile()
genomes_file.add_genome(genome)
trackdb = trackhub.TrackDb()
hub.add_genomes_file(genomes_file)

genomes_file.add_genome(genome)
genome.add_trackdb(trackdb)

for bw in glob.glob(os.path.join(trackhub.helpers.data_dir(), "*no1*.bw")):
    name, _, _ = os.path.basename(bw).split(".")
    track = trackhub.Track(
        name=trackhub.helpers.sanitize(name),
        source=bw,
        tracktype='bigWig',
        autoScale="on")
    trackdb.add_tracks(track)

trackhub.upload.stage_hub(hub)

