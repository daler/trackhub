``trackhub``
============

Data visualization is critical at all steps of genomic data analysis, from QC
through final figure preparation.  A *track hub* is a collection of genomic data
"tracks" (data files in a supported format)  along with a set of plain-text
files that determine the organization, labels, color, configuration UI, and
other details.  The files comprising a track hub are uploaded to a server, and
a genome browser (e.g., UCSC Genome Browser) is pointed to the served URL for
viewing.

For a handful of tracks, it is straightforward to write the configuration files
and upload the tracks manually. For larger data sets however, this becomes
tedious and error-prone. Here we introduce `trackhub`, a Python package that
enables the programmatic construction and upload of arbitrarily complex track
hubs. It has no dependencies besides Python itself and the availability of
``rsync``, a standard Unix command-line tool for remotely transferring files. It
is availabe on PyPI, bioconda, and GitHub; an automated test suite and tested
documentation ensure high-quality code and help.

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
http://packages.python.org/trackhub.

The following example will build and upload a trackhub for all the bigWig files
in the current directory, coloring them based on their filenames:

.. code-block:: python

    import glob, os
    from trackhub import Track, default_hub
    from trackhub.upload import upload

    hub, genomes_file, genome, trackdb = default_hub(
        hub_name="myhub",
        genome="hg19",
        email="none@example.com")

    # Host the hub will be uploaded to
    host = 'www.example.com'
    username = 'username'

    # Upload the hub.txt to this path on the host. Other associated files will
    # be relative to this file.
    hub.remote_fn = "/var/www/data/hubs/my_example_hub.txt"

    # Upon being uploaded to the host, this is its resulting
    # publicly-accessible URL
    hub.url = "http://example.com/hubs/my_example_hub.txt"

    for bigwig in glob.glob('*.bigwig'):

        if 'mutant' in bigwig:
            color = '128,0,0'  # dark red
        else:
            color = '0,0,0'    # black

        track = Track(local_fn=bigwig, tracktype='bigWig', color=color)
        trackdb.add_tracks(track)

    upload_hub(hub=hub, host='www.example.com', user='username')


Copyright 2012-1017 Ryan Dale; BSD 2-clause license.
