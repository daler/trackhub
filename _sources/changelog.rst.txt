Changelog
=========
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
