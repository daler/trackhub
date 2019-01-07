from __future__ import absolute_import, print_function

import os
import json
from . import base
from .hub import Hub
from .compatibility import string_types

_here = __file__


def dimensions_from_subgroups(s):
    """
    Given a sorted list of subgroups, return a string appropriate to provide as
    a composite track's `dimensions` arg.

    Parameters
    ----------
    s : list of SubGroup objects (or anything with a `name` attribute)
    """
    letters = 'XYABCDEFGHIJKLMNOPQRSTUVWZ'
    return ' '.join(['dim{0}={1}'.format(dim, sg.name)
                     for dim, sg in zip(letters, s)])


def filter_composite_from_subgroups(s):
    """
    Given a sorted list of subgroups, return a string appropriate to provide as
    the a composite track's `filterComposite` argument

    >>> import trackhub
    >>> trackhub.helpers.filter_composite_from_subgroups(['cell', 'ab', 'lab', 'knockdown'])
    'dimA dimB'

    Parameters
    ----------
    s : list
        A list representing the ordered subgroups, ideally the same list
        provided to `dimensions_from_subgroups`. The values are not actually
        used, just the number of items.
    """
    dims = []
    for letter, sg in zip('ABCDEFGHIJKLMNOPQRSTUVWZ', s[2:]):
        dims.append('dim{0}'.format(letter))
    if dims:
        return ' '.join(dims)


def hex2rgb(h):
    """
    Convert hex colors to RGB tuples

    Parameters
    ----------
    h : str
        String hex color value

    >>> hex2rgb("#ff0033")
    '255,0,51'
    """
    if not h.startswith('#') or len(h) != 7:
        raise ValueError("Does not look like a hex color: '{0}'".format(h))
    return ','.join(map(str, (
        int(h[1:3], 16),
        int(h[3:5], 16),
        int(h[5:7], 16),
    )))


def sanitize(s, strict=True):
    """
    Sanitize a string.

    Spaces are converted to underscore; if strict=True they are then removed.

    Parameters
    ----------
    s : str
        String to sanitize

    strict : bool
        If True, only alphanumeric characters are allowed. If False, a limited
        set of additional characters (-._) will be allowed.
    """
    allowed = ''.join(
        [
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'abcdefghijklmnopqrstuvwxyz',
            '0123456789',
        ]
    )

    if not strict:
        allowed += '-_.'

    s = str(s).replace(' ', '_')

    return ''.join([i for i in s if i in allowed])


def auto_track_url(track):
    """
    Automatically sets the bigDataUrl for `track`.

    Requirements:

        * the track must be fully connected, such that its root is a Hub object
        * the root Hub object must have the Hub.url attribute set
        * the track must have the `source` attribute set
    """
    hub = track.root(cls=Hub)

    if hub is None:
        raise ValueError(
            "track is not fully connected because the root is %s" % repr(hub))
    if hub.url is None:
        raise ValueError("hub.url is not set")
    if track.source is None:
        raise ValueError("track.source is not set")


def show_rendered_files(results_dict):
    """
    Parses a nested dictionary returned from :meth:`Hub.render` and just prints
    the resulting files.
    """
    for k, v in results_dict.items():
        if isinstance(v, string_types):
            print("rendered file: %s (created by: %s)" % (v, k))
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
        print(s.rstrip())


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
