.. currentmodule:: trackhub

.. _tutorial:

Tutorial
========
This tutorial is a more detailed tour through :mod:`trackhub`.  The goal here
will be to build a track hub with a composite track containing two views (for
bigWig signals and bigBed peaks from an imaginary ChIP-seq experiment) along
with subsetting and selection tools like a matrix to determine peak caller and
cell type.

Prerequisites
-------------
It's assumed you know a fair bit about track hubs in general and Python in
general.

This tutorial uses data that ships with :mod:`trackhub`, so you can play around
without actually having any data of your own....

Setup
-----
The example data we're working with consists of two bigWig files that contains
some modified sine waves.  The only difference is in the frequency of the sine
wave:

    * ``sine-dm3-1000.bedgraph.bw`` -- low frequency, in cell type "a"
    * ``sine-dm3-10000.bedgraph.bw`` -- high frequency, in cell type "b"

and some random peaks with different feature sizes:

    * ``random-dm3-0.bigBed`` -- random features, each 1kb, in cell type "a"
    * ``random-dm3-1.bigBed`` -- random features, each 10kb, in cell type "a"
    * ``random-dm3-2.bigBed`` -- random features, each 100kb, in cell type "b"

Note the different cell types, too.  The goal here is to have an example data
set that is complex enough to reflect real-world cases without being
burdernsome.


Make a :class:`Hub`, :class:`GenomesFile`, and :class:`Genome`
--------------------------------------------------------------
Recall that the hierarchy of a track hub is something like this::

    HUB.TXT

        GENOMES.TXT
        (contains stanzas that point to a trackDb.txt file for each genome)

            TRACKDB.TXT
            (contains details about all the tracks)


So we need:

* a :class:`Hub` object (representing ``HUB.TXT`` above)
* a :class:`GenomesFile` object (representing ``GENOMES.TXT`` above)
* an intermediate :class:`Genome` object that represents stanzas in the genomes
  file.
* a :class:`TrackDb` object (representing ``TRACKDB.TXT`` above

Easy enough:

.. testcode::

    # import the components we'll be using
    from trackhub import Hub, GenomesFile, Genome, TrackDb

    hub = Hub(
        hub='example_hub',
        short_label='example hub',
        long_label='an example hub for testing',
        email='none@example.com')

    genomes_file = GenomesFile()
    genome = Genome('dm3')
    trackdb = TrackDb()

.. _connecting-the-components:

Connecting the components
-------------------------
Now we need to connect them together.  Importantly, we can connect things from
the bottom-up or from the top-down, or even a mix of the two.  It doesn't
really matter, whatever fits your brain better.

The "bottom-up" approach (which, by the way, would actually need all the tracks
to be truly bottom-up, and add them to trackdb first) would look something like
this:

.. testcode::

    hub = Hub(
        hub='example_hub',
        short_label='example hub',
        long_label='an example hub for testing',
        email='none@example.com')
    genomes_file = GenomesFile()
    genome = Genome('dm3')
    trackdb = TrackDb()

    # Bottom-up
    genome.add_trackdb(trackdb)
    genomes_file.add_genome(genome)
    hub.add_genomes_file(genomes_file)

Check to see that the trackDb made it to the hub:

.. testcode::

    assert trackdb is hub.genomes_file.genomes[0].trackdb


Here's the top-down way (again re-creating the components from scratch to make
a good test case):

.. testcode::

    hub = Hub(
        hub='example_hub',
        short_label='example hub',
        long_label='an example hub for testing',
        email='none@example.com')
    genomes_file = GenomesFile()
    genome = Genome('dm3')
    trackdb = TrackDb()

    # Top-down
    hub.add_genomes_file(genomes_file)
    genome.add_trackdb(trackdb)
    genomes_file.add_genome(genome)

Do the same check:

.. testcode::

    assert trackdb is hub.genomes_file.genomes[0].trackdb

