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
            block for an item outside the image currently displayed (Default: on)
            """,
            # NOTE: BED 10 or higher
            set(['on', 'off']),

        Parameter(
            'scoreFilter',
            ' default score filter value for a track which excludes scores below threshold',
            # TODO: Verify documentation confusion, possiblely could be using range
            int),

        Parameter(
            'scoreFilterLimits',
            """
            low[:high]; range that score is filter between, score value N imples N:1000 
            (Default 0:1000)
            """,
            str,)

        Parameter(
            'itemRgb',
            'on|off; activates item coloring based on ninth field (Default: off)',
            # NOTE: BED 9 or higher
            set(['on', 'off'])),

        Parameter(
            'maxItems',
            """
            integer defining threshold of items to display in full mode and number of
            lines to display in pack mode. (Default: 250, can't be larger than 100,000)
            """,
            # TODO: Improve verification to check that values is less than 100,000
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
            on|off; turns off filter on score configuration options in UI (Default: off) 
            """,
            # TODO: Add additional verification that checks that type has + or .
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
            'defines lower score limit that will recieve graded scoring',
            # NOTE: BED 5 or higher, used with spectrum
            int),
        
        Parameter(
            'thickDrawItem',
            """
            on|off; draw portions of items thicker to differentiate from
            other regions (Default: off)
            """,
            # NOTE: BED 8 or higher
            set(['on', 'off']),

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
            'maxWindowToQuery',
            """
            a (large) positive number; if winEnd-winStart is larger, don't query
            items
            """,
            int),

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
    ]),

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
        # No Special Configuration for vcfTabix, uses maxWindowToDraw
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
        # TODO: better verification
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
    
    # Common Settings
    Parameter(
        'visibility',
        'hide|dense|squish|pack|full;default visibility for this track (Default: hide)',
        set(['hide', 'dense', 'squish', 'pack', 'full'])
    ),
    
    Parameter(
        'html',
        """
        optional file containg description of a track in HTML and is path is relative
        to the path of trackDb file track is in. 
        """,
        str),

    # Common Optional Settings
    Parameter(
        'boxedCfg',
        """
        on|off; places configuration controls within a box, much like multi-view controls
        have (Default: off)""",
        set(['on', 'off'])),

    Parameter(
        'color',
        'red, green, blue values 0 to 255; specifies primary color for items',
        validate.RGB),

    Parameter(
        'altColor',
        'red, green, blue values 0 to 255; specifies secondary color for items',
        validate.RGB),

    Parameter(
        'chromosomes',
        """
        chr1, chr3; only these chroms have data for this track, the system displays
        message that there is no data on other chroms
        """,
        validate.CSV),
    
    Parameter(
        'dataVersion',
        """
        display a version statment for this track on configruation and details pages, 
        supports limited HTML
        """,
        str),

    Paremeter(
        'directUrl',
        """
        url;
        link image to alternative detials page using these fields in order:
        item name, chromosome name, chromosome start position, chromosome end position, track name, database name;
        """,
        # TODO: better verification and information
        str),
    
    Parameter(
        'otherDb',
        'declare the other species/assembly used in the pariwise alingments',
        # TODO: determine if functionaitly works for bigBed
        str),

    Parameter(
        'pennantIcon',
        """
        icon [html [tip]]; Displays icon next to track in "parade" of tracks
        found in hgTracks config. Html is an optional page describing the icon 
        and path can be relative to the track or absolute. Tip is an optional "quoted string"
        that is seen when the user hovers over the icon.
        """,
        str),
 
    Parameter(
        'priority',
        """
        used to order this track within its track group and within the browser image,
        tracks of the same priority are sorted alphabetically by short label.
        (Default: 0)
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
        used with url setting and provides text for link (Default: "outside link:")
        """,
        str),

    Parameter(
        'url2Label',
        """
        used with url2 setting and provides text for link (Default: "outside linl:")
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


])
