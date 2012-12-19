.. trackhub documentation master file, created by
   sphinx-quickstart on Fri Sep 21 17:51:18 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

`trackhub` documentation
========================
Why :mod:`trackhub`?
====================
.. currentmodule:: trackhub

This Python package, :mod:`trackhub`, aims to ease in construction of programatically-generated track
hubs for the UCSC Genome Browser.

The existing framework for creating a track hub consists of writing a text file
as detailed in the `trackDb.txt README <http://genome-source.cse.ucsc.edu/gitweb/?p=kent.git;a=blob;f=src/hg/makeDb/trackDb/README;hb=HEAD>`_
(and, more recently, in the development `track database definition page
<http://genome.ucsc.edu/goldenPath/help/trackDb/trackDbHub.html>`_).

This can get extremely tedious, especially when trying to create and upload
track hubs as part of an automated pipeline.  :mod:`trackhub` tries to ease
this creation by providing a framework in Python for creating track hubs from
scripts and programs. Why use :mod:`trackhub`?:

* `filename handling`: automatic (yet still completely configurable, if needed)
  handling of filenames and directory structure
* `uploading`: upload a full hub -- hub/genomes/trackdb files, plus all data
  files (bam/bigWig/bigBed) -- via rsync over ssh
* `validation`: mechanisms for handling validation of parameters so errors are
  [hopefully] caught prior to uploading
* `rapid deployment`: mapping local filenames to remote filenames on the host enables
  rapid updating of the hub with new or updated data (e.g., when analysis
  parameters change)
* `flexibility`: support for simple hubs up through complex composite hubs with views and
  subtracks
* `extensible`: provides a framework for working with hub components, allowing
  new functionality to be easily added

Move on to the :ref:`quickstart` to get started, or try the more in-depth
:ref:`tutorial`.

Contents:

.. toctree::
    :maxdepth: 2

    quickstart
    tutorial
    filenames
    autodocs
    developers
    changelog
