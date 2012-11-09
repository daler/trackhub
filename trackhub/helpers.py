import os
import sys
import json
import base
from hub import Hub

_here = __file__

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

def auto_track_url(track):
    """
    Automatically sets the bigDataUrl for `track`.

    Requirements:

        * the track must be fully connected, such that its root is a Hub object
        * the root Hub object must have the Hub.url attribute set
        * the track must have the `local_fn` attribute set
    """
    hub = track.root(cls=Hub)

    if hub is None:
        raise ValueError(
            "track is not fully connected because the root is %s" % repr(hub))
    if hub.url is None:
        raise ValueError( "hub.url is not set")
    if track.local_fn is None:
        raise ValueError("track.local_fn is not set")




def show_rendered_files(results_dict):
    """
    Parses a nested dictionary returned from :meth:`Hub.render` and just prints
    the resulting files.
    """
    for k, v in results_dict.items():
        if isinstance(v, basestring):
            print "rendered file: %s (created by: %s)" % (v, k)
        else:
            show_rendered_files(v)
    return


def print_rendered_results(results_dict):
    """
    Pretty-prints the rendered results dictionary.

    Rendered results can be multiply-nested dictionaries; this uses JSON
    serialization to print a nice representation.
    """
    class _HubComponentEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, base.HubComponent):
                return repr(o)
            return json.JSONEncoder.default(self, o)
    formatted = json.dumps(results_dict, indent=4, cls=_HubComponentEncoder)
    # the returned string contains lines with trailing spaces, which causes
    # doctests to fail.  So fix that here.
    for s in formatted.splitlines():
        print s.rstrip()


def data_dir():
    """
    Returns the data directory that contains example files for tests and
    documentation.
    """
    return os.path.join(os.path.dirname(_here), 'test', 'data')


def example_bigbeds():
    """
    Returns list of example bigBed files
    """
    hits = []
    d = data_dir()
    for fn in os.listdir(d):
        fn = os.path.join(d, fn)
        if os.path.splitext(fn)[-1] == '.bigBed':
            hits.append(os.path.abspath(fn))
    return hits


def example_bigwigs():
    """
    Returns list of bigWig example files
    """
    hits = []
    d = data_dir()
    for fn in os.listdir(d):
        fn = os.path.join(d, fn)
        if os.path.splitext(fn)[-1] == '.bw':
            hits.append(os.path.abspath(fn))
    return hits