There is also a convenience function to set up a connected set of hub components:

.. testcode::

    from trackhub import default_hub
    hub, genomes_file, genome, trackdb = default_hub(
        hub_name='example_hub',
        short_label='example hub',
        long_label='an example hub for testing',
        email='none@example.com',
        genome='dm3')


Now we need to create objects representing stanzas in the :class:`TrackDb`
object, which makes up the bulk of the rest of the tutorial....

Grouping Tracks in supertracks
______________________________
Before we get into more complicated grouping structure of tracks,
lets discuss supertracks::

    SUPERTRACK STANZA
    - Defines a group of tracks to vizualize as a block
    - Doesn't contain any params like a track, including
       bigDataUlr

    TRACK A STANZA
    - Defines params for this track, including bigDataUrl
    - Refers to supertrack as parent, can have different
       type than other track stanzas

    TRACK B STANZA
    - Defines params for this track, including bigDataUrl
    - Refers to supertrack as parent, can have different
      type than other track stanzas

A supertrack acts as a container level to group tracks that should
be visualized together. Connections between supertracks and tracks
will be created in much the same way as adding a ``track`` to
the parent ``trackdb`` -- for example,
``supertrack.add_track(track)`` to add the child ``track`` to the 
parent ``supertrack``.

Creating a supertrack
_____________________
So lets create a supertrack:

.. testcode::
    
    from trackhub import SuperTrack

    supertrack = SuperTrack(
        name="supertrack",
        short_label="my super",
        long_label="An example supertrack")

    #make sure it looks OK
    print supertrack

.. testoutput::
    :options: +REPORT_NDIFF

    track supertrack
    shortLabel my super
    longLabel An example supertrack
    superTrack on

After the supertrack has been created, we can incrementally
add additional tracks.

Create two new :class:`Track` instances and add them to the ``supertrack``. 
Each instance represents a stanza in the ``supertrack``: 

.. testcode::
    
    from trackhub import Track
    import os

    URLBASE = 'http://example.com/mytrackhubs'
    GENOME = 'dm3'

    track1 = Track(
        name="track1Track",
        url=os.path.join(URLBASE, GENOME, 'track1.bigWig'),
        tracktype='bigWig 0 1000',
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
        color='128,0,0')

    supertrack.add_track(track1)
    supertrack.add_track(track2)

    #make sure it looks OK
    print supertrack

.. testoutput::
    :options: +REPORT_NDIFF

    track supertrack
    shortLabel my super
    longLabel An example supertrack
    superTrack on

    track track1Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track1.bigWig
    shortLabel track1
    longLabel my track #1
    type bigWig 0 1000
    color 128,0,0
    parent supertrack

    track track2Track
    bigDataUrl http://example.com/mytrackhubs/dm3/track2.bigBed
    shortLabel track2
    longLabel my track #2
    type bigBed 3
    color 128,0,0
    parent supertrack

Note that children stanzas of a ``supertrack`` are not indented
further, like we will see for composites, to allow
for easier readability. Next onto composites, views and subtracks.


General structure of composites, views, and subtracks
-----------------------------------------------------
OK, we're about to get into the somewhat complicated stuff. So it may be
helpful to recall the structure of a hypothetical ``trackDb.txt`` file that
contains a composite, some views, and some subtracks::

    COMPOSITE TRACK STANZA
    - defines top-level params

        VIEW TRACK 1 STANZA
        - defines params for this kind of view -- e.g., bigWig params for
          a bigWig view
        - Refers to the composite track as parent

            SUBTRACK A STANZA
            - Defines params for this track, including bigDataUrl
            - Refers to view track as parent, so this subtrack is probably
              refers to a bigWig file

        VIEW TRACK 2 STANZA
            - Another view track with different settings than the one above,
              say, bigBed params

            SUBTRACK B STANZA
            - Refers to view track #2 as parent, so this subtrack probably
              refers to a bigBed

