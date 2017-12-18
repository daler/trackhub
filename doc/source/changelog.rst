Changelog
=========
Version 0.2 (Nov 2017)
----------------------

Overhaul in how files are uploaded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Instead of uploading files one-by-one, first the hub is rendered to a local
"staging" directory and tracks are symlinked over to this directory. BAM and
VCF indexes are also symlinked if needed, and any HTML documentation is also
rendered to the staging directory.  This allows for inspecting the hub locally
before uploading.  The entire directory can then be uploaded with ``rsync``
using the ``-L`` option to follow symlinks.


``local_fn`` is replaced by ``source``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To better align the semantics of keyword arguments with this new uploading
strategy, ``local_fn`` and ``remote_fn`` are deprecated as arguments to
:class:`Track` objects. Using them is still supported, but a DeprecationWarning
will be raised. Instead, use ``source`` to point to a file on disk.  This
allows support of the ``url`` argument, to provide a remote URL that you want
to include in the hub but are not uploading yourself. If more control over the
filename is required, use the ``filename`` argument. See the documentation for
:class:`trackhub.BaseTrack` for details.



Version 0.1.3 (Nov 2015)
------------------------
- fixed bug where local rsync operations were not using the provided rsync options
- docs now at https://daler.github.io/trackhub
- tests now on travis-ci using Docker

Version 0.1.2 (Jan 2 2015)
--------------------------
- always use the remote filename of a BAM when uploading the corresponding .bai
- add support for BAM parameters `baseColorUseSequence`, `baseColorDefault`,
  and `showDiffBasesAllScales`
- add `fabric` as a dependency upon install
- better example in the README
- use local path of trackdb to be relative to the hub local filename (thanks
  Jakob Goldman)

Version 0.1.1 (Dec 19 2012)
---------------------------
- Initial support for SuperTracks (Venkat Malladi)
- Support for vcfTabix format (Venkat Malladi)
- Support for most known UCSC parameters (in constants.py) (Venkat Malladi)
- Support for aggregate tracks (Venkat Malladi)
- `default_hub()` function for creating a fully-connected set of components
- `long_label` for tracks defaults to `short_label`
- `run_local` kwarg for upload functions to upload hubs/data locally
- various typo and consistency fixes in docs
- improvements to automatic track URL handling
- better support for adding single tracks
- subgroups incrementally updated rather than replaced

Version 0.1 (Oct 30 2012)
-------------------------
Initial release
