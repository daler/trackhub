"""
These params are organized mostly in order from
https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html. Params are
defined only once, so a param shared across track types is defined in the first
track type we hit.

Once the _params dict is defined, over in constants.py organize them into
track-specific groups.

Note that parser.py has a method of importing the documentation, but it ends up
being easier (and more robust) to just go through the parameters manually.
"""

from .validate import Parameter
from . import validate

_params = {i.name:i for i in [

    # Common settings
    Parameter("track", validate.alphanumeric_),
    Parameter("type", set([
        'bam',
        'bigBed',
        'bigWig',
        'bigPsl',
        'bigMaf',
        'bigNarrowPeak',
        'bigGenePred',
        'bigChain',
        'bigBarChart',
        'halSnake',
        'vcfTabix',
    ])),
    Parameter("shortLabel", validate.short_label),
    Parameter("longLabel", validate.long_label),
    Parameter("bigDataUrl", str),
    Parameter("html", str,),
    Parameter("visibility", set([
        'hide',
        'dense',
        'squish',
        'pack',
        'full'])),

    # Not specified in the database document, but is used in assembly hubs.
    Parameter("group", str),

    # Common optional settings
    Parameter("color", validate.RGB),
    Parameter("priority", float),
    Parameter("altColor", validate.RGBList),
    Parameter("boxedCfg", set(['on', 'off'])),
    Parameter("chromosomes", str,),
    Parameter("darkerLabels", set(['on'])),
    Parameter("dataVersion", str),
    Parameter("directUrl", validate.full_or_local_url),
    Parameter("iframeUrl", validate.full_or_local_url),
    Parameter("iframeOptions", str),
    Parameter("mouseOverField", str),
    Parameter("otherDb", str),
    Parameter("pennantIcon", str),
    Parameter("url", validate.full_url),
    Parameter("urls", validate.key_val),
    Parameter("skipEmptyFields", set(['on'])),
    Parameter("skipFields", validate.key_val),
    Parameter("sepFields", validate.key_val),

    # BAM/CRAM
    Parameter("refUrl", validate.full_url),
    Parameter("bigDataIndex", validate.full_or_local_url),
    Parameter("bamColorMode", set(['strand', 'gray', 'tag', 'off'])),
    Parameter("bamGrayMode", set(['aliQual', 'baseQual', 'unpaired'])),
    Parameter("aliQualRange", validate.ColSV2),
    Parameter("baseQualRange", validate.ColSV2),
    Parameter("bamColorTag", str),
    Parameter("noColorTag", set(['.'])),
    Parameter("bamSkipPrintQualScore", set(['.'])),
    Parameter("indelDoubleInsert", set(['on', 'off'])),
    Parameter("indelQueryInsert", set(['on', 'off'])),
    Parameter("indelPolyA", set(['on', 'off'])),
    Parameter("minAliQual", validate.int_like),
    Parameter("pairEndsByName", set(['.'])),
    Parameter("pairSearchRange", validate.int_like),
    Parameter("showNames", set(['on', 'off'])),

    # bigBarChart
    Parameter("barChartBars", str),
    Parameter("barChartColors", validate.hex_or_named),
    Parameter("barChartLabel", str),
    Parameter("barChartMetric", str),
    Parameter("barChartUnit", str),
    Parameter("barChartMatrixUrl", validate.full_or_local_url),
    Parameter("barChartSampleUrl", validate.full_or_local_url),
    Parameter("maxLimit", float),

    # bigBed
    Parameter("itemRgb", set(['on']), 'BED9'),
    Parameter("colorByStrand", validate.RGBList, 'BED6'),
    Parameter("denseCoverage", validate.int_like),
    Parameter("labelOnFeature", set(['on', 'off'])),
    Parameter("exonArrows", set(['on', 'off']), 'BED10'),
    Parameter("exonNumbers", set(['on', 'off']), 'BED9'),
    Parameter("scoreFilter", validate.ColSV2_numbers_or_single_number),
    Parameter("maxItems", validate.int_like),
    Parameter('maxWindowToDraw', validate.int_like),
    Parameter("minGrayLevel", set(range(1, 10))),
    Parameter('noScoreFilter', set(['on'])),
    Parameter("spectrum", set(['on']), 'BED5'),
    Parameter("scoreMax", validate.int_like, 'BED5'),
    Parameter("scoreMin", validate.int_like, 'BED5'),
    Parameter("thickDrawItem", set(['on', 'off']), 'BED8'),
    Parameter("searchIndex", str),
    Parameter("searchTrix", validate.full_or_local_url),
    Parameter("labelFields", str),
    Parameter("defaultLabelFields", str),
    Parameter("labelSeparator", str),
    Parameter("bedNameLabel", str),
    Parameter("exonArrowsDense", set(['on', 'off']), 'BED10'),
    Parameter("itemImagePath", str),
    Parameter("itemBigImagePath", str),
    Parameter("linkIdInName", set(['on'])),
    Parameter("nextExonText", str, 'BED10'),
    Parameter("prevExonText", str, 'BED10'),
    Parameter("scoreLabel", str),
    Parameter("showTopScores", validate.int_like, 'BED5'),

    # bigChain
    Parameter("linkDataUrl", validate.full_or_local_url),

    # bigGenePred
    # Shared with bigBed:
    # labelFields
    # defaultLabelFields
    # labelSeparator

    # bigNarrowPeak
    Parameter("scoreFilter", validate.ColSV2_numbers_or_single_number),
    Parameter("pValueFilter", validate.ColSV2_numbers_or_single_number),
    Parameter("qValueFilter", validate.ColSV2_numbers_or_single_number),
    Parameter("signalFilter", validate.ColSV2_numbers_or_single_number),
    Parameter("scoreFilterLimits", validate.ColSV2_numbers_or_single_number),
    Parameter("pValueFilterLimits", validate.ColSV2_numbers_or_single_number),
    Parameter("qValueFilterLimits", validate.ColSV2_numbers_or_single_number),
    Parameter("signalFilterLimits", validate.ColSV2_numbers_or_single_number),
    Parameter("scoreFilterByRange", set(['on', 'off'])),
    Parameter("pValueFilterByRange", set(['on', 'off'])),
    Parameter("qValueFilterByRange", set(['on', 'off'])),
    Parameter("signalFilterByRange", set(['on', 'off'])),

    # bigMaf
    Parameter("speciesOrder", str),
    Parameter("frames", validate.full_or_local_url),
    Parameter("summary", str),

    # bigPsl
    Parameter("baseColorUseCds", str),
    Parameter("baseColorUseSequence", str),
    Parameter("baseColorDefault", set([
        'diffBases',
        'diffCodons',
        'itemBases',
        'itemCodons',
        'genomicCodons'])),
    Parameter("showDiffBasesAllScales", set(['on'])),
    # Shared with bigBed:
    # labelFields
    # defaultLabelFields
    # labelSeparator

    # bigWig
    Parameter("autoScale", set(['on', 'off'])),
    Parameter("maxHeightPixels", validate.ColSV3),
    Parameter("viewLimits", validate.ColSV2),
    Parameter("alwaysZero", set(['on', 'off'])),
    Parameter("graphTypeDefault", set(['points', 'bar'])),
    Parameter("maxWindowToQuery", validate.int_like),
    Parameter("negateValues", set(['on'])),
    Parameter("smoothingWindow", set(['off'] + list(range(1, 17)))),
    Parameter("transformFunc", set(['LOG', 'NONE'])),
    Parameter("windowingFunction", set([
        'mean',
        'mean+whiskers',
        'maximum',
        'minimum'])),
    Parameter("yLineMark", validate.float_like),
    Parameter("yLineOnOff", set(['on', 'off'])),
    Parameter("gridDefault", set(['on'])),

    # halSnake
    Parameter("showSnpWidth", validate.int_like),
    Parameter("otherSpecies", str),

    # vcfTabix
    # Shared with BAM:
    # bigDataIndex
    Parameter("hapClusterEnabled", set(['true', 'false'])),
    Parameter("hapClusterColorBy", set([
        'altOnly',
        'refAlt',
        'base'])),
    Parameter("hapClusterTreeAngle", set([
        'triangle',
        'rectangle'])),
    Parameter("hapClusterHeight", validate.int_like),
    Parameter("applyMinQUal", set(['true', 'false'])),
    Parameter("minQual", validate.int_like),
    Parameter("minFreq", validate.float_like),

    # Supertrack
    Parameter("superTrack", set(['on'])),
    Parameter("parent", str),

    # Composite track
    Parameter('compositeTrack', set(['on'])),
    Parameter('allButtonPair', set(['on'])),
    Parameter('centerLabelsDense', set(['on', 'off'])),
    Parameter('dragAndDrop', set(['subTracks'])),

    # Subgroups can have subGroup1, subGroup2, etc.
    Parameter('subGroups', validate.key_val),
    Parameter('dimensions', validate.key_val),
    Parameter('filterComposite', str),

    # dimensionAchecked, dimensionBchecked, etc.
    Parameter('sortOrder', validate.key_val),


    # View tracks
    Parameter('view', str),
    Parameter('viewUi', set(['on'])),
    Parameter('configurable', set(['on', 'off'])),

    # Aggregate
    Parameter('container', set(['multiWig'])),
    Parameter('aggregate', set([
        'transparentOverlay',
        'stacked',
        'solidOverlay',
        'none'])),
    Parameter('showSubtrackColorOnUi', set(['on'])),

    # Assembly
    Parameter('description', str),
    Parameter('organism', str),
    Parameter('scientificName', str),
    Parameter('orderKey', str),
    Parameter('defaultPos', validate.ucsc_position),
    ]
}