Recall that the hub, genomes file, and genome objects make up different levels
of a hierarchy.  In the previous section, we used the ``add_<something>()``
methods to add a child to a parent -- for example,
``genome.add_trackdb(trackdb)`` to add the child ``trackdb`` to the parent
``genome``.

Connections between composite tracks, view tracks, and subtracks
will be created in much the same way -- for example,
``composite.add_view(view)`` to add the child ``view`` to the parent ``composite`` track.

Creating a composite track
--------------------------
So let's create a composite track:

.. testcode::

    from trackhub import CompositeTrack

    composite = CompositeTrack(
        name="mycomposite",
        short_label="my composite",
        long_label="An example composite track",
        tracktype="bigWig")

    # make sure it looks OK
    print composite

.. testoutput::
    :options: +REPORT_NDIFF

    track mycomposite
    shortLabel my composite
    longLabel An example composite track
    type bigWig
    compositeTrack on

After the composite track has been created, we can incrementally add additional
parameters.  This is same method can be used for all classes derived from
:class:`Track` -- :class:`CompositeTrack`, :class:`ViewTrack` and of course
:class:`Track` itself:

.. testcode::

    composite.add_params(dragAndDrop='subtracks', visibility='full')

    print composite

.. testoutput::
    :options: +REPORT_NDIFF

    track mycomposite
    shortLabel my composite
    longLabel An example composite track
    type bigWig
    visibility full
    dragAndDrop subtracks
    compositeTrack on

.. note::

    **Parameter handling**

    Parameters for all subclasses of :class:`Track` -- which includes
    :class:`CompositeTrack` and :class:`ViewTrack` --  are checked against known
    supported values in the UCSC Genome Browser.  Trying to add an unknown
    parameter results in a :class:`ParameterError`:

    .. testcode::

        composite.add_params(not_a_param=5)

    .. testoutput::

        Traceback (most recent call last):
            ...
        ParameterError: "not_a_param" is not a valid parameter for CompositeTrack

    Parameters are also checked for validity.  There's a lot more than just floats,
    ints, and strings -- for example the ``color`` parameter needs to be
    a comma-separated list of 3 ints between 0-255.

    .. testcode::

        # Try adding the wrong kind of parameter and get a ValidationError
        composite.add_params(color='red')

    .. testoutput::

        Traceback (most recent call last):
            ...
        ValidationError: no commas in RGB tuple; an example value is: "128,0,255"


Subgroups
---------
Composite tracks use the concept of subgroups to slice-and-dice tracks
according to various definitions.  In :mod:`trackhub`, you create these via
:class:`SubGroupDefinition` objects.

Each :class:`SubGroupDefinition` specifies:

* a name (a short tag for the subgroup that will be referred to later by
  tracks)
* a label (a longer description that will show up in various places in the hub)
* a mapping.

A mapping is simply a dictionary where each key is a short tag that will be
referred to later by subtracks, and each value is the corresponding label for
that tag.

For example, in the final rendered files, the composite track will have a line
like this, defining the "frequency" group (I added some annotations below the
line)::

    subGroup3 frequency Frequency lo=Low     hi=High
    #            ^          ^     key1=val1  key2=val2
    #           name      label   ^---- mapping -----^

And the tracks will add themselves to the appropriate category of the
"frequency" group with a line like::

    subGroups frequency=lo
    #             ^     ^
    #            name   one of the keys from the mapping


Here's how to set it up in :mod:`trackhub`.  Let's make a "frequency" group as
well as a "feature size" group to categorize the bed files and a "cell type"
group for further subsetting:

.. testcode::

    from trackhub.track import SubGroupDefinition
    subgroups = [

        SubGroupDefinition(
            name="frequency",
            label="Frequency",
            mapping=dict(lo="Low", hi="High")),

        SubGroupDefinition(
            name="size",
            label="Feature_size",
            mapping=dict(small="Small", med="Medium", lg="Large")),

        SubGroupDefinition(
            name="celltype",
            label="Cell_Type",
            mapping=dict(a="CelltypeA", b="CelltypeB")),

    ]

