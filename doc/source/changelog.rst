Changelog
=========
Version 0.2 (Nov 2017)
----------------------
Major release breaking backwards compatibility.

One of the features of `trackhub` I've always found useful is the ability to
have a local file (configured as ``local_fn`` in ``Track`` objects) in
a completely different path on the remote host (configured with ``remote``).
The way this was handled was by rsync-ing each file separately, but that meant
that the directory needed to be created on the host. For this, I used the
`fabric` package with its remote execution functions.

This worked fine, but was not optimal because 1) `fabric` does not support
Python 3 and 2) rsync-ing many individual files could be slow, and annoying if
the the hostshowed a banner each time or if a public key was not configured on
the host.

One of the major changes in this version is that instead of individual rsync
calls, first the directory structure desired on the host is recreated locally
using symlinks. This is called the "staging" area. Then the entire staging area
is rsynced at once (using `-L` so that links are followed) to the host. The end
result is the same as before (local paths don't have to match remote pathsThe
end result is the same as before (local paths don't have to match remote
paths), but with the added bonus of being able to inspect the files in the
staging area.

Having both remote_fn and local_fn seemed like overkill especially for
rendered-on-the-fly files like the hub file or genomes file. There were also
problems with the assembly hub remote filenames, and debugging it was tricky.

Rendering take place in the (newly-introduced) staging area using the filename
attribute, and what used to be "rendering" is now "staging". For
rendered-on-the-fly files, filename is created relative to the staging
directory. Objects that represent an existing file on disk (BAM, bigWig, .2bit,
etc) have a source attribute pointing to that file, and a filename attribute,
similar to the other objects, that represents the remote path relative to the
staging dir.


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
