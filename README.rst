``trackhub``
============

``trackhub`` is a Python package for handling the creation and uploading of
track hubs for the UCSC Genome Browser (see
http://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html for more info)

Some reasons for using ``trackhub`` to manage your track hubs:

* `filename handling`: automatic (yet still completely configurable, if needed)
  handling of filenames and directory structure
* `uploading`: upload a full hub -- hub/genomes/trackdb files, plus all data
  files (bam/bigWig/bigBed) -- via rsync over ssh
* `validation`: mechanisms for handling validation of parameters so errors are
  [hopefully] caught prior to uploading
* `rapid deployment`: mapping local filenames to remote filenames on the host enables
  rapid updating of the hub with new or updated data (e.g., when analysis
  parameters change)
* `flexibility`: support for simple hubs up through complex composite hubs with
  views and subtracks
* `extensible`: provides a framework for working with hub components, allowing
  new functionality to be easily added


Full documentation, including a full in-depth tutorial, can be found at
http://packages.python.org/trackhub.

Here's an example of creating a hub, and uploading the hub and files to
a remote server.  This hub will show all the bigWig files in the current
directory, and any of them that have "control" in the filename will be colored
gray in the hub

.. code-block:: python

    from trackhub imoprt Track, default_hub
    from trackhub.upload import upload_hub, upload_track

    hub, genomes_file, genome, trackdb = default_hub(
        hub_name="myhub",
        genome="hg19",
        short_label="example hub",
        long_label="My example hub",
        email="none@example.com")

    # publicly accessible hub URL
    hub.url = "http://example.com/hubs/my_example_hub.txt"

    # hub's location on remote host, for use with rsync
    hub.remote_fn = "/var/www/data/hubs/my_example_hub.txt"

    # Make tracks for all bigWigs in current dir
    import glob, os
    for fn in glob.glob('*.bigwig'):
        label = fn.replace('.bigwig', '')

        # Parameters are checked for valid values, see 
        # http://genome.ucsc.edu/goldenPath/help/trackDb/trackDbHub.html
        # for what's available
        track = Track(
            name=label,
            short_label=label,
            long_label=label,
            autoScale='off',
            local_fn=fn,
            tracktype='bigWig',
            )
        trackdb.add_tracks(track)

    # Demonstrate some post-creation adjustments...here, just make control
    # samples gray
    for track in trackdb.tracks:
        if 'control' in track.name:
            track.add_params(color="100,100,100")

    # Render the hub to text files
    hub.render()

    # Upload the hub files and all the bigwig files using rsync.
    kwargs = dict(host='www.example.com', user='me')
    upload_hub(hub=hub, **kwargs)
    for track, level in hub.leaves(Track):
        upload_track(track=track, **kwargs)


**Note:** ``trackhub`` is still under active development and should be considered an
alpha version.  Please open an issue on github
(https://github.com/daler/trackhub/issues) if you run into problems.




Copyright 2012 Ryan Dale; BSD 2-clause license.