Verify that the subgroups look OK:

.. testcode::

    for sg in subgroups:
        print sg

.. testoutput::
    :options: +REPORT_NDIFF

    frequency Frequency lo=Low hi=High
    size Feature_size small=Small lg=Large med=Medium
    celltype Cell_Type a=CelltypeA b=CelltypeB

Note that they don't yet have the ``subGroupN`` prefix -- that's because these
prefixes aren't added until the TrackDb object is ready to print, since
additional handling has to take place (like inserting a special Views subgroup
as subGroup1 if needed).

Now that we have some subgroups for this composite track, let's add them:

.. testcode::

    composite.add_subgroups(subgroups)

Creating :class:`ViewTrack` objects
-----------------------------------
The next part of the hierarchy is a :class:`ViewTrack` object.  Both
:class:`ViewTrack` and :class:`CompositeTrack` are subclasses of the more
generic :class:`Track` class, so they act in much the same way.  This should
look familiar, but a notable difference is the addition of the `view` kwarg:

.. testcode::

    from trackhub import ViewTrack

    bed_view = ViewTrack(
        name="bedViewTrack",
        view="Bed",
        visibility="squish",
        tracktype="bigBed 3",
        short_label="beds",
        long_label="Beds")

    signal_view = ViewTrack(
        name="signalViewTrack",
        view="Signal",
        visibility="full",
        tracktype="bigWig 0 10000",
        short_label="signal",
        long_label="Signal")

Add these new view tracks to ``composite``:

.. testcode::

    composite.add_view(bed_view)
    composite.add_view(signal_view)


Now when we print ``composite``, it has the views added to it (nicely
indented, too):

.. testcode::

    # after adding the views
    print composite

.. testoutput::
    :options: +REPORT_NDIFF

    track mycomposite
    shortLabel my composite
    longLabel An example composite track
    type bigWig
    visibility full
    dragAndDrop subtracks
    subGroup1 view Views Signal=Signal Bed=Bed
    subGroup2 frequency Frequency lo=Low hi=High
    subGroup3 celltype Cell_Type a=CelltypeA b=CelltypeB
    subGroup4 size Feature_size small=Small lg=Large med=Medium
    compositeTrack on

        track bedViewTrack
        shortLabel beds
        longLabel Beds
        type bigBed 3
        visibility squish
        parent mycomposite
        view Bed

        track signalViewTrack
        shortLabel signal
        longLabel Signal
        type bigWig 0 10000
        visibility full
        parent mycomposite
        view Signal


We can make changes to the created views without having to add them again to
the composite.  For example, here we add ``configureable on`` to each view and
print ``composite`` to make sure the changes show up:

.. testcode::

    for view in composite.views:
        view.add_params(configurable="on")

    # after changing params
    print composite

.. testoutput::
    :options: +REPORT_NDIFF

    track mycomposite
    shortLabel my composite
    longLabel An example composite track
    type bigWig
    visibility full
    dragAndDrop subtracks
    subGroup1 view Views Signal=Signal Bed=Bed
    subGroup2 frequency Frequency lo=Low hi=High
    subGroup3 celltype Cell_Type a=CelltypeA b=CelltypeB
    subGroup4 size Feature_size small=Small lg=Large med=Medium
    compositeTrack on

        track bedViewTrack
        shortLabel beds
        longLabel Beds
        type bigBed 3
        visibility squish
        configurable on
        parent mycomposite
        view Bed

        track signalViewTrack
        shortLabel signal
        longLabel Signal
        type bigWig 0 10000
        visibility full
        configurable on
        parent mycomposite
        view Signal

And then make all bigBed tracks non-configurable and change visibility to dense
. . .

