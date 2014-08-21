import sys
import os
import re
from validate import ValidationError
from base import HubComponent
import hub
import trackdb
import genomes_file
import genome
import constants

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


TRACKTYPES = ['bigWig', 'bam', 'bigBed', 'vcfTabix', None]


def _check_name(name):
    regex = re.compile('[^a-zA-Z0-9-_.]')
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

        :param name:
            String; name for the subgroup (e.g., "celltype").

        :param label:
            String; the label that will be displayed (e.g., "Cell_Type")

        :param mapping:
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

        :param default:
            String; value to be used by subtracks if they don't explicitly
            define this subgroup. Continuing the example, if a subtrack didn't
            specify the "celltype" subgroup, then by default a "celltype=none"
            value will be added.  This is necessary because subtracks must
            define a value for all groups.
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
                 long_label=None, subgroups=None, local_fn=None,
                 remote_fn=None, html_string=None, **kwargs):
        """
        Represents a single track stanza.

        :param name: String; name of the track

        :param tracktype: String; type of the track (e.g., "bam")

        :param url: String; full URL for the track (i.e., bigDataUrl)

        :param short_label: String; used for the left-hand side track label

        :param long_label:
            String; used for the longer middle labels; if None will copy
            short_label

        :param subgroups:

            A dictionary of `{name: tag}` where each `name` is the name of
            a SubGroupDefinition in a parent :class:`CompositeTrack` and each
            `tag` is a key in the SubGroupDefinition.mapping dictionary.  They
            end up looking like this in the string representation::

                subGroups view=aln celltype=ES

        :param local_fn:
            String; Local path to the file (used for uploading)

        :param remote_fn:
            String; path to upload the file to, over rsync and ssh.
        """
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

        self._local_fn = local_fn
        self._remote_fn = remote_fn
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
    def local_fn(self):
        if self._local_fn is not None:
            return self._local_fn
        return None

    @local_fn.setter
    def local_fn(self, fn):
        self._local_fn = fn

    @property
    def remote_fn(self):
        if self._remote_fn is not None:
            return self._remote_fn
        # If remote_fn hasn't been assigned then make one automatically based
        # on the track name and the trackhub's remote_fn (which, by the way,
        # acts similarly, deferring up to the genomes_file.remote_fn . . . and
        # so on up to the hub's remote_fn)
        if self.trackdb:
                return os.path.join(
                    os.path.dirname(self.trackdb.remote_fn),
                    self.name + '.' + self.tracktype.split(' ')[0])
        return None

    @remote_fn.setter
    def remote_fn(self, fn):
        self._remote_fn = fn

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

        :param subgroups:
            Dictionary of subgroups, e.g., {'celltype': 'K562', 'treatment':
                'a'}.  Each key must match a SubGroupDefinition name in the
                composite's subgroups list.  Each value must match a key in
                that SubGroupDefinition.mapping dictionary.
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
                s.append('parent %s' % self.parent.name)

        if len(self.kwargs) > 0:
            raise ParameterError(
                "Unhandled keyword arguments: %s" % self.kwargs)

        self.kwargs = self._orig_kwargs.copy()
        return '\n'.join(s)

    def _render(self):
        if self._html:
            self._html.render()

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
        #assert self.tracktype in TRACKTYPES

    @property
    def html_fn(self):
        if self.remote_fn and self.trackdb:
            return os.path.join(
                os.path.dirname(self.trackdb.remote_fn),
                self.name + '.html')
        else:
            return None


class Track(BaseTrack):
    def __init__(self, url=None, *args, **kwargs):
        kwargs['bigDataUrl'] = kwargs.get('bigDataUrl', url)
        super(Track, self).__init__(*args, **kwargs)
        self._url = url

    @property
    def url(self):
        if self._url is not None:
            return self._url
        if self.remote_fn is None:
            return None
        return os.path.relpath(
            self.remote_fn,
            start=os.path.dirname(self.trackdb.remote_fn)
        )

    @url.setter
    def url(self, fn):
        self._url = fn


class CompositeTrack(BaseTrack):

    def __init__(self, *args, **kwargs):
        """
        Represents a composite track.  Subclasses :class:`Track`, and adds some
        extras.

        Add a view to this composite with :meth:`add_view`.

        Add a subtrack with :meth:`add_track`.

        Eventually, you'll need to make a :class:`trackdb.TrackDb` instance and
        add this composite to it with that instance's :meth:`add_tracks`
        method.

        If composite=True, then this track will be consider a composite
        parent for other tracks.  In this case, `subgroups` is a list of
        :class:`SubGroupDefinition` objects, each defining the possible
        values and display labels for the items in a group (for example,
        a celltype SubGroupDefinition would define the tags and titles for
        cell types).  In the string representation of this Track, subgroups
        end up looking like::

            subGroup1 view Views aln=Alignments sig=Signal
            subGroup2 celltype Cell_Type ES=embryonic k562=K562
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
        Add a child :class:`SubTrack`.
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
        Represents a View track.  Subclasses :class:`Track`, and adds some
        extras.

        Upon being added to a CompositeTrack, the `view` tag will be checked.
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
        Add tracks to this view.

        :param subtracks:
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
        """
        super(SuperTrack, self).__init__(*args, **kwargs)
        self.subtracks = []

    def add_track(self, subtrack):
        """
        Add a child :class:`SubTrack` to this supertrack.
        """
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
        add this supertrack to it with that instance's :meth:`add_tracks`
        method.
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
    def __init__(self, contents):
        """
        Represents and HTML file used for documentation.

        Handles local/remote/url filenames when connected to a Track and
        CompositeTrack
        """
        self.contents = contents
        self._local_fn = None
        self._remote_fn = None
        super(HTMLDoc, self).__init__()

    def validate(self):
        return

    @property
    def local_fn(self):
        if (self.trackdb is None) or (self.track is None):
            return None
        return os.path.join(
            os.path.dirname(self.trackdb.local_fn),
            self.track.name + '.html')

    @property
    def remote_fn(self):
        if (self.trackdb is None) or (self.track is None):
            return None
        return os.path.join(
            os.path.dirname(self.trackdb.remote_fn),
            self.track.name + '.html')

    @property
    def trackdb(self):
        obj, level = self.root(cls=trackdb.TrackDb)
        return obj

    @property
    def track(self):
        obj, level = self.root(cls=BaseTrack)
        return obj

    def _render(self):
        if not self.trackdb:
            raise ValueError("HTMLDoc object must be connected to a "
                             "BaseTrack subclass instance and a TrackDb "
                             "instance")
        dirname = os.path.dirname(self.local_fn)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        fout = open(self.local_fn, 'w')
        fout.write(str(self))
        fout.close()
        return fout.name

    def __str__(self):
        return self.contents
