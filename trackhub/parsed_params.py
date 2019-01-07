from .validate import Param
from . import validate

# HOW TO UPDATE
# parse.py will output blocks of Param() calls that can be directly
# added here (including indentation).
#
# Probably easiest to redirect parse.py's output to a file, then run `diff` (or
# `meld`) between that file and this module.
#
# If something is unclear, run parse.py interactively and inspect the `debug`
# dictionary.
#

# Observed types from the parsed document
TRACKTYPES = [
    'all',
    'bam',
    'bigBarChart',
    'bigBed',
    'bigChain',
    'bigGenePred',
    'bigInteract',
    'bigMaf',
    'bigNarrowPeak',
    'bigPsl',
    'bigWig',
    'compositeTrack',
    'halSnake',
    'multiWig',
    'subGroups',
    'superTrack',
    'vcfTabix',
    'view',

    # assembly tracks are not defined in the document; we need to add
    # separately.
    'assembly',
]

# Tracks for which the definition specifies bigDataUrl
DATA_TRACKTYPES = [
    'bam',
    'bigBarChart',
    'bigBed',
    'bigChain',
    'bigInteract',
    'bigMaf',
    'bigPsl',
    'bigWig',
    'vcfTabix',
]


param_defs = [

    Param(
        name="aggregate",
        fmt=['aggregate <transparentOverlay/stacked/solidOverlay/none>'],
        types=['multiWig'],
        required=False,
        validator=set(['transparentOverlay', 'stacked', 'solidOverlay', 'none'])),

    Param(
        name="aliQualRange",
        fmt=['bamGrayMode <aliQual/baseQual/unpaired>', 'aliQualRange <min:max>', 'baseQualRange <min:max>'],
        types=['bam'],
        required=False,
        validator=validate.ColSV2),

    Param(
        name="allButtonPair",
        fmt=['allButtonPair on'],
        types=['compositeTrack'],
        required=False,
        validator=set(['on'])),

    Param(
        name="altColor",
        fmt=['altColor <red,green,blue>'],
        types=['all'],
        required=False,
        validator=validate.RGB),

    Param(
        name="alwaysZero",
        fmt=['alwaysZero  <off/on>'],
        types=['bigWig'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="autoScale",
        fmt=['autoScale <off/on>'],
        types=['bigWig'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="bamColorMode",
        fmt=['bamColorMode <strand/gray/tag/off>'],
        types=['bam'],
        required=False,
        validator=set(['strand', 'gray', 'tag', 'off'])),

    Param(
        name="bamColorTag",
        fmt=['bamColorTag <XX>'],
        types=['bam'],
        required=False,
        validator=str),

    Param(
        name="bamGrayMode",
        fmt=['bamGrayMode <aliQual/baseQual/unpaired>', 'aliQualRange <min:max>', 'baseQualRange <min:max>'],
        types=['bam'],
        required=False,
        validator=set(['aliQual', 'baseQual', 'unpaired'])),

    Param(
        name="bamSkipPrintQualScore",
        fmt=['bamSkipPrintQualScore .'],
        types=['bam'],
        required=False,
        validator=set(['.'])),

    Param(
        name="barChartBars",
        fmt=['barChartBars <label1 label2...>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartColors",
        fmt=['barChartColors <color1 color2...>'],
        types=['bigBarChart'],
        required=False,
        validator=.validate.hex_or_named),

    Param(
        name="barChartLabel",
        fmt=['barChartLabel <label>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartMatrixUrl",
        fmt=['barChartMatrixUrl <url>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartMetric",
        fmt=['barChartMetric <metric>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartSampleUrl",
        fmt=['barChartSampleUrl <url>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartUnit",
        fmt=['barChartUnit <unit>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="baseColorDefault",
        fmt=['baseColorDefault\n                    <diffBases/diffCodons/itemBases/itemCodons/genomicCodons>'],
        types=['all'],
        required=False,
        validator=set(['diffBases', 'diffCodons', 'itemBases', 'itemCodons', 'genomicCodons'])),

    Param(
        name="baseColorUseCds",
        fmt=['baseColorUseCds <given/table <table>>'],
        types=['bigPsl'],
        required=False,
        validator=str),

    Param(
        name="baseColorUseSequence",
        fmt=['baseColorUseSequence < <extFile {seqTable} <extFile> /\n                        hgPcrResult / lfExtra / nameIsSequence / seq1Seq2 / ss >'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="baseQualRange",
        fmt=['bamGrayMode <aliQual/baseQual/unpaired>', 'aliQualRange <min:max>', 'baseQualRange <min:max>'],
        types=['bam'],
        required=False,
        validator=validate.ColSV2),

    Param(
        name="bedNameLabel",
        fmt=['bedNameLabel <label>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="bigDataIndex",
        fmt=['bigDataIndex <url/relativePath>'],
        types=['bam', 'vcfTabix'],
        required=False,
        validator=str),

    Param(
        name="bigDataUrl",
        fmt=['bigDataUrl <url/relativePath>'],
        types=['bam', 'bigBarChart', 'bigBed', 'bigChain', 'bigInteract', 'bigMaf', 'bigPsl', 'bigWig', 'vcfTabix'],
        required=True,
        validator=str),

    Param(
        name="bigDataUrl2",
        fmt=['bigDataUrl <url/relativePath>'],
        types=['bam', 'bigBed', 'bigWig', 'vcfTabix'],
        required=False,
        validator=str),

    Param(
        name="boxedCfg",
        fmt=['boxedCfg <on/off>'],
        types=['all'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="centerLabelsDense",
        fmt=['centerLabelsDense <off/on>'],
        types=['compositeTrack'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="chromosomes",
        fmt=['chromosomes <chr1,chr2,...>'],
        types=['all'],
        required=False,
        validator=validate.CSV),

    Param(
        name="color",
        fmt=['color <red,green,blue>'],
        types=['all'],
        required=False,
        validator=validate.RGB),

    Param(
        name="colorByStrand",
        fmt=['colorByStrand <red,green,blue> <red,green,blue>'],
        types=['bigBed'],
        required=False,
        validator=validate.RGBList,
        min_bed_fields=6),

    Param(
        name="compositeTrack",
        fmt=['compositeTrack on'],
        types=['compositeTrack'],
        required=False,
        validator=set(['on'])),

    Param(
        name="configurable",
        fmt=['configurable <off/on>'],
        types=['view'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="container",
        fmt=['container multiWig'],
        types=['multiWig'],
        required=False,
        validator=set(['multiWig'])),

    Param(
        name="darkerLabels",
        fmt=['darkerLabels on'],
        types=['all'],
        required=False,
        validator=set(['on'])),

    Param(
        name="dataVersion",
        fmt=['dataVersion <str>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="defaultLabelFields",
        fmt=['defaultLabelFields <fieldName[,fieldName]>'],
        types=['bigBarChart', 'bigBed', 'bigGenePred', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=str),

    Param(
        name="denseCoverage",
        fmt=['denseCoverage <maxVal>'],
        types=['bigBed'],
        required=False,
        validator=float),

    Param(
        name="dimensionAchecked",
        fmt=['dimension<?>checked <mTag1a> [mTag1b …]'],
        types=['subGroups'],
        required=False,
        validator=str),

    Param(
        name="dimensions",
        fmt=['dimensions <dimX=gTag#> [dimY=gTag#] [dimA=gTag# ...]'],
        types=['subGroups'],
        required=False,
        validator=validate.key_val),

    Param(
        name="directUrl",
        fmt=['directUrl <url>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="directUrl_for_hubs",
        fmt=['directUrl <url>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="doWiggle",
        fmt=['doWiggle on'],
        types=['bam'],
        required=False,
        validator=set(['on'])),

    Param(
        name="dragAndDrop",
        fmt=['dragAndDrop subTracks'],
        types=['compositeTrack'],
        required=False,
        validator=set(['subTracks'])),

    Param(
        name="filterComposite",
        fmt=['filterComposite <dim[A/B/C][=one]> [dimB dimC ...]'],
        types=['subGroups'],
        required=False,
        validator=str),

    Param(
        name="frames",
        fmt=['frames <table/url>'],
        types=['bigMaf'],
        required=False,
        validator=str),

    Param(
        name="graphTypeDefault",
        fmt=['graphTypeDefault points'],
        types=['bigWig'],
        required=False,
        validator=set(['points', 'bar'])),

    Param(
        name="gridDefault",
        fmt=['yLineMark <#>', 'yLineOnOff <off/on>', 'gridDefault   on'],
        types=['bigWig'],
        required=False,
        validator=set(['on'])),

    Param(
        name="html",
        fmt=['html'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="idInUrlSql",
        fmt=['url <url>', 'urlLabel <label>', 'idInUrlSql <sql for id>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="iframeOptions",
        fmt=['iframeOptions <string>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="iframeUrl",
        fmt=['iframeUrl <url>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="indelDoubleInsert",
        fmt=['indelDoubleInsert <off/on>', 'indelQueryInsert <off/on>', 'indelPolyA <off/on>'],
        types=['bam'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="indelPolyA",
        fmt=['indelDoubleInsert <off/on>', 'indelQueryInsert <off/on>', 'indelPolyA <off/on>'],
        types=['bam'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="indelQueryInsert",
        fmt=['indelDoubleInsert <off/on>', 'indelQueryInsert <off/on>', 'indelPolyA <off/on>'],
        types=['bam'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="interactDirectional",
        fmt=['interactDirectional <true|offsetSource|offsetTarget|clusterSource|clusterTarget>'],
        types=['bigInteract'],
        required=False,
        validator=set(['true', 'offsetSource', 'offsetTarget', 'clusterSource',
                      'clusterTarget'])),

    Param(
        name="interactUp",
        fmt=['interactUp <true|false>'],
        types=['bigInteract'],
        required=False,
        validator=set(['true', 'false'])),

    Param(
        name="itemRgb",
        fmt=['itemRgb on'],
        types=['bigBed'],
        required=False,
        validator=set(['on']),
        min_bed_fields=9,
    ),

    Param(
        name="labelFields",
        fmt=['labelFields <fieldName[,fieldName]>'],
        types=['bigBarChart', 'bigBed', 'bigGenePred', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=validate.CSV),

    Param(
        name="labelOnFeature",
        fmt=['labelOnFeature <on/off>'],
        types=['bigBed'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="labelSeparator",
        fmt=['labelSeparator <text>'],
        types=['bigBed', 'bigGenePred', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=str),

    Param(
        name="linkDataUrl",
        fmt=['linkDataUrl <url/relativePath>'],
        types=['bigChain'],
        required=['bigChain'],
        validator=str),

    Param(
        name="linkIdInName",
        fmt=['linkIdInName on'],
        types=['bigBed'],
        required=False,
        validator=set(['on'])),

    Param(
        name="longLabel",
        fmt=['longLabel'],
        types=['all'],
        required=True,
        validator=validate.long_label),

    Param(
        name="maxHeightPixels",
        fmt=['maxHeightPixels <max:default:min>'],
        types=['bigInteract', 'bigWig'],
        required=False,
        validator=validate.ColSV3),

    # TODO: Improve verification to check that values is less than 100,000
    Param(
        name="maxItems",
        fmt=['maxItems <integer>'],
        types=['bigBed'],
        required=False,
        validator=int),

    Param(
        name="maxLimit",
        fmt=['maxLimit<#>'],
        types=['bigBarChart'],
        required=False,
        validator=int),

    Param(
        name="maxWindowToDraw",
        fmt=['maxWindowToDraw <integer>'],
        types=['bam', 'bigWig'],
        required=False,
        validator=int),

    Param(
        name="maxWindowToQuery",
        fmt=['maxWindowToQuery <integer>'],
        types=['bigWig'],
        required=False,
        validator=int),

    Param(
        name="meta",
        fmt=['meta'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="minAliQual",
        fmt=['minAliQual <#>'],
        types=['bam'],
        required=False,
        validator=int),

    Param(
        name="minGrayLevel",
        fmt=['minGrayLevel  <1-9>'],
        types=['bigBed'],
        required=False,
        validator=set(range(1, 10))),

    Param(
        name="mouseOverField",
        fmt=['mouseOverField <fieldName1>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="negateValues",
        fmt=['negateValues <on>'],
        types=['bigWig'],
        required=False,
        validator=set(['on'])),

    Param(
        name="nextExonText",
        fmt=['nextExonText <str>', 'prevExonText <str>'],
        types=['all'],
        required=False,
        validator=str,
        min_bed_fields=10),

    Param(
        name="noColorTag",
        fmt=['noColorTag .'],
        types=['bam'],
        required=False,
        validator=set(['.'])),

    Param(
        name="otherDb",
        fmt=['otherDb <otherDb>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="otherSpecies",
        fmt=['otherSpecies <otherSpecies>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="pairEndsByName",
        fmt=['pairEndsByName .'],
        types=['bam'],
        required=False,
        validator=set(['.'])),

    Param(
        name="pairSearchRange",
        fmt=['pairSearchRange <#>'],
        types=['bam'],
        required=False,
        validator=int),

    # NOTE in the spec there is "parent_container" as well as "parent" so as to
    # have unique div names in the HTML. They apply to different track types
    # (multiWig, superTrack, compositeTrack). In addition, subtracks of various
    # types can use the parent param to control visibility, though there is no
    # div that sets "parent" to "all" track types.
    #
    # To cover all these cases, we set types to "all" and just validate on str.

    Param(
        name="parent",
        fmt=['parent <composite> [off/on]', 'parent <containerTrack>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="pennantIcon",
        fmt=['pennantIcon <iconFile>/<text color> [html [tip]]'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="prevExonText",
        fmt=['nextExonText <str>', 'prevExonText <str>'],
        types=['all'],
        required=False,
        validator=str,
        min_bed_fields=10),

    Param(
        name="priority",
        fmt=['priority <float>'],
        types=['all'],
        required=False,
        validator=float),

    Param(
        name="refUrl",
        fmt=['refUrl <url>'],
        types=['bam'],
        required=False,
        validator=str),

    # TODO: worth a custom validator?
    Param(
        name="scoreFilter",
        fmt=['scoreFilter <low>[:<high>]', 'scoreFilterLimits <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    # TODO: worth a custom validator?
    Param(
        name="scoreFilterLimits",
        fmt=['scoreFilter <low>[:<high>]', 'scoreFilterLimits <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="scoreLabel",
        fmt=['scoreLabel <label>'],
        types=['bigBed', 'bigGenePred', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=str),

    Param(
        name="scoreMax",
        fmt=['spectrum on', 'scoreMax <integer>', 'scoreMin <integer>'],
        types=['all'],
        required=False,
        validator=int,
        min_bed_fields=5),

    Param(
        name="scoreMin",
        fmt=['spectrum on', 'scoreMax <integer>', 'scoreMin <integer>'],
        types=['all'],
        required=False,
        validator=int,
        min_bed_fields=5),

    Param(
        name="searchIndex",
        fmt=['searchIndex <str>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="searchTrix",
        fmt=['searchTrix <url/relativePath>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="sepFields",
        fmt=['sepFields <fieldName1>="<url1>" <fieldName2>="<url2>" ...'],
        types=['bigBed', 'bigChain', 'bigGenePred', 'bigMaf', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=validate.key_val),

    Param(
        name="shortLabel",
        fmt=['shortLabel'],
        types=['all'],
        required=True,
        validator=validate.short_label),

    Param(
        name="showDiffBasesAllScales",
        fmt=['showDiffBasesAllScales on'],
        types=['all'],
        required=False,
        validator=set(['on'])),

    Param(
        name="showNames",
        fmt=['showNames <on/off>'],
        types=['bam'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name="showSnpWidth",
        fmt=['showSnpWidth <integer>'],
        types=['halSnake'],
        required=False,
        validator=int),

    Param(
        name="showSubtrackColorOnUi",
        fmt=['showSubtrackColorOnUi on'],
        types=['multiWig'],
        required=False,
        validator=set(['on'])),

    Param(
        name="skipEmptyFields",
        fmt=['skipEmptyFields on'],
        types=['bigBed', 'bigChain', 'bigGenePred', 'bigMaf', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=set(['on'])),

    Param(
        name="skipFields",
        fmt=['skipFields <fieldName1>="<url1>" <fieldName2>="<url2>" ...'],
        types=['bigBed', 'bigChain', 'bigGenePred', 'bigMaf', 'bigNarrowPeak', 'bigPsl'],
        required=False,
        validator=validate.key_val),

    Param(
        name="smoothingWindow",
        fmt=['smoothingWindow <off/1-16>'],
        types=['bigWig'],
        required=False,
        validator=str),

    Param(
        name="sortOrder",
        fmt=['sortOrder <gTag#=+/-> [gTag#=- …]'],
        types=['subGroups'],
        required=False,
        validator=validate.key_val),

    Param(
        name="spectrum",
        fmt=['spectrum on', 'scoreMax <integer>', 'scoreMin <integer>'],
        types=['all'],
        required=False,
        validator=set(['on']),
        min_bed_fields=5),

    Param(
        name="subGroups",
        fmt=['subGroups <gTag1=mTag1?> [gTag2= mTag2?]'],
        types=['subGroups'],
        required=False,
        validator=validate.key_val),

    Param(
        name="summary",
        fmt=['summary <tableName/url>'],
        types=['bigMaf'],
        required=False,
        validator=str),

    Param(
        name="superTrack",
        fmt=['superTrack on'],
        types=['superTrack'],
        required=False,
        validator=set(['on'])),

    Param(
        name="thickDrawItem",
        fmt=['thickDrawItem <off/on>'],
        types=['bigBed'],
        required=False,
        validator=set(['on', 'off']),
        min_bed_fields=8),

    Param(
        name="track",
        fmt=['track'],
        types=['all'],
        required=True,
        validator=str),

    Param(
        name="transformFunc",
        fmt=['transformFunc <NONE/LOG>'],
        types=['bigWig'],
        required=False,
        validator=set(['NONE', 'LOG'])),

    Param(
        name="url",
        fmt=['url <url>', 'urlLabel <label>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="url_for_hubs",
        fmt=['url <url>', 'urlLabel <label>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="urlLabel",
        fmt=['url <url>', 'urlLabel <label>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="urls",
        fmt=['urls <fieldName1>="<url1>" <fieldName2>="<url2>" ...'],
        types=['bigBarChart', 'bigBed'],
        required=False,
        validator=validate.key_val),

    Param(
        name='view',
        fmt='view <viewName>',
        types=['view'],
        required=False,
        validator=str),

    Param(
        name="viewLimits",
        fmt=['viewLimits <lower:upper>', 'viewLimitsMax <lower:upper>'],
        types=['bigWig'],
        required=False,
        validator=validate.ColSV2),

    Param(
        name="viewLimitsMax",
        fmt=['viewLimits <lower:upper>', 'viewLimitsMax <lower:upper>'],
        types=['bigWig'],
        required=False,
        validator=validate.ColSV2),

    Param(
        name="viewUi",
        fmt=['viewUi on'],
        types=['view'],
        required=False,
        validator=set(['on'])),

    Param(
        name="visibility",
        fmt=['visibility'],
        types=['all'],
        required=False,
        validator=set(['hide', 'dense', 'squish', 'pack', 'full'])),

    Param(
        name="windowingFunction",
        fmt=['windowingFunction  <mean/mean+whiskers/maximum/minimum>'],
        types=['bigWig'],
        required=False,
        validator=set(['mean', 'mean+whiskers', 'maximum', 'minimum'])),

    Param(
        name="yLineMark",
        fmt=['yLineMark <#>', 'yLineOnOff <off/on>', 'gridDefault   on'],
        types=['bigWig'],
        required=False,
        validator=float),

    Param(
        name="yLineOnOff",
        fmt=['yLineMark <#>', 'yLineOnOff <off/on>', 'gridDefault   on'],
        types=['bigWig'],
        required=False,
        validator=set(['on', 'off'])),

    Param(
        name='description',
        fmt='',
        types=['assembly'],
        required=False,
        validator=str),

    Param(
        name='organism',
        fmt='',
        types=['assembly'],
        required=False,
        validator=str),

    Param(
        name='scientificName',
        fmt='',
        types=['assembly'],
        required=False,
        validator=str),

    Param(
        'orderKey',
        fmt='',
        types=['assembly'],
        required=False,
        validator=str),

    Param(
        'defaultPos',
        fmt='',
        types=['assembly'],
        required=False,
        validator=validate.ucsc_position),


    # Add a param for types
    Param(
        name='type',
        fmt='',
        types=TRACKTYPES,
        required=True,
        validator=set(TRACKTYPES)),

    ]


# TODO: Some params are not specified for bigBed, only BED.
# - exonArrows
# - exonNumbers
#