.. testcode::

    for view in composite.views:
        if 'bigBed' in view.tracktype:
            view.remove_params('configurable')
            view.add_params(visibility='dense')

. . . you get the idea.  It's convenient to have programmatic access to the hub
components.  Next, on to the tracks.

Creating :class:`Track` objects
-------------------------------
We could add the track params one-by-one, similar to how we created the hub,
composite track, and view tracks . . . but we might as well edit the
trackDb.txt by hand.  The goal here will be to provide a flavor for how you
might go about adding many tracks with custom parameters, even though here
we're only working on a relatively simple set of of 2 bigWigs and 3 bigBeds.

First, let's get the example data to work with.  In practice you would get
these via ``glob`` or ``os.listdir`` or more complicated things depending on
your use case.

Here, we'll just grab some files that come with :mod:`trackhub`, saving the
filenames of the bigBed files in ``bbs`` and the bigWig filenames in ``bws``:

.. testcode::

    from trackhub import helpers
    bbs = helpers.example_bigbeds()
    bws = helpers.example_bigwigs()

Recall we're working with the following files. Note the numbers embedded in
the filenames; we'll be using them in a moment:

    * ``sine-dm3-1000.bedgraph.bw`` (low-frequency bigWig)
    * ``sine-dm3-10000.bedgraph.bw`` (high-frequency bigWig)
    * ``random-dm3-0.bigBed`` -- (random features bigBed, each 1kb)
    * ``random-dm3-1.bigBed`` -- random features bigBed, each 10kb
    * ``random-dm3-2.bigBed`` -- random features bigBed, each 100kb

Also recall we created these subgroups:

.. testcode::

    # print the subgroups as a reminder
    for sg in subgroups:
        print sg.name, sg.mapping

.. testoutput::

    frequency {'lo': 'Low', 'hi': 'High'}
    size {'small': 'Small', 'lg': 'Large', 'med': 'Medium'}
    celltype {'a': 'CelltypeA', 'b': 'CelltypeB'}


The numbers from the filenames will be extracted in a moment.  But first, let's
set up some dictionaries to map the number in the filename to various
parameters for the tracks.  Here, we map the filename numbers to the
"frequency" subgroup, and arbitrarily make the low freq file to be "CelltypeA":

.. testcode::

    bw_p = {'1000': 'lo',   '10000': 'hi'}
    bw_c = {'1000': 'a',    '10000': 'b'}

For the bigBeds, let's map the numbers (0, 1, 2) in the filenames to the
"size" subgroup.  Let's also abritrarily make the first two bigBeds from
"CelltypeA" and the last one from "CelltypeB":

.. testcode::

    bb_s = {'0': 'small', '1': 'med', '2': 'lg'}
    bb_c = {'0': 'a',     '1': 'a',   '2': 'b'}

One more thing: it's easiest to add the ``remote_fn``, ``local_fn``, and
``url`` attributes now, while we're handling tracks iteratively.  To do so, we
need to configure some values -- you'll need to edit these to match your own
situtation or else they won't work when you try to upload them later on.

In this example, the files will have bigDataUrls that start with ``url_base``,
so that will be the publicly accessibly location.  However, in order to get
them there, the files have to be transferred to the host to the path indicated
in ``upload_base``:

.. testcode::

    # edit these to reflect where your data will be hosted
    url_base = 'http://example.com/trackhubs/dm3/'
    upload_base = '/var/www/data/dm3/'

Now we make :class:`Track` objects for each of the bigBeds and each of the
bigWigs.  Numbers from filenames are extracted, subgroups are assigned
according to the mappings we created above, and each track is added to the
appropriate :class:`ViewTrack` we've already constructed:

