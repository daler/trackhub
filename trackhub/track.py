from __future__ import absolute_import

import os
import re
from collections import OrderedDict
from .base import HubComponent, deprecation_handler
from . import hub
from . import trackdb
from . import constants


TRACKTYPES = ['bigWig', 'bam', 'bigBed', 'vcfTabix', None]


def _check_name(name):
    regex = re.compile('[^a-zA-Z0-9-_]')
    if regex.search(name):
        raise ValueError('Non-alphanumeric character in name "%s"' % name)


class ParameterError(Exception):
    pass


class SubGroupDefinition(object):
    def __init__(self, name, label, mapping, default="none"):
        """
        Represents a subgroup line in a composite track.

        Instances of this class are provided to a composite track in order to
        define options for the subtracks' groups.

        Parameters
        ----------

        name : str
            Name for the subgroup (e.g., "celltype").

        label : str
            The label that will be displayed (e.g., "Cell_Type")

        mapping : dict
            Dictionary of {tag: title}, where `tag` will be how subtracks
            access this group and `title` is how it will be displayed in the
            browser, e.g.::

                {
                  "ES": "Embryonic stem cell",
                 "MEF": "Mouse embryonic fibroblast"
                }

            Upon appending this SubGroupDefinition to a composite track, the
            options for the subtracks' subgroups are required to come from the
            keys in the mapping.  Continuing the example, "celltype=ES" would
            be a valid subgroup for a subtrack, but "celltype=other" would not
            since it's not in the mapping dict above.

        default : str
            Value to be used by subtracks if they don't explicitly define this
            subgroup. Continuing the example, if a subtrack didn't specify the
            "celltype" subgroup, then by default a "celltype=none" value will
            be added.  This is necessary because subtracks must define a value
            for all groups.
        """
        self.name = name
        self.label = label
        self.mapping = mapping
        self.default = default

    def __str__(self):
        s = []
        s.append(self.name)
        s.append(self.label)
        s.extend('%s=%s' % (k, v) for k, v in self.mapping.items())
        return ' '.join(s)


