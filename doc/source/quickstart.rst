.. currentmodule:: trackhub

.. _quickstart:

Quickstart
----------
Preliminaries
~~~~~~~~~~~~~

It's a good idea to read the `track hub help
<http://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html>`_ so you know
some of the terminology.

In order to create the structure of a track hub, no data files are necessary
and no host is required -- it's simply a handful of text files on disk.
However, if you want to use the track hub as it was intended -- to browse data
-- you'll need a publicly accessible place to host files (http or ftp) and some
data.

Here, we'll set up a simple hub with 2 subtracks using data that comes with
:mod:`trackhub`

In the more detailed :ref:`tutorial` you can learn how to create more
complicated track hubs -- for example, a composite hub with multiple views for
BAM alignments, bigWig signal, and bigBed called peaks.

Setup
~~~~~
First, import some classes that we'll be using:

.. testcode::

    from trackhub import Hub, GenomesFile, Genome, TrackDb, Track
    import os

Then set up the URL base.  This will completely depend on your own setup -- it's
the URL of the top-level directory where you'll be hosting your track hub.

.. testcode::

    URLBASE = 'http://example.com/mytrackhubs'
    GENOME = 'dm3'

Create hub components
~~~~~~~~~~~~~~~~~~~~~
Create a new :class:`Hub`, which will represent the top-level "hub.txt" file:

.. testcode::

    hub = Hub(
        hub='example_hub',
        short_label='example hub',
        long_label='an example hub for testing',
        email='none@example.com')

Create a new :class:`GenomesFile`, which will represent the genomes file
containing one or more multiple 2-line stanzas. We'll only be using data for
a single assembly (dm3).

.. testcode::

    genomes_file = GenomesFile()

Create a new :class:`Genome` object with the assembly name; this will represent
the stanza in the genomes file created above:

.. testcode::

    genome = Genome(GENOME)

Create a new :class:`TrackDb` object that will represent the ``trackDb.txt``
file and will eventually hold the tracks for this genome:

.. testcode::

    trackdb = TrackDb()

Create two new :class:`Track` instances.  Each instance represents a stanza in
the ``trackDb.txt`` file.  Creation of these objects in a script really pays
off -- in fact, the ability to do so is a major reason for :mod:`trackhub`'s
existence. But here, we're just creating them longhand for clarity:

.. testcode::

    track1 = Track(
        name="track1Track",
        url=os.path.join(URLBASE, GENOME, 'track1.bigBed'),
        tracktype='bigBed 3',
        short_label='track1',
        long_label='my track #1',
        # add other params here...
        color='128,0,0')

    track2 = Track(
        name="track2Track",
        url=os.path.join(URLBASE, GENOME, 'track2.bigBed'),
        tracktype='bigBed 3',
        short_label='track2',
        long_label='my track #2',
        # add other params here...
        color='0,0,255')

Connect components
~~~~~~~~~~~~~~~~~~
Now we connect them all together.  **This is an important step**, as it ties
together the objects thus far created into a defined hierarchy.

Here we start from the bottom (tracks) and hierarchically add each object to
the next object up in the hierarchy (trackDb, genome, genomes file, and finally
up to the hub):

.. testcode::

    trackdb.add_tracks([track1, track2])
    genome.add_trackdb(trackdb)
    genomes_file.add_genome(genome)
    hub.add_genomes_file(genomes_file)

Conveniently, upon connecting all the components, reasonable defaults are
initialized for filenames based on the name of the track hub and genomes
selected.  For the classes that represent files on disk (:class:`Hub`,
:class:`GenomesFile`, and :class:`TrackDb`), you can check and/or change the
:attr:`filename` attribute if you'd like.

In this case, the filenames are as follows (created in the current directory):

* hub: :file:`example_hub.hub.txt`
* genomes file: :file:`example_hub.genomes.txt`
* track db: :file:`dm3/trackDb.txt`

See :ref:`filenames` in the tutorial for more info on customizing this.

Introspection
~~~~~~~~~~~~~
Printing the objects shows the contents that will be placed into their files.
For example, the hub object:

.. doctest::

    >>> print hub
    hub example_hub
    shortLabel example hub
    longLabel an example hub for testing
    genomesFile example_hub.genomes.txt
    email none@example.com


Printing the genomes file shows all of its attached genomes, so if we were
working with multiple genomes, they would all be shown here:

.. testcode::

    print genomes_file

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    genome dm3
    trackDb dm3/trackDb.txt


