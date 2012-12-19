Changelog
=========

Version 0.1 (Oct 30 2012)
-------------------------
Initial release

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
