from collections import OrderedDict
from validate import Parameter
import validate

# http://genome-source.cse.ucsc.edu/gitweb/
#       ?p=kent.git;a=blob;f=src/hg/makeDb/trackDb/README;hb=HEAD


track_field_order = OrderedDict((i.param, i) for i in [
    Parameter(
        'track',
        "track name",
        str),
    Parameter(
        'bigDataUrl',
        "URL",
        str),
    Parameter(
        'shortLabel',
        "label used on left-side labels",
        str),
    Parameter(
        'longLabel',
        'label used in center',
        str),
    Parameter(
        'type',
        'track type',
        # TODO: better validation here for things like bed 3
        str),
])

track_typespecific_fields = {
    None: (),

    'bigBed': OrderedDict((i.param, i) for i in [
        Parameter(
            'denseCoverage',
            """
            in dense mode, do a density plot based on max coverage seen under
            pixel. The maxVal corresponds to the count at which it gets as dark
            as it can get. If maxVal is 0 then this will be calculated from the
            data itself.""",
            int),

        Parameter(
            'nonBedFieldsLabel',
            """
            text heading string printed on item details page before display of
            non-bed type fields.  Default is 'Non-BED fields:'""",
            str),
    ]),
    'bigWig': OrderedDict((i.param, i) for i in [
        Parameter(
            'autoScale',
            "auto y-axis scaling",
            set(['on', 'off'])),
        Parameter(
            'gridDefault',
            "draw y=0.0 line",
            set(['on', 'off'])),

        Parameter(
            'maxHeightPixels',
            "max:default:min; default is 128:128:11",
            validate.ColSV3),

        Parameter(
            'graphType',
            "bar or points; default bar",
            set(['bar', 'points'])),

        Parameter(
            'viewLimits',
            "default is from the type line limits; lower:upper.",
            validate.ColSV2),

        Parameter(
            'viewLimitsMax',
            'lower:upper; unenforced -- suggested bounds of viewLimits',
            validate.ColSV2),

        Parameter(
            'yLineMark',
            'float; draw line here',
            float),

        Parameter(
            'yLineOnOff',
            'on|off; draw y line',
            set(['on', 'off'])),

        Parameter(
            'alwaysZero',
            'on|off; always show zero values',
            set(['on', 'off'])),

        Parameter(
            'windowingFunction',
            'maximum|mean|minimum',
            set(['maximum', 'mean', 'minimum'])),

        Parameter(
            'smoothingWindow',
            'off or 2-16; default off',
            validate.off_or_int),

        Parameter(
            'transformFunc',
            'NONE|LOG; default NONE',
            set(['NONE', 'LOG'])),

        Parameter(
            'wigColorBy',
            'use colors in bed for wiggle in overlapping regions',
            str),

        Parameter(
            'spanList',
            'sets spans to just be the first span in table',
            str),
    ]
    ),

    'bam':  OrderedDict((i.param, i) for i in [
        Parameter(
            'bamColorMode',
            'coloring method; default is strand',
            set(['strand', 'gray', 'tag', 'off'])),
        Parameter(
            'bamGrayMode',
            'grayscale metric; default aliQual',
            set(['aliQual', 'baseQual', 'unpaired'])),
        Parameter(
            'bamColorTag',
            'optional tag for rgb color; default is YC',
            str),
        Parameter(
            'bamSkipPrintQualScore',
            """
            skip printing qual score in bam item details page; use "." to skip
            printing""",
            '.'),
        Parameter(
            'minAliQual',
            'display only items with qualscore or better; default 0',
            int),
        Parameter(
            'aliQualRange',
            'min:max; shade alignment quals within this range; default 0:99',
            validate.ColSV2),
        Parameter(
            'baseQualRange',
            'min:max; shade base quals within this range; default 0:40',
            validate.ColSV2),
        Parameter(
            'noColorTag',
            """
            placeholder, e.g. "."; if present don't offer option of setting
            color tag in hgTrackUi""",
            str),
        Parameter(
            'showNames',
            "on|off; if off then don't display query names",
            set(['on', 'off'])),
    ]),
    
    'vcfTabix': OrderedDict((i.param, i) for i in [
        Parameter(
            'maxWindowToDraw',
            """
            Forces track to dense mode, summary mode, when a threshold
            number of bases is displayed in the window""",
            int),
        ]),

}


composite_track_fields = OrderedDict((i.param, i) for i in [
    Parameter(
        'noInherit',
        """
        use this when subtracks of a different type are included in this
        composite """,
        'on'),

    Parameter(
        "allButtonPair",
        """
        Add all [=][-] buttons for selecting subtracks""",
        "on"),

    Parameter(
        "filterComposite",
        """
        ABC dimensions are represented by filter-like drop-downs.  can be "on",
        or something like dimB=onlyOne in order to allow only a single
        selection for that dimension, overriding the default of dimB=multi""",
        str),

    Parameter(
        "dragAndDrop",
        """
        enable drag-and-drop subtracks""",
        "subtracks"),

    Parameter(
        'dimensions',
        "dimensionX=factor1 dimensionY=factor2 dimA=rep dimB=prot",
        #TODO: better verification
        str),

    Parameter(
        'sortOrder',
        'sort order for composite, e.g., cellType=+ factor=-',
        str),

])