class BaseTrack(HubComponent):

    # Dictionary where keys are parameter names (e.g., "color") and values are
    # Parameter objects.  These are defined in the constants module.
    params = OrderedDict()
    params.update(constants.track_field_order)
    params.update(constants.track_fields)

    # For a plain 'ol Track, there's nothing specific.  But CompositeTracks and
    # ViewTracks can have addtional specific parameters (e.g., filterComposite
    # for CompositeTracks) that need to be handled separately.  Make some space
    # for that here.
    specific_params = OrderedDict()

    def __init__(self, name, tracktype=None, short_label=None,
                 long_label=None, parentonoff="on", subgroups=None, source=None,
                 filename=None, html_string=None, **kwargs):
        """
        Represents a single track stanza, base class for other track types.

        Parameters
        ----------

        name : str
            Name of the track

        tracktype : str
            Type of the track (e.g., "bam", "bigWig"). The UCSC parameter name
            is "type" which is a reserved Python keyword, hence using
            "tracktype" here.

        short_label : str
            Used for the left-hand side track label; alias for UCSC parameter
            "shortLabel"

        long_label : str
            Used for the longer middle labels; if None will copy
            short_label. Alias for UCSC parameter "longLabel".

        parentonoff : 'on' | 'off'
            Used to determine individual track status on or off

        subgroups : dict
            A dictionary of `{name: tag}` where each `name` is the name of
            a SubGroupDefinition in a parent :class:`CompositeTrack` and each
            `tag` is a key in the SubGroupDefinition.mapping dictionary. The
            dictionary `{'celltype': 'ES'} would end up looking like this in
            the string representation::

                subGroups celltype=ES

            or like this, if the track had been added to a ViewTrack with name
            `aln`::

                subGroups view=aln celltype=ES

        source : str or None
            Local path to the file. If None, then `url` must instead be used to
            point to an already-existing filename or URL.

        filename : str or None
            Path to upload the file to, over rsync and ssh, relative to the hub
            directory. Typically only used when you need extensive control over
            the remote filename.  If None, will use a filename of
            "<name>.tracktype>" in the same directory as the TrackDb. By
            default, TrackDb goes in a directory named after the assembly of
            its parent Genome object.

        See docstring for :class:`Track` for details.
        """
        source, filename = deprecation_handler(source, filename, kwargs)
        HubComponent.__init__(self)
        _check_name(name)
        self.name = name
        self.tracktype = tracktype
        if short_label is None:
            short_label = name
        self.short_label = short_label
        if long_label is None:
            long_label = short_label
        self.long_label = long_label
        self.parentonoff = parentonoff

        self._source = source
        self._filename = filename
        self.html_string = html_string
        self.subgroups = {}
        self.add_subgroups(subgroups)

        # Convert pythonic strings to UCSC versions
        kwargs['track'] = name
        kwargs['type'] = tracktype
        kwargs['longLabel'] = kwargs.get('longLabel', long_label)
        kwargs['shortLabel'] = kwargs.get('shortLabel', short_label)

        self.kwargs = kwargs

        self._orig_kwargs = kwargs.copy()

    @property
    def _html(self):
        if not self.html_string:
            return None
        _html = HTMLDoc(self.html_string)
        _html.add_parent(self)
        return _html

    @property
    def trackdb(self):
        return self.root(trackdb.TrackDb)[0]

    @property
    def hub(self):
        return self.root(hub.Hub)[0]

    @property
    def source(self):
        if self._source is not None:
            return self._source
        return None

    @source.setter
    def source(self, fn):
        self._source = fn

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename

        # If filename hasn't been assigned then make one automatically based
        # on the track name and the trackhub's filename (which, by the way,
        # acts similarly, deferring up to the genomes_file.filename . . . and
        # so on up to the hub's filename).
        #
        # However, if source is None and URL is set, then this is an
        # already-existing remote file and so should not have a filename.
        if self.trackdb:
            if self.source is None and self._url is not None:
                return None
            return os.path.join(
                os.path.dirname(self.trackdb.filename),
                self.name + '.' + self.tracktype.split(' ')[0])
        return None

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    @property
    def tracktype(self):
        return self._tracktype

    @tracktype.setter
    def tracktype(self, tracktype):
        """
        When setting the track type, the valid parameters for this track type
        need to be set as well.
        """
        self._tracktype = tracktype
        if tracktype is not None:
            if 'bed' in tracktype.lower():
                tracktype = 'bigBed'
            elif 'wig' in tracktype.lower():
                tracktype = 'bigWig'
        self.params.update(constants.track_typespecific_fields[tracktype])

    def add_trackdb(self, trackdb):
        """
        Attach this track to a parent TrackDb object.
        """
        self.add_parent(trackdb)

    def add_params(self, **kw):
        """
        Add [possibly many] parameters to the track.

        Parameters will be checked against known UCSC parameters and their
        supported formats.

        E.g.,

        add_params(color='128,0,0', visibility='dense')

        """
        for k, v in kw.items():
            if (k not in self.params) and (k not in self.specific_params):
                raise ParameterError('"%s" is not a valid parameter for %s'
                                     % (k, self.__class__.__name__))
            try:
                self.params[k].validate(v)
            except KeyError:
                self.specific_params[k].validate(v)

        self._orig_kwargs.update(kw)
        self.kwargs = self._orig_kwargs.copy()

    def remove_params(self, *args):
        """
        Remove [possibly many] parameters from the track.

        E.g.,

        remove_params('color', 'visibility')
        """
        for a in args:
            self._orig_kwargs.pop(a)
        self.kwargs = self._orig_kwargs.copy()

    def add_subgroups(self, subgroups):
        """
        Update the subgroups for this track.

        Parameters
        ----------

        subgroups : dict
            Dictionary of subgroups, e.g., {'celltype': 'K562', 'treatment':
            'a'}.  Each key must match a SubGroupDefinition name in the
            composite's subgroups list.  Each value must match a key in that
            SubGroupDefinition.mapping dictionary.
        """
        if subgroups is None:
            subgroups = {}
        assert isinstance(subgroups, dict)
        self.subgroups.update(subgroups)

    def __str__(self):
        s = []

        specific = []
        for name, parameter_obj in self.specific_params.items():
            value = self.kwargs.pop(name, None)
            if value is not None:
                if parameter_obj.validate(value):
                    specific.append("%s %s" % (name, value))

        for name, parameter_obj in self.params.items():
            value = self.kwargs.pop(name, None)
            if name == 'bigDataUrl':
                value = getattr(self, 'url', None)
            if value is not None:
                if parameter_obj.validate(value):
                    s.append("%s %s" % (name, value))

        s.extend(specific)

        # Handle subgroups differently depending on if this is a composite
        # track or not.
        s.extend(self._str_subgroups())

        if self.parent is not None:
            if isinstance(self.parent, BaseTrack):
                s.append('parent %s' % self.parent.name + ' ' + self.parentonoff)

        if len(self.kwargs) > 0:
            raise ParameterError(
                "Unhandled keyword arguments: %s" % self.kwargs)

        self.kwargs = self._orig_kwargs.copy()

        return '\n'.join(s)

    def _render(self, staging='staging'):
        if self._html:
            self._html.render(staging)

    def _str_subgroups(self):
        """
        helper function to render subgroups as a string
        """
        if not self.subgroups:
            return ""
        return ['subGroups %s'
                % ' '.join(['%s=%s' % (k, v) for (k, v) in
                           self.subgroups.items()])]

    def validate(self):
        pass

    @property
    def html_fn(self):
        if self.filename and self.trackdb:
            return os.path.join(
                os.path.dirname(self.trackdb.filename),
                self.name + '.html')
        else:
            return None