The single genome we're working with; printing the genome looks similar to
printing the genomes file.


.. testcode::

    print genome

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    genome dm3
    trackDb dm3/trackDb.txt

And the trackDb file:

.. testcode::

    print trackdb

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    track track1Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track1.bigBed
    shortLabel track1
    longLabel my track #1
    type bigBed 3
    color 128,0,0

    track track2Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track2.bigBed
    shortLabel track2
    longLabel my track #2
    type bigBed 3
    color 0,0,255

Now, at this point nothing has actually been written to file (more on that in
a moment).  But first, let's make some adjustments.  For example, let's add
a visibility mode of "squish" to all the tracks in `trackdb`:

.. testcode::

    for track in trackdb.tracks:
        track.add_params(visibility='squish')


Printing the ``trackdb`` again reflects the updates:

.. testcode::

    print trackdb

.. testoutput::
    :options: +NORMALIZE_WHITESPACE

    track track1Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track1.bigBed
    shortLabel track1
    longLabel my track #1
    type bigBed 3
    visibility squish
    color 128,0,0

    track track2Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track2.bigBed
    shortLabel track2
    longLabel my track #2
    type bigBed 3
    visibility squish
    color 0,0,255


Render the hub
~~~~~~~~~~~~~~
So far, nothing has been written to file.  *Rendering* the hub refers to
actually writing the content to files, creating directories as needed.

This is done simply by calling the render method on the top-level object:

.. testcode::

    results = hub.render()

Now everything is written to disk, ready for uploading.

Where were the files written?  You can use the
:func:`helpers.show_rendered_files` function to see:

.. testcode::

    from trackhub.helpers import show_rendered_files
    show_rendered_files(results)

.. testoutput::

    rendered file: example_hub.hub.txt (created by: <trackhub.hub.Hub object at 0x...>)
    rendered file: example_hub.genomes.txt (created by: <trackhub.genomes_file.GenomesFile object at 0x...>)
    rendered file: dm3/trackDb.txt (created by: <trackhub.trackdb.TrackDb object at 0x...>)



Upload data
~~~~~~~~~~~
Assuming you have a way of getting data to a publicly accessible location, you
can upload all of the hub configuration files and data files.

This requires some extra attributes for tracks and the hub.  For example, the
tracks need a :attr:`local_fn` attribute, which provides the local path on
disk, and an :attr:`upload_fn` attribute, which may or may not be the same as
their :attr:`bigDataUrl` URL -- this would depend on where exactly you're
hosting the files and how you access them through SSH.

Since so much depends on your setup, getting the path names right is up to you!

.. note::

    The :attr:`local_fn` attribute is very important, because it's the way that
    data on disk gets connected to tracks in the track hub.  Any file on disk
    can act as the data source for a track, so it's up to you to specify the
    right data file for each track.

The :attr:`bigDataUrl` attributes for the tracks above point to the URL
:file:`http://example.com/mytrackhubs/dm3/`.  Imagine that on our local
machine, the data files for these tracks are stored in :file:`/data/bedfiles/`.
And, in order to upload them via rsync so that they are served by the host at
the bigDataUrl specified above, imagine we need to get them to
:file:`user@example.com:/var/www/data/mytrackhubs/dm3`, with rsync over SSH.

Given this scenario, here's how we would set up the local and remote filenames:

.. testcode::

    local_dir = '/data/bedfiles'
    upload_dir = '/var/www/data/mytrackhubs'
    user = 'user'
    host = 'example.com'

    # hub already has a default local_fn (hub.filename)
    hub.upload_fn = os.path.join(upload_dir, os.path.basename(hub.local_fn))

    for track in trackdb.tracks:
        basename = os.path.basename(track.url)
        track.local_fn = os.path.join(local_dir, basename)
        track.remote_fn = os.path.join(upload_dir, basename)

(note: it's possible to simplify this even more by allowing default remote
names to be used; here we're being more explicit about local and remote
filenames)

And then upload (via rsync).  This creates directories as necessary, and only
uploads files that have differences compared to the server::

    from trackhub.upload import upload_track, upload_hub

    for track in trackdb.tracks:
        upload_track(track=track, host=host, user=user)

    upload_hub(hub=hub, host=host, user=user)

Now you can paste the hub URL -- :attr:`Hub.url` -- in the UCSC Genome Browser
to view the hub.

Continue on to the :ref:`tutorial` for a more in-depth look at :mod:`trackhub`.
