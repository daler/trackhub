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

Example
-------

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

    # Add a track for every bigwig found
    for bigwig in glob.glob('../trackhub/test/data/sine-hg38-*.bw'):
        track = trackhub.Track(
            name=trackhub.helpers.sanitize(os.path.basename(bigwig)),
            source=bigwig,
            visibility='full',
            color='128,0,5',
            autoScale='on',
            tracktype='bigWig',
        )
        trackdb.add_tracks(track)

    # add tracks for bigBed. Let's give them integer labels
    for i, bigbed in enumerate(glob.glob('../trackhub/test/data/random-hg38*.bigBed')):
        track = trackhub.Track(
            name=trackhub.helpers.sanitize(os.path.basename(bigbed)),
            short_label='regions{0}'.format(i),
            source=bigbed,
            visibility='dense',
            color='0,0,255',
            tracktype='bigBed',
        )
        trackdb.add_tracks(track)


    # Example of "uploading" the hub locally, to be pushed to github later:
    trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hub')

    # Example uploading to a web server (not run):
    if 0:
        trackhub.upload.upload_hub(
            hub=hub, host='example.com', user='username',
            remote_dir='/var/www/example_hub')


The above code is run automatically when the documentation is re-generated. The
resulting files are automatically uploaded to the GitHub repository
https://github.com/daler/trackhub-demo, and the built hub can be viewed with
the following link to the UCSC Genome Browser:
http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/total-refactor/example_hub/myhub.hub.txt&position=chr1%3A1-5000.
Note that the link encodes the ``hubUrl`` URL.

Copyright 2012-1017 Ryan Dale; BSD 2-clause license.
