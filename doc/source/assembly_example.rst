Assembly example
----------------

.. code-block:: python


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
    trackdb = trackhub.TrackDb()
    hub.add_genomes_file(genomes_file)
    genomes_file.add_genome(genome)
    genome.add_trackdb(trackdb)


    for bw in glob.glob(os.path.join(trackhub.helpers.data_dir(), "*no1*.bw")):
        name, _, _ = os.path.basename(bw).split(".")
        track = trackhub.Track(
            name=trackhub.helpers.sanitize(name),
            local_fn=bw,
            tracktype='bigWig',
            autoScale=True)
        trackdb.add_tracks(track)

    for bb in glob.glob(os.path.join(trackhub.helpers.data_dir(), "*no1*.bigBed")):
        name, _ = os.path.basename(bb).split(".")
        track = trackhub.Track(
            name=trackhub.helpers.sanitize(name),
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

    trackhub.upload.upload_hub(hub=hub, host='localhost',
        remote_dir='example_assembly_hub')
