.. currentmodule:: trackhub

Topical docs
============

.. _parameter_validation:

Validation of parameters
------------------------
:mod:`trackhub.constants` contains dictionaries of
:class:`trackhub.constants.Parameter` objects.  These were copied from the
trackDB help text from kentsrc.

Each Parameter object takes the parameter name, a description, and a "possible
values" object.  For simple cases, it's ``str`` or ``int``.  But for more
complex things -- like a comma separated RBG tuple -- a validation class, like
:class:`trackhub.constants.RGB`, can be provided.

Need to validate a new kind of parameter?  Write a function in
:mod:`validate.py` that returns True when its argument is valid.  For example,
:func:`trackhub.validate.RGB` checks that the value is a string containing
3 comma-separated integers that are between 0-255.

Different kinds of hub components are allowed to have different parameters.  In
:mod:`trackhub.constants`, there are dictionaries -- keyed by parameter name --
for the different components.

For example, there's a ``track_fields`` dictionary with all common track
parameters, and ``composite_track_fields`` which adds additional params used
for composite tracks.  ``track_typespecific_fields`` is a nested dict that has
specific parameters for bigBed, bigWig, and BAM formats.

.. _rendered_results_dict:

Rendered results dictionary
---------------------------
This section describes the ``results`` dictionary created in the tutorial in
the :ref:`render_tut` section.

``results`` is recursive nested dictionary, helpful for debugging or just
useful to see the structure of the track hub and what happened.

Each level has at least the object itself as a key and a dictionary of its
children as the value.  If an object rendered a text file, then it will have an
additional key at that level for itself and a value for the text file.
Any other keys at that level are keys of the children, which in turn is
a dictionary of [possibly] the child and any other sub-children, in a similar
structure.  It's probably easier just to look at the example -- we can view
a nicely-formatted version of it as follows:

::

    from trackhub.helpers import print_rendered_results
    print_rendered_results(results)

::

    {
        "<trackhub.hub.Hub object at 0x...>": "example_hub.hub.txt",
        "<trackhub.genomes_file.GenomesFile object at 0x...>": {
            "<trackhub.genomes_file.GenomesFile object at 0x...>": "example_hub.genomes.txt",
            "<trackhub.genome.Genome object at 0x...>": {
                "<trackhub.trackdb.TrackDb object at 0x...>": {
                    "<trackhub.trackdb.TrackDb object at 0x...>": "dm3/trackDb.txt",
                    "<trackhub.track.CompositeTrack object at 0x...>": {
                        "<trackhub.track.ViewTrack object at 0x...>": {
                            "<trackhub.track.Track object at 0x...>": {},
                            "<trackhub.track.Track object at 0x...>": {},
                            "<trackhub.track.Track object at 0x...>": {}
                        },
                        "<trackhub.track.ViewTrack object at 0x...>": {
                            "<trackhub.track.Track object at 0x...>": {},
                            "<trackhub.track.Track object at 0x...>": {}
                        }
                    }
                }
            }
        }
    }

For example, this shows that the rendering of the :class:`Hub` object resulted
in a text file ``example_hub.hub.txt``, and it had one child object (since
there's only one other key besides the hub itself at the same nesting level) -- the
:class:`GenomesFile` object.

That :class:`GenomesFile` object then rendered a ``example_hub.genomes.txt``
file, and contained a single :class:`Genome` object child.  Note that the
:class:`Genome` object itself did *not* render any text file -- that's because
it represents just a stanza in the :class:`GenomesFile` object rather than
a full file to itself.

The :class:`Genome` object contains one child, the :class:`TrackDb` object,
which *does* write out a file, ``dm3/trackDb.txt``.

The :class:`TrackDb` object then has 1 child objects -- the
:class:`CompositeTrack` object.  Again, no file created.  However there are
2 children here, the 2 :class:`ViewTrack` objects, each of which have several
:class:`Track` children.