class Track(BaseTrack):
    def __init__(self, url=None, *args, **kwargs):
        """
        Represents a single track stanza along with the file it describes.

        See :class:`BaseTrack` for details on arguments. Additional arguments
        supported by this class:

        Parameters
        ----------

        url : str
            Full URL for the track (i.e., bigDataUrl). Typically this is only
            used when using a remote track from some other provider or when you
            need lots of control over the URL. Otherwise the url will be
            automatically created based on `filename`.

        See :class:`BaseTrack` for details on other arguments.
        """
        kwargs['bigDataUrl'] = kwargs.get('bigDataUrl', url)
        super(Track, self).__init__(*args, **kwargs)
        self._url = url

    @property
    def url(self):
        if self._url is not None:
            return self._url
        if self.filename is None:
            return None
        return os.path.relpath(
            self.filename,
            start=os.path.dirname(self.trackdb.filename)
        )

    @url.setter
    def url(self, fn):
        self._url = fn


class CompositeTrack(BaseTrack):

    def __init__(self, *args, **kwargs):
        """
        Represents a composite track.  Subclasses :class:`BaseTrack`, and adds
        some extras.

        Add a view to this composite with :meth:`add_view`.

        Add a subtrack with :meth:`add_track`.

        Eventually, you'll need to make a :class:`trackdb.TrackDb` instance and
        add this composite to it with :meth:`trackdb.TrackDb.add_tracks()`.

        If composite=True, then this track will be considered a composite
        parent for other tracks.  In this case, `subgroups` is a list of
        :class:`SubGroupDefinition` objects, each defining the possible
        values and display labels for the items in a group (for example,
        a celltype SubGroupDefinition would define the tags and titles for
        cell types).  In the string representation of this Track, subgroups
        end up looking like::

            subGroup1 view Views aln=Alignments sig=Signal
            subGroup2 celltype Cell_Type ES=embryonic k562=K562

        See :class:`BaseTrack` for details on arguments. There are no
        additional arguments supported by this class.
        """
        super(CompositeTrack, self).__init__(*args, **kwargs)

        self.specific_params.update(constants.composite_track_fields)

        # TODO: are subtracks and views mutually exclusive, or can a composite
        # have both "view-ed" and "non-view-ed" subtracks?
        self.subtracks = []
        self.views = []

    def add_subgroups(self, subgroups):
        """
        Add a list of SubGroupDefinition objects to this composite.

        :param subgroups:
            List of SubGroupDefinition objects.
        """
        if subgroups is None:
            subgroups = {}
        _subgroups = {}
        for sg in subgroups:
            assert isinstance(sg, SubGroupDefinition)
            _subgroups[sg.name] = sg
        self.subgroups = _subgroups

    def add_subtrack(self, subtrack):
        """
        Add a child :class:`Track`.
        """
        self.add_child(subtrack)
        self.subtracks.append(subtrack)

    def add_view(self, view):
        """
        Add a ViewTrack object to this composite.

        :param view:
            A ViewTrack object.
        """

        self.add_child(view)
        self.views.append(view)

    def _str_subgroups(self):
        """
        renders subgroups to a list of strings
        """
        s = []

        i = 0

        # if there are any views, there must be a subGroup1 view View tag=val
        # as the first one.  So create it automatically here
        if len(self.views) > 0:
            mapping = dict((i.view, i.view) for i in self.views)
            view_subgroup = SubGroupDefinition(
                name='view',
                label='Views',
                mapping=mapping)
            i += 1
            s.append('subGroup%s %s' % (i, view_subgroup))

        for subgroup in self.subgroups.values():
            i += 1
            s.append('subGroup%s %s' % (i, subgroup))
        return s

    def __str__(self):

        s = []

        s.append(super(CompositeTrack, self).__str__())
        s.append('compositeTrack on')

        for view in self.views:
            s.append("")
            for line in str(view).splitlines(False):
                s.append('    ' + line)

        for subtrack in self.subtracks:
            s.append("")
            for line in str(subtrack).splitlines(False):
                s.append('    ' + line)
        return "\n".join(s)