view_track_fields = OrderedDict((i.param, i) for i in [
    Parameter(
        'view',
        "view tag, defined as a subgroup in parent composite",
        str),
    Parameter(
        'viewUi',
        'if on (default), displays view config settings',
        set(['on', 'off'])),
])

track_fields = OrderedDict((i.param, i) for i in [
    Parameter(
        'visibility',
        'default visibility',
        set(['hide', 'dense', 'squish', 'pack', 'full'])
    ),

    Parameter(
        'onlyVisibility',
        'only this visibility and "hide" are possible for this track',
        set(['hide', 'dense', 'squish', 'pack', 'full'])
    ),
    Parameter(
        'maxWindowToQuery',
        """
        a (large) positive number; if winEnd-winStart is larger, don't query
        items (only bigWig at the moment)""",
        int),

    Parameter(
        'maxWindowToDraw',
        """
        a (large) positive number; if winEnd-winStart is larger, don't draw
        items""",
        int),

    Parameter(
        'group',
        """
        any "name" from the grp table; e.g.: map, genes, rna, regulation,
        compGeno, varRep;  used to specify which group of track controls to
        place this track into""",
        str),

    Parameter(
        'useScore',
        'use score to shade color items',
        "1"),

    Parameter(
        'spectrum',
        'same effect as useScore',
        'on'),

    Parameter(
        'thickDrawItem',
        """
        keep width of bed item at least this many pixels wide even at great
        zoom levels""",
        int),

    Parameter(
        'color',
        'specifies primary color for items. red, green, blue values 0 to 255',
        validate.RGB),

    Parameter(
        'altColor',
        'specifies secondary color for items',
        validate.RGB),

    Parameter(
        'colorByStrand',
        """
        specifies plus and minus strand color as above; first rgb is plus
        strand, second rgb is minus strand. this has no effect for elements
        w/out strand.""",
        validate.RGBList),

    Parameter(
        'priority',
        """
        used to order this track within this track group. if no priority
        line, hgTrackDb sets priority to 100""",
        float),

    Parameter(
        'chromosomes',
        """
        only these chroms have data for this track, this track is not shown
        on other chroms""",
        validate.CSV),

    Parameter(
        'metadata',
        """
        Purely informational.  Gives additional information about a track
        which will be displayed in hgTrackUi and hgc. Especially useful for
        subtracks (see below)""",
        validate.key_val),

    Parameter(
        'boxedCfg',
        """
        puts a box around setting controls, much like multi-view controls
        'have.""",
        'on'),

    Parameter(
        'scoreFilter',
        'default score filter value for a track',
        int),

    Parameter(
        'scoreFilterLimits',
        """
        min:max range that score can take. (default 0:1000.  Single value
        N implies N:1000)""",
        str),

    Parameter(
        'scoreFilterByRange',
        """
        Filter using both upper and lower bounds. (when used, set default
        bounds by 'scoreFilter N:M')""",
        'on'),

    Parameter(
        'scoreFilterMax',
        "deprecated.  Use scoreFilterLimits.",
        int),

    Parameter(
        'noScoreFilter',
        """
        to turn off Ui options for bed 5+ tracks, I don't know what the . is
        for, but it always appears to be used.""",
        "."),

    Parameter(
        'table',
        """
        mySQL table name. Allows multiple tracks to use the same mySQL
        table.  If omitted the mySQL table name is the same as the track name.
        Note that there must be at least one track associated with the table
        where the track name is the same as the table name, or the table
        browser will have difficulties.""",
        str),

    Parameter(
        'configurable',
        """
        Default: on for all track types that allow configuration.  If set to
        off, configuration is blocked.  This setting is most useful in
        composites where some subtracks should be configurable and others
        not.""",
        set(['on', 'off'])),

    Parameter(
        'configureByPopup',
        """
        Default: on for most tracks, off for snp, conservation and multiz
        tracks.  If value is off, hgTracks does not use a modal dialog for
        hgTrackUi, but instead always forces user to hgTrackUi page; this is
        useful for very complicated config pages like dbSnp or multiz which do
        not work well in a modal dialogs, and snp tracks which use javascript
        that is not compatible with modal dialogs. This setting also turns off
        individual subtrack configuration in the composite configuration
        (hgTrackUi) page.""",
        set(['on', 'off'])),

    Parameter(
        'pennantIcon',
        """
        icon [url [hint]]. Displays icon next to track in "parade" of tracks
        found in hgTracks config MAY at some point appear in search tracks and
        next to title in hgTrackUi icon is required and must be in
        htdocs/images.  Url is optional and can be relative to the cgi-bin or
        absolute.  Hint is optional text for a toolTip.  Enclose in quotes for
        readability.""",
        str),
])
