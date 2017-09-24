.. currentmodule:: trackhub

.. _filenames:

Filenames
=========

Each hub component that refers to a file (either rendered, like :class:`Hub`,
:class:`GenomesFile` and :class:`TrackDb`, or by reference, like :class:`Track`
objects) needs 2 filename attributes specified:

    1. :attr:`local_fn`, which specifies the local filename on disk

    2. :attr:`remote_fn`, which specifies the full path on the remote host that
       will be uploaded to over SSH

In addition, for hub components that will eventually be publicly accessible (:class:`Hub`
and :class:`Track`), there is a :attr:`url` attribute that specifies the public
web-accessible location.  This is an alias to :attr:`bigDataUrl` for
:class:`Track` objects.

:mod:`trackhub` tries to use sensible defaults where possible in order to
minimize configuration effort; this behavior is described below.


.. _defaults:

Default filenames
-----------------
.. note::

    If you want to put the hub somewhere other than the default of the current
    directory, usually all you need to do is set :attr:`Hub.local_dir` and
    :attr:`Hub.remote_dir`, and everything else will follow automatically.

    If you would like to have more control over the filenames, read through the
    tables below.

General behavior
~~~~~~~~~~~~~~~~
Here are some characteristics of the filename handling that may help understand
the behavior:

* If you manually specify a filename, that filename takes priority for that
  object.
* **Reset** the default behavior by setting the attribute back to `None`
* If a child component's filename has been reset but the parent's has not, the
  child component will have a sensible default that reflect the parent's
  filename (see tables below).
* Hub components that do not refer to filenames do not have a :attr:`local_fn`
  or :attr:`remote_fn` attribute.


Hub default filenames
~~~~~~~~~~~~~~~~~~~~~
For ease of configuration, you can set the :attr:`Hub.local_dir` and
:attr:`Hub.remote_dir`, and children :class:`HubComponent` objects will use
sensible defaults:

.. note::

    The "example" columns are a sort of running example across tables, where
    the hub's local_dir and remote_dir have been set to custom locations but
    everything else uses the default behavior.

======================== ======================================================= ====================================================
Attribute                Default value                                           Example
======================== ======================================================= ====================================================
:attr:`Hub.local_dir`    :file:`./`                                              :file:`/data/`
:attr:`Hub.remote_dir`   :file:`./`                                              :file:`/var/www/hubs/`
======================== ======================================================= ====================================================

For more control over the hub's filename, set the attributes directly:

======================== ======================================================= ====================================================
Attribute                Default value                                           Example
======================== ======================================================= ====================================================
:attr:`Hub.local_fn`     :file:`[Hub.local_dir]/[Hub.hub].hub.txt`               :file:`/data/example_hub.txt`
:attr:`Hub.remote_fn`    :file:`[Hub.remote_dir]/[Hub.hub].hub.txt`              :file:`/var/www/hubs/example_hub.txt`
======================== ======================================================= ====================================================

:class:`Hub` objects should have their :attr:`url` attribute manually set.

======================== ======================================================= ====================================================
Attribute                Default value                                           Example
======================== ======================================================= ====================================================
:attr:`Hub.url`          None                                                    :file:`http://example.com/hubs/example.hub.hub.txt`
======================== ======================================================= ====================================================

GenomeFile default filenames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The defaults for :class:`GenomeFile` objects use the parent :class:`Hub`'s
configured values.  If there is no parent :class:`Hub`, then the value is None.
For the "Default value" column below, assume that :file:`Hub` is the parent
hub.  The examples assume the example hub values in the above table.

================================ ======================================================= ===============================================
Attribute                        Default value                                           Example (using Hub above)
================================ ======================================================= ===============================================
:attr:`GenomesFile.local_fn`     :file:`[dirname(Hub.local_fn)]/genomes.txt`             :file:`/data/genomes.txt`
:attr:`GenomesFile.remote_fn`    :file:`[dirname(Hub.remote_dir)]/genomes.txt`           :file:`/var/www/hubs/genomes.txt`
================================ ======================================================= ===============================================

