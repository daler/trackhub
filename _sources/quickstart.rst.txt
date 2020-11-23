.. currentmodule:: trackhub

.. _quickstart:

Quickstart
----------
Preliminaries
~~~~~~~~~~~~~
If you've never created a track hub before, it's important to read the `track
hub help <http://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html>`_ so you
know some of the terminology.

In order to create the structure of a track hub, no data files are necessary
and no host is required -- it's simply a handful of text files on disk.
However, if you want to use the track hub as it was intended -- to browse data
-- you'll need a publicly accessible place to host files (http or ftp) and some
data. For testing small datasets, you can upload to a GitHub repository. The
example below demonstrates this.

Here, we'll set up a simple hub with 2 subtracks using data that comes with
`trackhub` to illustrate the workflow. More complicated examples can be
found in :ref:`assembly-example` and :ref:`grouping-example`.

For the impatient:

* `load the grouping example on UCSC <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/quickstart/quickstart.hub.txt&position=chr1%3A1-5000>`_
* `files in GitHub <https://github.com/daler/trackhub-demo/tree/master/quickstart>`_

Create hub components
~~~~~~~~~~~~~~~~~~~~~
A track hub consists of connected components of files that point to each other.
The hub file points to a genomes file, which points to a trackDb file, which
points to the various data tracks.

In `trackhub`, these are modeled as classes with parents and children. The hub
is the parent of the genomes file, which is the parent of the trackDb file, and
so on. In this quickstart, we use the :func:`default_hub` function to get all of
these components already connected. See :ref:`assembly-example` for connecting
them one-by-one or for more control over filenames.

.. testcode::

    import os
    import trackhub

    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="quickstart",
        genome="hg38",
        email="you@email.com")

We can indvidually print each object to see the contents of the text file that
will be created. Note that until a hub is "rendered" (see below), the files
won't actually exist.

.. testcode::

    print(hub)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    hub hub
    shortLabel quickstart
    longLabel quickstart
    genomesFile quickstart.genomes.txt
    email you@email.com

Note that we could have specified the short_label and long_label kwargs, but by
default the hub name is carried over to the shortLabel and longLabel lines.
Furthermore, the genomes.txt file's name is prefixed by the hub name.

.. testcode::

    print(genomes_file)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    genome hg38
    trackDb hg38/trackDb.txt

So far, the `trackdb` object has no tracks added:

.. testcode::

    print(trackdb)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE
    
    

Adding tracks
~~~~~~~~~~~~~

In this example, we are adding tracks one at a time. This is not much easier
than just writing the trackDb file in a text editor. However, creating tracks
in Python makes it easy to scale up to hundreds of tracks and unlocks all of
Python for configuring tracks. As one example, we could color tracks by some
aspect (sample, or treatment, for example) and rapidly make the changes across
the hub. See :ref:`grouping-example` for an example of this.

Here's how to create a single track. The most important argument is the
`source` argument, which points to the location of the track's file on disk.
Unlike the objects we made above which don't yet exist as a file, a Track
object must point to an existing file. Sometimes you might want to include
a file from a different hub in your own hub. In this case, instead of `source`,
use the `url` kwarg.

Here were are using the :func:`helpers.data_dir()` function to get the path to
the example data shipped with trackhub. In practice, these paths would be
inside your analysis directories.

First, the simplest track to add: a name, source, and type. Note that we add it
to the `trackdb` as well:

.. testcode::

    track1 = trackhub.Track(
        name="signal1",
        source=os.path.join(trackhub.helpers.data_dir(), 'sine-hg38-0.bedgraph.bw'),
        tracktype='bigWig -2 2',
    )

    trackdb.add_tracks(track1)


Next, a slightly more complex one, which changes the visibility, view height,
color, and view limits as well as sets nicer labels. See the `Track Database
Definition <https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html>`_
page for more details as well as all the other settings that are possible.

.. testcode::

    track2 = trackhub.Track(
        name='signal2',
        short_label='Signal 2',
        long_label='Signal track for sample 2',
        source=os.path.join(trackhub.helpers.data_dir(), 'sine-hg38-1.bedgraph.bw'),
        tracktype='bigWig',
        color='128,0,0',
        maxHeightPixels='8:50:128',
        viewLimits='-2:2',
        visibility='full'
    )

    trackdb.add_tracks(track2)


Now that we have added tracks to the `trackdb` object, printing it should show the updates:

.. testcode::

    print(trackdb)

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    track signal1
    bigDataUrl signal1.bigWig
    shortLabel signal1
    longLabel signal1
    type bigWig -2 2

    track signal2
    bigDataUrl signal2.bigWig
    shortLabel Signal 2
    longLabel Signal track for sample 2
    type bigWig
    color 128,0,0
    maxHeightPixels 8:50:128
    viewLimits -2:2
    visibility full

Render (stage) the hub
~~~~~~~~~~~~~~~~~~~~~~
To get ready for uploading, `trackhub` renders the hub files and symlinks all
the track source files into a local directory. This allows us to inspect the
hub before uploading.

By default the staging directory is a temporary directory, but here to be more
explicit we will set ``staging="quickstart-staging"`` 

.. testcode::

    trackhub.upload.stage_hub(hub, staging="quickstart-staging")

The `quickstart-staging` should have these contents:

.. testcode::
    :hide:

    for path, dirs, files in os.walk('quickstart-staging'):
          print(path + '/')
          for f in sorted(files):
            print('  ' + f)

.. testoutput::

    quickstart-staging/
      quickstart.genomes.txt
      quickstart.hub.txt
    quickstart-staging/hg38/
      signal1.bigWig
      signal2.bigWig
      trackDb.txt

This directory is now ready for transferring to a host to serve it. You can
either use rsync directly from the terminal (be sure to use the ``-L``
argument, which follows symlinks), or use the
:func:`trackhub.upload.upload_hub()` function.

Another workflow would be to `create a Github repo
<https://help.github.com/articles/create-a-repo/>`_, then either set the path
to the repo as the `staging` diretory, or move the contents of the staging
directory into the repo:

For example, at the command line::

    git clone https://github.com/user/repo.git
    cd repo
    rsync -L ../quickstart-staging .
    git add .
    git commit -m 'update hub'
    git push origin