.. testcode::

    import os
    from trackhub import Track

    # A quick function to return the number in the middle of filenames -- this
    # will become the key into the subgroup dictionaries above
    def num_from_fn(fn):
        return os.path.basename(fn).split('.')[0].split('-')[-1]

    # Make the bigBed tracks
    for bb in sorted(bbs):
        num = num_from_fn(bb)
        basename = os.path.basename(bb)
        track = Track(
            name='features%s' % num,
            tracktype='bigBed 3',
            url=url_base + basename,
            local_fn=bb,
            remote_fn=upload_base + basename,
            shortLabel='features %s' % num,
            longLabel='features %s' % num,
            subgroups=dict(
                size=bb_s[num],
                celltype=bb_c[num]))

        # add this track to the bed view
        bed_view.add_tracks(track)

    # Make the bigWig tracks
    for bw in sorted(bws):
        num = num_from_fn(bw)
        basename = os.path.basename(bw)
        track = Track(
            name='signal%s' % num,
            tracktype='bigWig 0 ' + num,
            url=url_base + basename,
            local_fn=bw,
            remote_fn=upload_base + basename,
            shortLabel='signal %s' % num,
            longLabel='signal %s' % num,
            subgroups=dict(
                frequency=bw_p[num],
                celltype=bw_c[num]))

        # add this track to the signal view
        signal_view.add_tracks(track)

Now print the track db:

.. doctest::

    print trackdb

Oops! We forgot to add the composite to the trackdb.  So even though we made
the connections earlier (hub -> genomes file -> genome -> trackdb), the trackdb
never got anything added to it.  This is a one-line remedy...

.. testcode::

    trackdb.add_tracks(composite)

...and since we've already added the tracks to the views, and the views to the
composite, adding the composite to the trackdb like that makes the final
connection, allowing us to print *everything*:

.. testcode::

    print trackdb

.. testoutput::
    :options: +NORMALIZE_WHITESPACE +REPORT_NDIFF

    track mycomposite
    shortLabel my composite
    longLabel An example composite track
    type bigWig
    visibility full
    dragAndDrop subtracks
    subGroup1 view Views Signal=Signal Bed=Bed
    subGroup2 frequency Frequency lo=Low hi=High
    subGroup3 celltype Cell_Type a=CelltypeA b=CelltypeB
    subGroup4 size Feature_size small=Small lg=Large med=Medium
    compositeTrack on

        track bedViewTrack
        shortLabel beds
        longLabel Beds
        type bigBed 3
        visibility dense
        parent mycomposite
        view Bed

                track features0
                bigDataUrl http://example.com/trackhubs/dm3/random-dm3-0.bigBed
                shortLabel features 0
                longLabel features 0
                type bigBed 3
                subGroups view=Bed celltype=a size=small
                parent bedViewTrack

                track features1
                bigDataUrl http://example.com/trackhubs/dm3/random-dm3-1.bigBed
                shortLabel features 1
                longLabel features 1
                type bigBed 3
                subGroups view=Bed celltype=a size=med
                parent bedViewTrack

                track features2
                bigDataUrl http://example.com/trackhubs/dm3/random-dm3-2.bigBed
                shortLabel features 2
                longLabel features 2
                type bigBed 3
                subGroups view=Bed celltype=b size=lg
                parent bedViewTrack

        track signalViewTrack
        shortLabel signal
        longLabel Signal
        type bigWig 0 10000
        visibility full
        configurable on
        parent mycomposite
        view Signal

                track signal1000
                bigDataUrl http://example.com/trackhubs/dm3/sine-dm3-1000.bedgraph.bw
                shortLabel signal 1000
                longLabel signal 1000
                type bigWig 0 1000
                subGroups frequency=lo celltype=a view=Signal
                parent signalViewTrack

                track signal10000
                bigDataUrl http://example.com/trackhubs/dm3/sine-dm3-10000.bedgraph.bw
                shortLabel signal 10000
                longLabel signal 10000
                type bigWig 0 10000
                subGroups frequency=hi celltype=b view=Signal
                parent signalViewTrack

