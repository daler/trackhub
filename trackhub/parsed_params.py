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
    'bigLolly',
    'bigMaf',
    'bigNarrowPeak',
    'bigPsl',
    'bigWig',
    'compositeTrack',
    'halSnake',
    'hic',
    'multiWig',
    'subGroups',
    'superTrack',
    'vcfPhasedTrio',
    'vcfTabix',
    'view',

    # assembly tracks are not defined in the document; we need to add
    # separately.
    'assembly',

    # neither are genome objects, but we want to support arguments like
    # defaultPos so it needs to be added here.
    'genome',
]

# Tracks for which the definition specifies bigDataUrl
DATA_TRACKTYPES = [
    'bam',
    'bigBarChart',
    'bigBed',
    'bigChain',
    'bigInteract',
    'bigLolly',
    'bigMaf',
    'bigPsl',
    'bigWig',
    'hic',
    'vcfPhasedTrio',
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
        fmt=['autoScale <off/on/group>'],
        types=['bigWig', 'hic', 'compositeTrack'],
        required=False,
        validator=set(['on', 'off', 'group'])),

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
        name="barChartCategoryUrl",
        fmt=['barChartCategoryUrl <url>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

    Param(
        name="barChartColors",
        fmt=['barChartColors <color1 color2...>'],
        types=['bigBarChart'],
        required=False,
        validator=str),

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
        name="barChartMaxSize",
        fmt=['barChartMaxSize <small/medium/large>'],
        types=['bigBarChart'],
        required=False,
        validator=['small', 'medium', 'large']),

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
        name="barChartSizeWindows",
        fmt=['barChartSizeWindows <largeMax> <smallMin>'],
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
        types=['bam', 'vcfPhasedTrio', 'vcfTabix'],
        required=False,
        validator=str),

    Param(
        name="bigDataUrl",
        fmt=['bigDataUrl <url/relativePath>'],
        types=['bam', 'bigBarChart', 'bigBed', 'bigChain', 'bigInteract',
               'bigLolly', 'bigMaf', 'bigPsl', 'bigWig', 'hic',
               'vcfPhasedTrio', 'vcfTabix'],
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
        fmt=['dimension<?>checked <mTag1a> [mTag1b ...]'],
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
        validator=str),

    Param(
        name="drawMode",
        fmt=['drawMode <triangle|square|arc>'],
        types=['hic'],
        required=False,
        validator=str),

    Param(
        name="exonNumbers",
        fmt=['exonNumbers <on/off>'],
        types=['bigBed', 'bigGenePred'],
        required=False,
        validator=str),

    Param(
        name="filter",
        fmt=['filter.<fieldName> <default integer>', 'filterByRange.<fieldName> <off/on>', 'filterLimits.<fieldName> <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filter.<fieldName>",
        fmt=['filter.<fieldName> <default integer>', 'filterByRange.<fieldName> <off/on>', 'filterLimits.<fieldName> <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterByRange.<fieldName>",
        fmt=['filter.<fieldName> <default integer>', 'filterByRange.<fieldName> <off/on>', 'filterLimits.<fieldName> <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterComposite",
        fmt=['filterComposite <dim[A/B/C][=one]> [dimB dimC ...]'],
        types=['subGroups'],
        required=False,
        validator=str),

    Param(
        name="filterLabel",
        fmt=['filterLabel.<fieldName> <label>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterLimits.<fieldName>",
        fmt=['filter.<fieldName> <default integer>', 'filterByRange.<fieldName> <off/on>', 'filterLimits.<fieldName> <low>[:<high>]'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterText",
        fmt=['filterText.<fieldName> <default search string>', 'filterType.<fieldName> <wildcard/regexp>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterText.<fieldName>",
        fmt=['filterText.<fieldName> <default search string>', 'filterType.<fieldName> <wildcard/regexp>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterType.<fieldName>",
        fmt=['filterValues.<fieldName> <value1,value2,value3...>',
             'filterValuesDefault.<fieldName> <value1,value2,value3...>',
             'filterType.<fieldName> <singleList/multipleListOr/multipleListAnd/multipleListOnlyOr/multipleListOnlyAnd>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterValues",
        fmt=['filterValues.<fieldName> <value1,value2,value3...>',
             'filterValuesDefault.<fieldName> <value1,value2,value3...>',
             'filterType.<fieldName> <singleList/multipleListOr/multipleListAnd/multipleListOnlyOr/multipleListOnlyAnd>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterValues.<fieldName>",
        fmt=['filterValues.<fieldName> <value1,value2,value3...>',
             'filterValuesDefault.<fieldName> <value1,value2,value3...>',
             'filterType.<fieldName> <singleList/multipleListOr/multipleListAnd/multipleListOnlyOr/multipleListOnlyAnd>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="filterValuesDefault.<fieldName>",
        fmt=['filterValues.<fieldName> <value1,value2,value3...>',
             'filterValuesDefault.<fieldName> <value1,value2,value3...>',
             'filterType.<fieldName> <singleList/multipleListOr/multipleListAnd/multipleListOnlyOr/multipleListOnlyAnd>'],
        types=['bigBed'],
        required=False,
        validator=str),

    Param(
        name="frames",
        fmt=['frames <table/url>'],
        types=['bigMaf'],
        required=False,
        validator=str),

    Param(
        name="geneTrack",
        fmt=['geneTrack <track>'],
        types=['vcfPhasedTrio'],
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
        validator=str),

    Param(
        name="hideEmptySubtracks",
        fmt=['hideEmptySubtracks <on/off>'],
        types=['compositeTrack'],
        required=False,
        validator=str),

    Param(
        name="hideEmptySubtracksLabel",
        fmt=['hideEmptySubtracksLabel <label>'],
        types=['compositeTrack'],
        required=False,
        validator=str),

    Param(
        name="hideEmptySubtracksMultiBedUrl",
        fmt=['hideEmptySubtracksMultiBedUrl file.bb'],
        types=['compositeTrack'],
        required=False,
        validator=str),

    Param(
        name="hideEmptySubtracksSourcesUrl",
        fmt=['hideEmptySubtracksSourcesUrl file.tab'],
        types=['compositeTrack'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="interactMultiRegion",
        fmt=['interactMultiRegion <true|padding>'],
        types=['bigInteract'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="lollyField",
        fmt=['lollyField <integer>'],
        types=['bigLolly'],
        required=False,
        validator=str),

    Param(
        name="lollyMaxSize",
        fmt=['lollyMaxSize <integer>'],
        types=['bigLolly'],
        required=False,
        validator=str),

    Param(
        name="lollySizeField",
        fmt=['lollySizeField <integer>'],
        types=['bigLolly'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="mergeSpannedItems",
        fmt=['mergeSpannedItems <on/off>'],
        types=['bigBed'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="mouseOver",
        fmt=['mouseOver <pattern>'],
        types=['bigBed'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="noStems",
        fmt=['noStems <on/off>'],
        types=['bigLolly'],
        required=False,
        validator=str),

    Param(
        name="normalization",
        fmt=['normalization <NONE|VC|VC_SQRT|KR>'],
        types=['hic'],
        required=False,
        validator=str),

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

    # NOTE in the spec there is "parent_container", "parent_supertrack", and
    # "parent". The reason appears to be so that there are unique div
    # names in the HTML, but they all refer to the parameter "parent".
    # In addition, subtracks of various types can use the parent param to
    # control visibility, though there is no div that sets "parent" to "all"
    # track types.
    #
    # To cover all these cases, we:
    #   - remove the Params for "parent_container" and "parent_supertrack"
    #   - include the Param for "parent"
    #   - set types to "all" and just validate on str

    Param(
        name="parent",
        fmt=['parent <composite> [off/on]', 'parent <containerTrack>'],
        types=['all'],
        required=False,
        validator=str),

    Param(
        name="pennantIcon",
        fmt=['pennantIcon <iconFile>/<text color> [html [tip]] \n[; <iconFile>/<text color> [html [tip]]]'],
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

    Param(
        name="resolution",
        fmt=['resolution <Auto|integer>'],
        types=['hic'],
        required=False,
        validator=str),

    Param(
        name="saturationScore",
        fmt=['saturationScore <float>'],
        types=['hic'],
        required=False,
        validator=str),

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
        fmt=['sortOrder <gTag#=+/-> [gTag#=- ...]'],
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
        validator=str),

    Param(
        name="tableBrowser",
        fmt=['tableBrowser <off/on/noGenome> [table1 ...]'],
        types=['all'],
        required=False,
        validator=str),

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
        validator=str),

    Param(
        name="vcfChildSample",
        fmt=['vcfChildSample <sampleName|altName>'],
        types=['vcfPhasedTrio'],
        required=False,
        validator=str),

    Param(
        name="vcfParentSamples",
        fmt=['vcfParentSamples <sampleName|altName,sampleName|altName>'],
        types=['vcfPhasedTrio'],
        required=False,
        validator=str),

    Param(
        name="vcfUseAltSampleNames",
        fmt=['vcfUseAltSampleNames <on/off>'],
        types=['vcfPhasedTrio'],
        required=False,
        validator=str),

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
        name="yAxisLabel",
        fmt=['yAxisLabel.<integer> <integer> <on/off> <R,G,B> <string> '],
        types=['bigLolly'],
        required=False,
        validator=str),

    Param(
        name="yAxisNumLabels",
        fmt=['yAxisNumLabels.<on/off> <integer>'],
        types=['bigLolly'],
        required=False,
        validator=str),

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

    # NOTE: Assembly parameters are not defined in the database, so they need
    # to be added separately here.
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
        types=['all','assembly', 'genome'],
        required=False,
        validator=validate.ucsc_position),


    # Add a param for types
    Param(
        name='type',
        fmt='',
        types=TRACKTYPES,
        required=True,
        validator=validate.tracktypes),

    # Add a param for group, which is used in assembly hubs (but not documented
    # in the Track Hub Database Definition document)
    Param(
        name='group',
        fmt='',
        types=TRACKTYPES,
        required=False,
        validator=str),

    ]


# TODO: Some params are not specified for bigBed, only BED.
# - exonArrows
# - exonNumbers
#

# NOTE: there are other allowed parameters for things like Assembly or Genome
# objects that require more complexity to find/create/validate. For example,
# trackDb filenames are figured out on the fly. Those params with extra
# complexity are not included here.
