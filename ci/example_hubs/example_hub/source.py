import glob, os
import trackhub

# First we initialize the components of a track hub

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="myhub",
    short_label='myhub',
    long_label='myhub',
    genome="hg38",
    email="ryan.dale@nih.gov")

# Next we add tracks for some bigWigs. These can be anywhere on the
# filesystem; symlinks will be made to them. Here we use some example data
# included with the trackhub package; in practice you'd point to your own
# data.

for bigwig in glob.glob('trackhub/test/data/sine-hg38-*.bw'):

    # track names can't have any spaces or special characters. Since we'll
    # be using filenames as names, and filenames have non-alphanumeric
    # characters, we use the sanitize() function to remove them.

    name = trackhub.helpers.sanitize(os.path.basename(bigwig))

    # We're keeping this relatively simple, but arguments can be
    # programmatically determined (color tracks based on sample; change scale
    # based on criteria, etc).

    track = trackhub.Track(
        name=name,          # track names can't have any spaces or special chars.
        source=bigwig,      # filename to build this track from
        visibility='full',  # shows the full signal
        color='128,0,5',    # brick red
        autoScale='on',     # allow the track to autoscale
        tracktype='bigWig', # required when making a track
    )

    # Each track is added to the trackdb

    trackdb.add_tracks(track)

# In this example we "upload" the hub locally. Files are created in the
# "example_hub" directory, along with symlinks to the tracks' data files.
# This directory can then be pushed to GitHub or rsynced to a server.

trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_hub')

# Alternatively, we could upload directly to a web server (not run in this
# example):

if 0:
    trackhub.upload.upload_hub(
        hub=hub, host='example.com', user='username',
        remote_dir='/var/www/example_hub')