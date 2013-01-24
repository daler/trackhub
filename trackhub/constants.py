try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
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
            'colorByStrand',
            """
            red, green, blue  red, green, blue values 0 to 255;
            specifies plus and minus strand color, first rgb is plus
            strand, second rgb is minus strand
            """,
            # NOTE: BED 6 or higher
            validate.RGBList),

        Parameter(
            'denseCoverage',
            """
            in dense mode, do a density plot based on max coverage seen under
            pixel. The maxVal corresponds to the count at which it gets as dark
            as it can get. If maxVal is 0 then this will be calculated from the
            data itself.""",
            int),

        Parameter(
            'exonArrow',
            """
            on|off; shows arrows on blocks allowing user to navigate to next
            block for an item outside the image currently displayed (Default:
            on)
            """,
            # NOTE: BED 10 or higher
            set(['on', 'off'])),

        Parameter(
            'scoreFilter',
            """default score filter value for a track which excludes scores
            below threshold""",
            # TODO: Verify documentation confusion, possibly could be using
            # range
            int),

        Parameter(
            'scoreFilterLimits',
            """
            low[:high]; range that score is filtered between, score value
            N imples N:1000 (Default 0:1000)
            """,
            str),

        Parameter(
            'itemRgb',
            """
            on|off; activates item coloring based on ninth field (Default: off)
            """,
            # NOTE: BED 9 or higher
            set(['on', 'off'])),

        Parameter(
            'maxItems',
            """
            integer defining threshold of items to display in full mode and
            number of lines to display in pack mode. (Default: 250, can't be
            larger than 100,000)
            """,
            # TODO: Improve verification to check that values is less than
            # 100,000
            int),

        Parameter(
            'minGrayLevel',
            """
            1-9; specifies the lightest shade to be used
            """,
            # TODO: Need to look up better verification for range
            int),

        Parameter(
            'noScoreFilter',
            """
            on|off; turns off filter on score configuration options in UI
            (Default: off)
            """,
            # TODO: Add additional verification that checks that type has + or
            # .
            set(['on', 'off'])),


        Parameter(
            'spectrum',
            'use score to shade color items',
            # NOTE: BED 5 or higher
            'on'),

        Parameter(
            'scoreMax',
            'defines upper score limit that will receive graded scoring',
            # NOTE: BED 5 or higher, used with spectrum
            int),

        Parameter(
            'scoreMin',
            'defines lower score limit that will receive graded scoring',
            # NOTE: BED 5 or higher, used with spectrum
            int),

        Parameter(
            'thickDrawItem',
            """
            on|off; draw portions of items thicker to differentiate from
            other regions (Default: off)
            """,
            # NOTE: BED 8 or higher
            set(['on', 'off'])),

        # Less frequent used options

        Parameter(
            'bedNameLabel',
            """
            specifies an alternate label for the item name
            """,
            str),

        Parameter(
            'exonArrowDense',
            """
            on|off; display exon arrows even when the
            track is in dense mode (Default: off)
            """,
            # NOTE: BED 10 or higher
            set(['on', 'off'])),

        Parameter(
            'itemImagePath',
            """
            path suffix; specifies a URL or relative path to track
            that displays image on item details page
            """,
            str),

        Parameter(
            'itemBigImagePath',
            """
            path suffix; specifies a URL or relative path to track
            that provides link to bigger image if itemImagePath
            is specified
            """,
            str),

        Parameter(
            'nextExonText',
            """
            specifies an alternate label, when mousing over
            next exon arrows
            """,
            # NOTE: BED 10 or higher
            str),

        Parameter(
            'prevExonText',
            """
            specifies an alternate label, when mousing over
            previous exon arrows
            """,
            # NOTE: BED 10 or higher
            str),

        Parameter(
            'showTopScores',
            """
            integer specifying a list of top-scoring items
            in genomic region on the item details page
            """,
            # NOTE: BED 5 or higher
            int),

    ]),

    'bigWig': OrderedDict((i.param, i) for i in [

        Parameter(
            'alwaysZero',
            """
            on|off; when autoScale is on, this setting
            ensures that y=0 is in the view (Default: off)
            """,
            set(['on', 'off'])),

        Parameter(
            'autoScale',
            """
            on|off; auto y-axis scaling to ensure that
            highest score in the current widow will
            peak at the top of the window (Default: off)
            """,
            set(['on', 'off'])),

        Parameter(
            'graphTypeDefault',
            """
            points|bars; signal can be graphed as points
            or bars (Default: bars)
            """,
            set(['points', 'bars'])),

        Parameter(
            'maxHeightPixels',
            """
            max:default:min; amount of vertical viewing space
            (Default: 100:16:8)
            """,
            validate.ColSV3),

        Parameter(
            'maxWindowToQuery',
            """
            a (large) positive number; if winEnd-winStart is larger, don't
            query items
            """,
            int),

        Parameter(
            'smoothingWindow',
            """
            off|1-16; smoothing of graph using surrounding data,
            the numeric number determines how much surrounding data
            to use (Default: off_
            """,
            validate.off_or_int),

        Parameter(
            'transformFunc',
            'NONE|LOG; change representation scale (Default: NONE)',
            set(['NONE', 'LOG'])),

        Parameter(
            'viewLimits',
            "lower:upper; set default viewing range",
            # NOTE: autoScale must be off for this to work
            validate.ColSV2),

        Parameter(
            'viewLimitsMax',
            'lower:upper; unenforced -- suggested bounds of viewLimits',
            validate.ColSV2),

        Parameter(
            'windowingFunction',
            """
            mean|mean+whiskers|maximum|minimum; how to summarize signal
            data
            """,
            set(['maximum', 'mean', 'mean+whiskers', 'minimum'])),

        Parameter(
            'yLineMark',
            'float; position on y-axis to draw line across (Default: 0.0)',
            float),

        Parameter(
            'yLineOnOff',
            """on|off; draw y line at some fixed position set by yLineMark
            (Default: off)""",
            set(['on', 'off'])),

        Parameter(
            'gridDefault',
            "on|off; draw y=0.0 line (Default: off)",
            set(['on', 'off'])),

    ]),

    'bam':  OrderedDict((i.param, i) for i in [
        Parameter(
            'bamColorMode',
            """
            strand|gray|tag|off; coloring method (Default: strand)
            """,
            set(['strand', 'gray', 'tag', 'off'])),

        Parameter(
            'bamGrayMode',
            """
            aliQual|baseQual|unpaired; grayscale metric (Default: aliQual)
            """,
            # NOTE: bamColorMode gray
            set(['aliQual', 'baseQual', 'unpaired'])),

        Parameter(
            'aliQualRange',
            'min:max; shade alignment quals within this range (Default: 0:99)',
            validate.ColSV2),

        Parameter(
            'baseQualRange',
            'min:max; shade base quals within this range (Default: 0:40)',
            validate.ColSV2),

        Parameter(
            'bamColorTag',
            'optional tag for rgb color (Default: YC)',
            # NOTE: bamColorMode tag
            str),

        Parameter(
            'noColorTag',
            """
            placeholder, e.g. "."; if present don't offer option of setting
            color tag in track configuration page""",
            str),

        Parameter(
            'bamSkipPrintQualScore',
            """
            skip printing qual score in bam item details page; use "." to skip
            printing""",
            '.'),

        Parameter(
            'indelDoubleInsert',
            """
            on|off; highlight alignment gaps in target and query sequence
            with = (Default: 0ff)
            """,
            set(['on', 'off'])),

        Parameter(
            'indelQueryInsert',
            """
            on|off; highlight inserts in query sequence with
            orange or purple vertical lines (Default: off)
            """,
            set(['on', 'off'])),

        Parameter(
            'indelPolyA',
            """
            on|off; highlight poly-a tail with a vertical green line
            (Default: off)
            """,
            set(['on', 'off'])),

        Parameter(
            'minAliQual',
            'display only items above threshold quality score (Default: 0)',
            int),

        Parameter(
            'pairEndsByName',
            """
            if data has paired-end tags joined by name; use "."
            """,
            '.'),

        Parameter(
            'pairSearchRange',
            """
            search range to join pairs of tags (Default: 20000)
            """,
            int),

        Parameter(
            'showNames',
            "on|off; if off then don't display query names (Default: on)",
            set(['on', 'off'])),


        # Undocumented stuff, found from
        # https://lists.soe.ucsc.edu/pipermail/genome/2012-June/029615.html
        #
        # Uploading BAM files directly showed indels, but not when the same
        # file was included in a track hub.
        #
        # Currently not supported for bigBed
        Parameter(
            'baseColorUseSequence',
            'for BAM, try "lfExtra"; <extFile {seqTable} <extFile> / hgPcrResult / lfExtra / nameIsSequence / seq1Seq2 / ss >',
            set(['extFile', 'hgPcrResult', 'lfExtra', 'nameIsSequence', 'seq1Seq2', 'ss'])),

        Parameter(
            'baseColorDefault',
            '<diffBases/diffCodons/itemBases/itemCodons/genomicCodons>',
            set(['diffBases', 'diffCodons', 'itemBases', 'itemCodons', 'genomicCodons'])),

        Parameter(
            'showDiffBasesAllScales',
            '.',
            set(['.'])),





    ]),

    'vcfTabix': OrderedDict((i.param, i) for i in [
        # No Special Configuration for vcfTabix, uses maxWindowToDraw

    ]
    ),

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
        ABC dimensions are represented by filter-like drop-downs.  Can be "on",
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
        # TODO: better verification
        str),

    Parameter(
        'sortOrder',
        'sort order for composite, e.g., cellType=+ factor=-',
        str),

    Parameter(
        'centerLabelsDense',
        'show subtrack labels even in dense view',
        set(['on', 'off'])),

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