Now that we have a nice structure here, it's possible to make all kinds of
changes and tweaks to the tracks with minimal effort.  For example, this will
set default view limits of all bigWigs in the hub:

.. testcode::

    for track in signal_view.subtracks:
        track.add_params(viewLimits='0:3', autoScale='off')


Track hub filenames
-------------------
We're about to render the hub components to file; you can jump right to
:ref:`render_tut` if you'd like.  This section is an explanation of how
filenames are chosen by default, how to change them, and what the consequences
are of changing the filenames.

With only one genome here, there are only 3 files to create:  the hub file, the
genomes file, and the trackdb file, but in general the number of files will be
``1 + genomes * 2``.  :mod:`trackhub` handles the creation of the files on
disk, and its behavior is fully described in the :ref:`filenames` section.
Here it's probably easier to see this as an example.

For the example we've been working on, the default values are:

.. testcode::

    print hub.local_fn
    print genomes_file.local_fn
    print trackdb.local_fn

.. testoutput::

    example_hub.hub.txt
    example_hub.genomes.txt
    dm3/trackDb.txt

Note that these files are all in the current directory. To put all the files in
another directory, all we need to do is change the hub filename and the rest
will follow:

.. testcode::

    hub.local_fn = '/data/myhubs/hub.txt'

    print hub.local_fn
    print genomes_file.local_fn
    print trackdb.local_fn

.. testoutput::

    /data/myhubs/hub.txt
    /data/myhubs/example_hub.genomes.txt
    /data/myhubs/dm3/trackDb.txt

Reset to defaults by setting the filename to None:

.. testcode::

    hub.local_fn = None
    print hub.local_fn
    print genomes_file.local_fn
    print trackdb.local_fn

.. testoutput::

    example_hub.hub.txt
    example_hub.genomes.txt
    dm3/trackDb.txt


.. _render_tut:

Render
------
After setting up the filenames (or leaving them as their defaults), simply
render the entire hub:

.. testcode::

    results = hub.render()

At this point, we're ready to upload.  For details on the ``results``
dictionary, refer to the developer docs, :ref:`rendered_results_dict`.

If you're interested, you can check to see which files were created:

.. testcode::

    from trackhub.helpers import show_rendered_files
    show_rendered_files(results)

.. testoutput::

    rendered file: example_hub.hub.txt (created by: <trackhub.hub.Hub object at 0x...>)
    rendered file: example_hub.genomes.txt (created by: <trackhub.genomes_file.GenomesFile object at 0x...>)
    rendered file: dm3/trackDb.txt (created by: <trackhub.trackdb.TrackDb object at 0x...>)


HTML documentation for tracks
-----------------------------
See :ref:`htmldocs` for more info on how to easily add documentation to your
tracks kwarg to tracks by simply providing some content via the `html_string`
kwarg when creating any subclass of :class:`BaseTrack`.

Uploading
---------
So far we've seen how to use :mod:`trackhub` to create the text files that
define a track hub.  Now lets see how to use :mod:`trackhub` to upload these
files and all associated data files to a publicly available web server.

In order to do this, each hub component that refers to a file needs to have
3 different filenames defined:

:``local_fn``:
    local filename on disk (e.g., :file:`/data/sample_01_filtered.bam`)
:``remote_fn``:
    remote filename used by SSH to transfer to host (e.g.,
    :file:`/var/www/data/sample1.bam`)
:``url``:
    publicly accessible URL as served by the host (e.g.,
    :file:`http://example.com/sample1.bam`)

You will need a publicly-accessible location to upload your tracks to (ftp,
http, https; see http://genome.ucsc.edu/goldenPath/help/hgTrackHubHelp.html for
more info).  Currently, the upload mechanism expects SSH access, and works best
if you configure ssh to use public/private key pairs (google "ssh no password"
for more info on this).

