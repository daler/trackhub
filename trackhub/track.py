from __future__ import absolute_import

import os
import re
import warnings
from docutils.core import publish_parts
from trackhub.base import HubComponent, deprecation_handler
from trackhub import hub
from trackhub import constants
from trackhub import settings


TRACKTYPES = ['bigWig', 'bam', 'bigBed', 'vcfTabix', 'bigNarrowPeak', None,
              'bigBarChart', 'bigChain', 'bigGenePred', 'bigNarrowPeak',
              'bigMaf', 'bigPsl', 'halSnake']


def _check_name(name):
    regex = re.compile('[^a-zA-Z0-9-_]')
    if regex.search(name):
        raise ValueError('Non-alphanumeric character in name "%s"' % name)


class ParameterError(Exception):
    pass


def update_list(existing, new, first=constants.initial_params):
    """
    Extend a list, but with constraints.

    Returned list is sorted alphabetically, except for any items that are in
    `first`, which will come first regardless of sorting.

    Parameters
    ----------
    existing : list
        List to extend

    new : list
        Update `existing` with this

    first : list or None
        If provided, ensure that this list occurs at the beginning. Items must
        already be in `existing` or `new`, others are ignored.
    """
    if first is None:
        first = []

    combined = set(existing + new)
    beginning = [i for i in first if i in combined]
    end = sorted(combined.difference(first))

    return beginning + end


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
    def __init__(self, name, tracktype=None, short_label=None,
                 long_label=None, subgroups=None, source=None, filename=None,
                 html_string=None, html_string_format="rst", track_type_override=None, **kwargs):
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

        subgroups : dict
            A dictionary of `{name: tag}` where each `name` is the name of
            a SubGroupDefinition in a parent :class:`CompositeTrack` and each
            `tag` is a key in the SubGroupDefinition.mapping dictionary. The
            dictionary `{'celltype': 'ES'}` would end up looking like this in
            the string representation::

                subGroups celltype=ES

            or like this, if the track had been added to a ViewTrack whose name
            is `aln`::

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

        html_string : str
            String containing documentation for a track. By default, the format
            is assumed to be ReStructured Text format, use
            `html_string_format="html"` if the documentation is already in HTML
            format.

        html_string_format : 'html' or 'rst'
            Indicates the format of `html_string`. If `"html"`, then use as-is;
            if `"rst"` then convert ReST to HTML.

        track_type_override : str
            Composite tracks can specify a tracktype of their children, but we
            also need to know that it's a composite track. For composite tracks,
            this can be set to "compositeTrack":

        """
        source, filename = deprecation_handler(source, filename, kwargs)
        HubComponent.__init__(self)
        _check_name(name)
        self.name = name

        # Dictionary where keys are parameter names (e.g., "color") and values
        # are Param objects.  These are defined in the constants module. To
        # start, we add the params valid for all tracks.
        #
        # The Track subclass will add its own parameters when the track type is
        # set. Other subclasses (Composite and View) will add their own special
        # params in the class definition.
        self.track_field_order = []
        self.track_field_order = update_list(self.track_field_order,
                                             constants.track_fields['all'])

        self.track_type_override = track_type_override

        # NOTE: when setting track type, it will update the track field order
        # according to the known params for that track...so
        # self.track_field_order needs to exist first.
        self.tracktype = tracktype
        if short_label is None:
            short_label = name
        self.short_label = short_label
        if long_label is None:
            long_label = short_label
        self.long_label = long_label

        self._source = source
        self._filename = filename
        self.html_string = html_string
        self.html_string_format = html_string_format
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
        _html = HTMLDoc(self.html_string, self.html_string_format)
        _html.add_parent(self)
        return _html

    @property
    def trackdb(self):
        from trackhub import TrackDb
        return self.root(TrackDb)[0]

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

        # E.g., bigBed 6+3
        base_tracktype = tracktype.split()[0]

        fields = []
        if self.track_type_override:
            for t in self.track_type_override:
                fields.extend(constants.track_fields[t])
        else:
            fields.extend(constants.track_fields[base_tracktype])
        self.track_field_order = update_list(self.track_field_order, fields)

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

        E.g.::

            add_params(color='128,0,0', visibility='dense')

        """
        for k, v in kw.items():
            if k not in self.track_field_order and constants.VALIDATE:
                raise ParameterError(
                    '"{0}" is not a valid parameter for {1} with '
                    'tracktype {2}'
                    .format(k, self.__class__.__name__, self.tracktype)
                )
            if not constants.param_dict[k].validate(v) and constants.VALIDATE:
                raise ParameterError(
                    'value "{0}" did not validate for parameter "{1}"'
                    .format(k, v))

        self._orig_kwargs.update(kw)
        self.kwargs = self._orig_kwargs.copy()

    def remove_params(self, *args):
        """
        Remove [possibly many] parameters from the track.

        E.g.::

            remove_params('color', 'visibility')
        """
        for a in args:
            self._orig_kwargs.pop(a)
        self.kwargs = self._orig_kwargs.copy()

    def add_subgroups(self, subgroups):
        """
        Update the subgroups for this track.

        Note that in contrast to :meth:`CompositeTrack`, which takes a list of
        :class:`SubGroupDefinition` objects representing the allowed subgroups,
        this method takes a single dictionary indicating the particular
        subgroups for this track.

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
        kwargs = self.kwargs.copy()
        for name in self.track_field_order:
            value = kwargs.pop(name, None)
            if name == 'parent':
                if isinstance(self.parent, BaseTrack):
                    if value is not None:
                        s.append('parent {0} {1}'.format(self.parent.name, value))
                    else:
                        s.append('parent {0}'.format(self.parent.name))
                continue

            if name == 'bigDataUrl' and value is None:
                # fall back to `url` if set
                value = getattr(self, 'url', None)

            if value is not None:
                if constants.param_dict[name].validate(value) or not settings.VALIDATE:
                    s.append("%s %s" % (name, value))

                else:
                    raise ParameterError(
                        "The value '{0}' did not validate for parameter '{1}'"
                        .format(value, name))
        # Handle subgroups differently depending on if this is a composite
        # track or not.
        s.extend(self._str_subgroups())

        if settings.VALIDATE:
            if len(kwargs) > 0:
                raise ParameterError(
                    "The following parameters are unknown for track type {0}: "
                    "{1}".format(self.tracktype, kwargs))
        else:
            for k, v in kwargs.items():
                s.append("%s %s" % (k, v))

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
            raise ValueError(self.filename)


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
        add this composite to it with :meth:`trackdb.TrackDb.add_tracks()`. If
        you're using subgroups, use the :meth:`CompositeTrack.add_subgroups()`
        method.

        See :class:`BaseTrack` for details on arguments. There are no
        additional arguments supported by this class.
        """
        super(CompositeTrack,
              self).__init__(track_type_override=['compositeTrack',
                                                  'subGroups'], *args,
                             **kwargs)

        self.track_field_order = update_list(
            self.track_field_order, constants.track_fields['compositeTrack'])

        # TODO: are subtracks and views mutually exclusive, or can a composite
        # have both "view-ed" and "non-view-ed" subtracks?
        self.subtracks = []
        self.views = []

    def add_subgroups(self, subgroups):
        """
        Add a list of SubGroupDefinition objects to this composite.

        Note that in contrast to :meth:`BaseTrack`, which takes a single
        dictionary indicating the particular subgroups for the track, this
        method takes a list of :class:`SubGroupDefinition` objects representing
        the allowed subgroups for the composite.

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
        self.track_field_order = update_list(
            self.track_field_order, constants.track_fields['view'])
        self.subtracks = []

    def add_tracks(self, subtracks):
        """
        Add one or more tracks to this view.

        subtracks : Track or iterable of Tracks
            A single Track instance or an iterable of them.
        """
        if isinstance(subtracks, BaseTrack):
            subtracks = [subtracks]
        for subtrack in subtracks:
            subtrack.subgroups['view'] = self.view
            self.add_child(subtrack)
            self.subtracks.append(subtrack)

    def __str__(self):
        s = []
        s.append(super(ViewTrack, self).__str__())

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
        super(SuperTrack, self).__init__(tracktype='superTrack', *args, **kwargs)
        self.track_field_order = update_list(
            self.track_field_order, constants.track_fields['superTrack'])

        self.subtracks = []

    def add_tracks(self, subtracks):
        """
        Add one or more tracks.

        subtrack : Track or iterable of Tracks
        """
        if isinstance(subtracks, BaseTrack):
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
        self.track_field_order = update_list(
            self.track_field_order, constants.track_fields['multiWig'])
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
    def __init__(self, contents, html_string_format, filename=None):
        """
        Represents an HTML file used for documentation.

        Handles local/remote/url filenames when connected to a Track and
        CompositeTrack

        Parameters
        ----------

        contents : str
            String of contents for HTML file. Expected format determined by
            `html_string_format`.

        html_string_format : 'html' | 'rst'
            If "html", write an HTML file with no additional modification. If
            "rst", assumes `contents` is in ReStructured Text format and is
            converted to HTML.

        filename : str or None
            If None, the rendered HTML filename will be the name of the parent
            track with an ".html" extension, in the same directory as the
            parent TrackDb.
        """
        self.contents = contents
        self.html_string_format = html_string_format
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
        from trackhub import TrackDb
        obj, level = self.root(cls=TrackDb)
        return obj

    @property
    def track(self):
        return self.parent

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
        if self.html_string_format == 'html':
            return self.contents
        elif self.html_string_format == 'rst':

            # docutils still internally uses a "U" mode for opening files.
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                parts = publish_parts(
                    self.contents, writer_name='html',
                    settings_overrides={'output_encoding': 'unicode'}
                )
            return parts['html_body']
        else:
            raise ValueError(
                "html_string_format '{}' not supported".format(
                    self.html_string_format)
            )
        return self.contents