class ViewTrack(BaseTrack):
    def __init__(self, view, *args, **kwargs):
        """
        Represents a View track.  Subclasses :class:`BaseTrack`, and adds some
        extras.

        This will need to be added to a :class:`track.CompositeTrack` with
        :meth:`track.CompositeTrack.add_view()`.

        Add tracks to this view with :meth:`track.ViewTrack.add_tracks()`.

        See :class:`BaseTrack` for details on arguments. Additional arguments
        supported by this class:

        Parameters
        ----------

        view : str
            Unique name to use for the view.

        See :class:`BaseTrack` for details on other arguments.
        """
        self.view = view
        kwargs['view'] = view
        super(ViewTrack, self).__init__(*args, **kwargs)
        self.subtracks = []

    def add_subgroups(self, subgroups):
        if subgroups is None:
            subgroups = {}
        else:
            raise ValueError('not sure if Views can have subgroups?')

    def add_tracks(self, subtracks):
        """
        Add one or more tracks to this view.

        subtracks : Track or iterable of Tracks
            A single Track instance or an iterable of them.
        """
        if isinstance(subtracks, Track):
            subtracks = [subtracks]
        for subtrack in subtracks:
            subtrack.subgroups['view'] = self.view
            self.add_child(subtrack)
            self.subtracks.append(subtrack)

    def _str_subgroups(self):
        return ""

    def __str__(self):
        s = []
        view_specific = []
        for name, parameter_obj in constants.view_track_fields.items():
            value = self.kwargs.pop(name, None)
            if value is not None:
                if parameter_obj.validate(value):
                    view_specific.append("%s %s" % (name, value))

        s.append(super(ViewTrack, self).__str__())
        s.extend(view_specific)

        for subtrack in self.subtracks:
            s.append("")
            for line in str(subtrack).splitlines(False):
                s.append('        ' + line)
        return '\n'.join(s)


