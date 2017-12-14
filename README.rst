``trackhub``
============

Data visualization is critical at all steps of genomic data analysis, from QC
through final figure preparation.  A `track hub
<https://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html>`_ is a collection
of genomic data "tracks" (data files in a supported format)  along with a set
of plain-text files that determine the organization, labels, color,
configuration UI, and other details.  The files comprising a track hub are
uploaded to a server, and a genome browser (e.g., UCSC Genome Browser) is
pointed to the served URL for viewing. `Here
<http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://vizhub.wustl.edu/VizHub/RoadmapRelease3.txt>`_
is an example of a track hub created by the ENCODE project.

If you only have a handful of tracks, it is straightforward to write the
configuration files and upload the tracks manually. For larger data sets
however, this becomes tedious and error-prone. Here we introduce `trackhub`,
a Python package that enables the programmatic construction and upload of
arbitrarily complex track hubs. It has no dependencies besides Python itself
and the availability of ``rsync`` (a standard Unix command-line tool for
remotely transferring files). It is availabe on PyPI, bioconda, and GitHub; an
automated test suite and tested documentation ensure high-quality code and
help.

See :ref:`basic-example`, :ref:`grouping-example`, and :ref:`assembly-example`

Features
--------

Validation
~~~~~~~~~~
When configuring a track hub, there are many parameters to choose from, and
a typo or invalid option in one part of a hub can cause the rest to fail. To
reduce these issues at creation time, `trackhub` validates the hub options
against UCSC's documentated options and raises a Python exception if improperly
configured.


Filename handling
~~~~~~~~~~~~~~~~~
Often the directory structure used for analysis does not reflect the desired
directory structure for a track hub. To avoid the tedious process of uploading
each local file to its remote destination (which would require many separate
``rsync`` calls), `trackhub` locally symlinks all tracks and configuration files
to a temporary directory that is then uploaded to the remote host in one call to
``rsync``.  This allows local inspection of the hub for troubleshooting, and
enables rapid deployment and updating since only files that have changed will be
uploaded on subsequent calls.

Flexibility
~~~~~~~~~~~
Where possible, sensible defaults are used to minimize the effort to build
a functioning track hub. However, all parts can be configured if desired,
resulting in support for simple one-track hubs through complex composite hubs
with supertracks, views, and subtracks.

While there is an implicit hierarchy in a track hub (hub file, genomes file,
trackdb, tracks), there is no requirement for them to be created in any
particular order. This allows the user to build their hub in whatever order or
method best suits the particular use-case.


Extensible
~~~~~~~~~~
The framework provided by `trackhub` can be extended as new hub functionality is
added to the UCSC Genome Browser.


Full documentation, including a full in-depth tutorial, can be found at
https://daler.github.io/trackhub.

.. _basic-example:

Basic example
-------------

The code below is run automatically when the documentation is re-generated. The
resulting files are automatically uploaded to the GitHub repository
https://github.com/daler/trackhub-demo, and the constructed hub can be viewed
with the following link to the UCSC Genome Browser:
http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/total-refactor/example_hub/myhub.hub.txt&position=chr1%3A1-5000.
Note that the link encodes the URL to the hub in the ``hubUrl`` parameter.

.. code-block:: python

    import glob, os
    import trackhub

    # Initialize the components of a track hub
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="myhub",
        short_label='myhub',
        long_label='myhub',
        genome="hg38",
        email="dalerr@niddk.nih.gov")

    # Add a track for every bigwig found. Note that this example is executed
    # from the `doc` directory, hence the `../trackhub` path. These data are
    # included in the source repository on github.
    for bigwig in glob.glob('../trackhub/test/data/sine-hg38-*.bw'):
        name = trackhub.helpers.sanitize(os.path.basename(bigwig)),
        track = trackhub.Track(
            name=name,          # track names can't have any spaces or special chars.
            source=bigwig,      # filename to build this track from
            visibility='full',  # shows the full signal
            color='128,0,5',    # brick red
            autoScale='on',     # allow the track to autoscale
            tracktype='bigWig', # required when making a track
        )
        trackdb.add_tracks(track)

    # Add a track for everyt bigBed. Let's give them nicer labels (the
    # short_label argument).
    for i, bigbed in enumerate(glob.glob('../trackhub/test/data/random-hg38*.bigBed')):
        track = trackhub.Track(
            name=trackhub.helpers.sanitize(os.path.basename(bigbed)),
            short_label='regions{0}'.format(i),  # a nicer label
            source=bigbed,                       # filename to build this track from
            visibility='dense',                  # display in a single line
            color='0,0,255',                     # bright blue
            tracktype='bigBed',                  # required when making a track
        )
        trackdb.add_tracks(track)

    # Example of "uploading" the hub locally, to be pushed to github later.
    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hub')

    # Example uploading to a web server (not run):
    if 0:
        trackhub.upload.upload_hub(
            hub=hub, host='example.com', user='username',
            remote_dir='/var/www/example_hub')


The hub files are now at
https://github.com/daler/trackhub-demo/tree/total-refactor/example_hub. The
`raw file
<https://raw.githubusercontent.com/daler/trackhub-demo/master/example_hub/myhub.hub.txt>`_
served by GitHub can be added to the Track Hubs section of UCSC Genome Browser.

Copyright 2012-1017 Ryan Dale; BSD 2-clause license.