aggregate_track_fields = OrderedDict((i.param, i) for i in [
    Parameter(
        'aggregate',
        """
        transparentOverlay|solidOverlay|none; declares aggregate method
        """,
        set(['transparentOverlay', 'solidOverlay', 'none'])),

    Parameter(
        'showSubtrackColorOnUi',
        """
        on|off; show color associated with each track on the
        configuration page (Default: off)
        """,
        set(['on', 'off'])),

])

track_fields = OrderedDict((i.param, i) for i in [

    # Common Settings
    Parameter(
        'visibility',
        """hide|dense|squish|pack|full;default visibility for this track
        (Default: hide)""",
        set(['hide', 'dense', 'squish', 'pack', 'full'])
    ),

    Parameter(
        'html',
        """
        optional file containing description of a track in HTML and is path is
        relative to the path of trackDb file track is in.
        """,
        str),

    # Common Optional Settings
    Parameter(
        'boxedCfg',
        """
        on|off; places configuration controls within a box, much like
        multi-view controls have (Default: off)""",
        set(['on', 'off'])),

    Parameter(
        'color',
        'red, green, blue values 0 to 255; specifies primary color for items',
        validate.RGB),

    Parameter(
        'altColor',
        """
        red, green, blue values 0 to 255; specifies secondary color for
        items""",
        validate.RGB),

    Parameter(
        'chromosomes',
        """
        chr1, chr3; only these chroms have data for this track, the system
        displays message that there is no data on other chroms
        """,
        validate.CSV),

    Parameter(
        'dataVersion',
        """
        display a version statement for this track on configuration and details
        pages, supports limited HTML
        """,
        str),

    Parameter(
        'directUrl',
        """
        url;
        link image to alternative details page using these fields in order:
        item name, chromosome name, chromosome start position, chromosome end
        position, track name, database name;
        """,
        # TODO: better verification and information
        str),

    Parameter(
        'otherDb',
        'declare the other species/assembly used in the pairwise alignments',
        # TODO: determine if functionality works for bigBed
        str),

    Parameter(
        'pennantIcon',
        """
        icon [html [tip]]; Displays icon next to track in "parade" of tracks
        found in hgTracks config. Html is an optional page describing the icon
        and path can be relative to the track or absolute. Tip is an optional
        "quoted string" that is seen when the user hovers over the icon.
        """,
        str),

    Parameter(
        'priority',
        """
        used to order this track within its track group and within the browser
        image, tracks of the same priority are sorted alphabetically by short
        label.  (Default: 0)
        """,
        float),

    Parameter(
        'url',
        'url; place an external link on the details page',
        # TODO: improved verification and information on coding
        str),

    Parameter(
        'url2',
        'url; place an additional external link on the details page',
        # TODO: improved verification and information on coding
        str),

    Parameter(
        'urlLabell',
        """
        used with url setting and provides text for link (Default: "outside
        link:")
        """,
        str),

    Parameter(
        'url2Label',
        """
        used with url2 setting and provides text for link (Default: "outside
        link")
        """,
        str),


    # Across datatype Settings

    Parameter(
        'maxWindowToDraw',
        """
        a (large) positive number; if winEnd-winStart is larger than threshold
        forces track to dense mode""",
        int),


    Parameter(
        'configurable',
        """
        on|off; on for all track types that allow configuration.  If set to
        off, configuration is blocked.  This setting is most useful in
        composites and views where some subtracks should be configurable and
        others not. (Default: on)""",
        set(['on', 'off'])),


])