class SuperTrack(BaseTrack):
    def __init__(self, *args, **kwargs):
        """
        Represents a Super track. Subclasses :class:`Track`, and adds some
        extras.

        Super tracks are container tracks (Folders) that group tracks. They are
        used to control visualization of a set of related data.

        Eventually, you'll need to make a :class:`trackdb.TrackDb` instance and
        add this supertrack to it with that instance's :meth:`add_tracks`
        method.

        See :class:`BaseTrack` for details on arguments.
        """
        super(SuperTrack, self).__init__(*args, **kwargs)
        self.subtracks = []

    def add_tracks(self, subtracks):
        """
        Add one or more tracks.

        subtrack : Track or iterable of Tracks
        """
        if isinstance(subtracks, Track):
            subtracks = [subtracks]
        for subtrack in subtracks:
            self.add_child(subtrack)
            self.subtracks.append(subtrack)

    def __str__(self):

        s = []

        s.append(super(SuperTrack, self).__str__())
        s.append('superTrack on')

        # Removed subtracks for Supertrack because composite tracks can be
        # within the supertrack.  This is also the recommendation from UCSC
        for subtrack in self.subtracks:
            s.append("")
            for line in str(subtrack).splitlines(False):
                s.append(line)
        return '\n'.join(s)


class AggregateTrack(BaseTrack):
    def __init__(self, aggregate, *args, **kwargs):
        """
        Represents an Aggregate or Overlay track. Subclasses :class:`Track`,
        adds some extras.

        Aggregate tracks allow closley related tracks to be viewed as a single
        track.

        Eventually, you'll need to make a :class:`trackdb.TrackDb` instance and
        add this aggregate track to it with that instance's :meth:`add_tracks`
        method.

        Parameters
        ----------

        aggregate : str
            Aggregate type. One of "transparentOverlay", "stacked",
            "solidOverlay". See
            https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html#aggregate
            for details.

        See :class:`BaseTrack` for details on other arguments.
        """

        self.aggregate = aggregate
        kwargs['aggregate'] = aggregate
        super(AggregateTrack, self).__init__(*args, **kwargs)
        self.specific_params.update(constants.aggregate_track_fields)
        self.subtracks = []

    def add_subtrack(self, subtrack):
        """
        Add a child :class:`SubTrack` to this aggregrate.
        """
        self.add_child(subtrack)
        self.subtracks.append(subtrack)

    def __str__(self):

        s = []

        s.append(super(AggregateTrack, self).__str__())
        s.append('container multiWig')

        for subtrack in self.subtracks:
            s.append("")
            for line in str(subtrack).splitlines(False):
                s.append('    ' + line)
        return "\n".join(s)


class HTMLDoc(HubComponent):
    def __init__(self, contents, filename=None):
        """
        Represents an HTML file used for documentation.

        Handles local/remote/url filenames when connected to a Track and
        CompositeTrack
        """
        self.contents = contents
        self._filename = None
        super(HTMLDoc, self).__init__()

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename
        if self.trackdb is None or self.track is None:
            return None
        return os.path.join(
            os.path.dirname(self.trackdb.filename),
            self.track.name + '.html')

    @filename.setter
    def filename(self, fn):
        self._filename = fn

    @property
    def trackdb(self):
        obj, level = self.root(cls=trackdb.TrackDb)
        return obj

    @property
    def track(self):
        obj, level = self.root(cls=BaseTrack)
        return obj

    def _render(self, staging='staging'):
        self.validate()
        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        fout = open(os.path.join(staging, self.filename), 'w')
        fout.write(str(self))
        fout.close()
        return fout.name

    def validate(self):
        if not self.trackdb:
            raise ValueError("HTMLDoc object must be connected to a "
                             "BaseTrack subclass instance and a TrackDb "
                             "instance")
        return True

    def __str__(self):
        return self.contents
