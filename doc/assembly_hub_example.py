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
    twobit_file="data/newOrg1.2bit",
    organism="Big Foot",
    defaultPos="chr1:0-1000000",
    scientificName="Biggus Footus",
    description="BigFoot V4",
    # htmlPath="newOrg1/description.html", # this should work like twobit_file
    orderKey=4800 # minimal example
)

genomes_file = trackhub.GenomesFile()
trackdb = trackhub.TrackDb()
hub.add_genomes_file(genomes_file)
genomes_file.add_genome(genome)
genome.add_trackdb(trackdb)

str(genome)

for bw in glob.glob("data/*.bw"):
    name, _, _ = os.path.basename(bw).split(".")
    track = trackhub.Track(
        name=name,
        local_fn=bw,
        tracktype='bigWig',
        group="example_tracks",
        autoScale=True)
    trackdb.add_tracks(track)

for bb in glob.glob("data/*.bigBed"):
    name, _ = os.path.basename(bb).split(".")
    track = trackhub.Track(
        name=name,
        local_fn=bb,
        tracktype='bigBed',
        group="example_tracks")
    trackdb.add_tracks(track)

example_group = trackhub.groups.GroupDefinition(
    "example_tracks",
    label="Example Tracks",
    priority=1,
    default_is_closed=False)

groups_file = trackhub.groups.GroupsFile([example_group])

genome.add_groups(groups_file)

hub.render()

# upload

hub.url = "http://trackhub.genereg.net/example/my_example_hub.txt"
hub.remote_fn = "/mnt/storage/www/ucsc_hub/example/my_example_hub.txt"

from trackhub.upload import upload_hub, upload_track

kwargs = dict(host='shire', user='malcolm')
upload_hub(hub=hub, **kwargs)
for track, level in hub.leaves(trackhub.Track):
        upload_track(track=track, **kwargs)