::

    from trackhub.upload import upload_track, upload_hub
    for track in trackdb.tracks:
        upload_track(track=track, host=host, user=user)

    upload_hub(hub=hub, host=host, user=user)


Now you can paste the hub's :attr:`Hub.url` into the UCSC genome browser track
hub page to load your new hub.


Group related tracks into an aggregate track
____________________________________________
To group related tracks and view as a single track we utilize
an aggregate::


    AGGREGATE TRACK STANZA
    - Defines a group of tracks to vizualize as a single
      track
    - defines top-level params

        TRACK A STANZA
        - Defines params for this track, including bigDataUrl
        - Refers to aggregate as parent

        TRACK B STANZA
        - Defines params for this track, including bigDataUrl
        - Refers to aggregate as parent

Connections between aggregate tracks, and subtracks
will be created in much the same way -- for example,
``aggregate.add_subtrack(subtrack)`` to add the child ``subtrack`` to the parent ``aggregate`` track.

Creating an aggregate track
___________________________
So lets create an aggregate:

.. testcode::
    
    from trackhub import AggregateTrack

    aggregate = AggregateTrack(
        name="aggregate",
        tracktype='bigWig 0 2000',
        short_label="my aggregate",
        long_label="An example aggregate",
        aggregate='transparentOverlay')

    #make sure it looks OK
    print aggregate

.. testoutput::
    :options: +REPORT_NDIFF

    track aggregate
    shortLabel my aggregate
    longLabel An example aggregate
    type bigWig 0 2000
    aggregate transparentOverlay
    container multiWig

After the aggregate track has been created, we can incrementally add additional
parameters.  This is same method can be used for all classes derived from
:class:`Track`:

.. testcode::

    aggregate.add_params(showSubtrackColorOnUi='on')

    print aggregate

.. testoutput::
    :options: +REPORT_NDIFF

    track aggregate
    shortLabel my aggregate
    longLabel An example aggregate
    type bigWig 0 2000
    aggregate transparentOverlay
    showSubtrackColorOnUi on
    container multiWig


After the aggregate track has been created, we can incrementally
add additional tracks, just like :class:`CompositeTrack`, :class:`ViewTrack`.

Create two new :class:`Track` instances and add them to the ``aggregate``. 
Each instance represents a stanza in the ``aggregate``: 

.. testcode::
    
    from trackhub import Track
    import os

    URLBASE = 'http://example.com/mytrackhubs'
    GENOME = 'dm3'

    track1 = Track(
        name="track1Track",
        url=os.path.join(URLBASE, GENOME, 'track1.bigWig'),
        tracktype='bigWig 0 1400',
        short_label='track1',
        long_label='my track #1',
        # add other params here...
        color='120,235,204')

    track2 = Track(
        name="track2Track",
        url=os.path.join(URLBASE, GENOME, 'track2.bigWig'),
        tracktype='bigWig 0 1700',
        short_label='track2',
        long_label='my track #2',
        # add other params here...
        color='255,128,128')

    aggregate.add_subtrack(track1)
    aggregate.add_subtrack(track2)

    #make sure it looks OK
    print aggregate

.. testoutput::
    :options: +REPORT_NDIFF


    track aggregate
    shortLabel my aggregate
    longLabel An example aggregate
    type bigWig 0 2000
    aggregate transparentOverlay
    showSubtrackColorOnUi on
    container multiWig

        track track1Track
        bigDataUrl http://example.com/mytrackhubs/dm3/track1.bigWig
        shortLabel track1
        longLabel my track #1
        type bigWig 0 1400
        color 120,235,204
        parent aggregate

        track track2Track
        bigDataUrl http://example.com/mytrackhubs/dm3/track2.bigWig
        shortLabel track2
        longLabel my track #2
        type bigWig 0 1700
        color 255,128,128
        parent aggregate

The new ``aggregate`` track can be added to ``trackDb.txt``
like other track objects. To see how to connect the components,
see :ref:`connecting-the-components`.
