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
    html_string="BIGFOOT V4 INFO\n",
    orderKey=4800
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
        autoScale=True)
    trackdb.add_tracks(track)

for bb in glob.glob("data/*.bigBed"):
    name, _ = os.path.basename(bb).split(".")
    track = trackhub.Track(
        name=name,
        local_fn=bb,
        tracktype='bigBed')
    trackdb.add_tracks(track)

example_group = trackhub.groups.GroupDefinition(
    "example_tracks",
    label="Example Tracks",
    priority=1,
    default_is_closed=False)

groups_file = trackhub.groups.GroupsFile([example_group])
for track in trackdb.children:
    track.add_params(group="example_tracks")
genome.add_groups(groups_file)

hub.render()

# upload

hub.url = "trackhub.example.org/my_example_hub.txt"
hub.remote_fn = "/www/trackhubs/my_example_hub.txt"

from trackhub.upload import upload_hub, upload_track

kwargs = dict(host='my_host', user='user')
upload_hub(hub=hub, **kwargs)
for track, level in hub.leaves(trackhub.Track):
        upload_track(track=track, **kwargs)


