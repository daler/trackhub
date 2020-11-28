trackhub
========

.. image:: https://github.com/daler/trackhub/workflows/main/badge.svg
    :target: https://github.com/daler/trackhub/actions?query=workflow%3Amain

See the documentation at https://daler.github.io/trackhub for more details.

Data visualization is critical at all steps of genomic data analysis, from QC
through final figure preparation.  A `track hub
<https://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html>`_ is way of
organizing large numbers of of genomic data "tracks" (data files in a supported
format), configured with a set of plain-text files that determine the
organization, UI, labels, color, and other details. The files comprising
a track hub are uploaded to a server, and a genome browser (e.g., UCSC Genome
Browser) is pointed to the served URL for viewing. For example, `here
<http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://vizhub.wustl.edu/VizHub/RoadmapRelease3.txt>`_
is a track hub created by the ENCODE project. It is straightforward to write
the configuration files and upload the tracks manually if you have a small
number of tracks. For larger data sets however, this becomes tedious and
error-prone.

`trackhub` is a Python package that enables the programmatic construction and
upload of arbitrarily complex track hubs. It has no dependencies besides Python
itself, the common Python package `docutils`, and the availability of ``rsync``
(a standard Unix command-line tool for remotely transferring files). It is
availabe on PyPI, bioconda, and GitHub; an automated test suite and tested
documentation ensure high-quality code and help.

Installation
------------

Using pip: ``pip install trackhub``

Using `bioconda <https://bioconda.github.io>`_: ``conda install trackhub``

Features
--------

Validation
~~~~~~~~~~
`trackhub` validates parameters against UCSC's documented options, so errors
are caught early and less time is spent debugging in the Genome Browser.

Filename handling
~~~~~~~~~~~~~~~~~
The directory structure of an analysis rarely matches the organization you want
for a track hub.  `trackhub` symlinks track files to a staging area so the hub
can be inspected locally before being uploaded, e.g., with ``rsync``. Staging
also enables rapid deployment and updating since only files that have changed
will be uploaded on subsequent calls.

Flexibility
~~~~~~~~~~~
Sensible defaults make it easy to build a functioning track hub. However, these
defaults can always be overridden for complex configurations or when more
precise control is needed. For example, by default a track's `name` also
becomes the `shortLabel`, `longLabel` and `filename` of the track in the hub
unless any of these are overridden by the user.

Easy track documentation
~~~~~~~~~~~~~~~~~~~~~~~~
Write track hub documentation in ReStructured Text, and it is converted to
HTML, connected to the track and uploaded with the rest of the hub. This allows
for programmatically including content without the tedium of writing HTML by
hand.

Extensible
~~~~~~~~~~
The framework provided by `trackhub` can be extended as new hub functionality is
added to the UCSC Genome Browser.

Full documentation can be found at https://daler.github.io/trackhub. The code
in the documentation is run as part of the test suite to guarantee correctness.

.. _basic-example:

Basic example
-------------
The following code demonstrates a track hub built out of all bigWig files found
in a directory. It is relatively simple; see these other examples from the
documentation for complex usage.

This basic example is run automatically when the documentation is re-generated.
You can view the uploaded files in the `trackhub-demo
<https://github.com/daler/trackhub-demo>`_ GitHub repository, and `load the hub
<http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_hub/myhub.hub.txt&position=chr1%3A1-5000>`_
directly into UCSC to see what it looks like.

.. code-block:: python

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


Copyright 2012-2020 Ryan Dale; MIT license.