TrackDb default filenames
~~~~~~~~~~~~~~~~~~~~~~~~~

Recall that each :class:`TrackDb` has a parent :class:`Genome`, which has a
:attr:`Genome.genome` attribute defining the assembly name.  In the "Default
value" column, assume that :file:`Genome` is the parent genome, and
:file:`GenomesFile` is the parent genomes file (with values configured as in
the "example" column above).

================================ ==================================================================== ================================================
Attribute                        Default value                                                        Example
================================ ==================================================================== ================================================
:attr:`TrackDb.local_fn`         :file:`[dirname(GenomesFile.local_fn)]/[Genome.genome]/trackDb.txt`  :file:`/data/hg19/trackDb.txt`
:attr:`TrackDb.remote_fn`        :file:`[dirname(GenomesFile.remote_fn)]/[Genome.genome]/genomes.txt` :file:`/var/www/hubs/hg19/trackDb.txt`
================================ ==================================================================== ================================================


Track default filenames
~~~~~~~~~~~~~~~~~~~~~~~

Recall that :class:`Track` objects have a parent :class:`TrackDb` object;
assume that :file:`TrackDb` is the parent TrackDb object (with values
configured as in the "example" column above).

:class:`Track` objects that are children of :class:`ViewTrack` and/or
:class:`CompositeTrack` objects still have a parent :class:`TrackDb` object,
which is used for configuring the defaults below.

Since the most meaningful part of a track hub is the data it contains, no
effort is made to assume what local filename you'd like to point each
:class:`Track` to.  However, the remote and URLs try to use sensible defaults.

================================ ============================================================== =================================================
Attribute                        Default value                                                  Example
================================ ============================================================== =================================================
:attr:`Track.local_fn`           None                                                           :file:`/data/sample_01/bams/final.sorted.bam`
:attr:`Track.remote_fn`          :file:`[dirname(TrackDb.remote_fn)]/[Track.name].[Track.type]` :file:`/var/www/hubs/hg19/sample_1.bam`
:attr:`Track.url`                :file:`[dirname(TrackDb.url)]/[Track.name].[Track.type]`       :file:`http://example.com/hubs/hg19/sample_1.bam`
================================ ============================================================== =================================================


.. _htmldocs:

HTML documentation default filenames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Providing a :class:`BaseTrack` subclass (typically :class:`CompositeTrack`)
with an `html_string` will trigger an automatic creation of an HTML file that
will be displayed on the bottom of the configuration page.

You can also directly set the `html_string` after the object has been created.
The following will trigger, at render time, the creation of an HTML file whose
contents will be automatically shown at the bottom of the track configuration
page::

    composite_track.html_string = """
    <h2>Description</h2>
    <p>This track shows...it was created by...</p>
    """


While the docs at
http://genome.ucsc.edu/goldenPath/help/trackDb/trackDbHub.html#commonSettings
say that an `html` parameter is needed if you want to supply documentation, it
turns out you don't need this if there is a :file:`<trackname>.html` file in
the same directory as the `trackDb.txt`.

HTML files are created at render time.  If you don't want to use any of this
automatic filename handling, simply write your own HTML file, upload it
wherever you'd like, and manually specify the `html` kwarg to point to that
file (relative to `trackDb.txt`) when creating a track.


================================ ============================================================== =================================================
Attribute                        Default value                                                  Example
================================ ============================================================== =================================================
:attr:`HTMLDoc.local_fn`         :file:`[dirname(TrackDb.local_fn)]/[Track.name].html`          :file:`/data/hg19/sample_1.html`
:attr:`HTMLDoc.remote_fn`        :file:`[dirname(TrackDb.remote_fn)]/[Track.name].html`         :file:`/var/www/hubs/hg19/sample_1.html`
================================ ============================================================== =================================================
