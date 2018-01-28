from __future__ import absolute_import

from collections import OrderedDict
from .params import _params

super_track_fields = OrderedDict((i, _params[i]) for i in [
    'superTrack',
    'parent'])

composite_track_fields = OrderedDict((i, _params[i]) for i in [
    'parent',
    'compositeTrack',
    'allButtonPair',
    'centerLabelsDense',
    'dragAndDrop',
    'subGroups',
    'dimensions',
    'filterComposite',
    'sortOrder',
])

view_track_fields = OrderedDict((i, _params[i]) for i in [
    'view',
    'subGroups',
    'viewUi',
    'configurable',
])

aggregate_track_fields = OrderedDict((i, _params[i]) for i in [
    'container',
    'parent',
    'aggregate',
    'showSubtrackColorOnUi',
])


assembly_fields = OrderedDict((i, _params[i]) for i in [
    'description',
    'organism',
    'scientificName',
    'orderKey',
    'defaultPos',
])

# Params shared by all tracks
track_fields = OrderedDict((i, _params[i]) for i in [
        'track',
        'type',
        'shortLabel',
        'longLabel',
        'visibility',
        'html',
        'boxedCfg',
        'color',
        'altColor',
        'chromosomes',
        'darkerLabels',
        'dataVersion',
        'directUrl',
        'iframeUrl',
        'iframeOptions',
        'otherSpecies',
        'otherDb',
        'pennantIcon',
        'priority',
        'url',
        'spectrum',
        'baseColorUseSequence',
        'baseColorDefault',
        'showDiffBasesAllScales',
        'nextExonText',
    ]
)

# Params specific to each track type. These are in addition to the params used
# by all tracks defined above.
track_typespecific_fields = {
    None: {},
    'bam': OrderedDict((i, _params[i]) for i in [
        'bigDataIndex',
        'maxWindowToDraw',
        'refUrl',
        'bamColorMode',
        'bamGrayMode',
        'bamColorTag',
        'noColorTag',
        'bamSkipPrintQualScore',
        'indelDoubleInsert',
        'minAliQual',
        'pairEndsByName',
        'pairSearchRange',
        'showNames',
    ]),
    'bigBarChart': OrderedDict((i, _params[i]) for i in [
        'bigDataUrl',
        'maxLimit',
        'labelFields',
        'defaultLabelFields',
        'barChartUnit',
        'barChartLabel',
        'barChartMetric',
        'barChartBars',
        'barChartColors',
        'barChartMatrixUrl',
        'barChartSampleUrl',
    ]),
    'bigBed': OrderedDict((i, _params[i]) for i in [
        'urls',
        'skipEmptyFields',
        'skipFields',
        'sepFields',
        'mouseOverField',
        'colorByStrand',
        'denseCoverage',
        'labelOnFeature',
        'scoreFilter',
        'itemRgb',
        'maxItems',
        'minGrayLevel',
        'searchIndex',
        'searchTrix',
        'thickDrawItem',
        'bedNameLabel',
        'scoreLabel',
        'linkIdInName',
        'labelFields',
        'defaultLabelFields',
        'labelSeparator',
    ]),
    'bigChain': OrderedDict((i, _params[i]) for i in [
        'linkDataUrl',
        'skipEmptyFields',
        'skipFields',
        'sepFields',
    ]),
    'bigGenePred': OrderedDict((i, _params[i]) for i in [
        'skipEmptyFields',
        'skipFields',
        'sepFields',
        'scoreLabel',
        'labelFields',
        'defaultLabelFields',
        'labelSeparator'
    ]),
    'bigMaf': OrderedDict((i, _params[i]) for i in [
        'skipEmptyFields',
        'skipFields',
        'sepFields',
        'frames',
        'summary'
    ]),
    'bigNarrowPeak': OrderedDict((i, _params[i]) for i in [
        'skipEmptyFields',
        'skipFields',
        'sepFields',
        'scoreLabel',
        'labelFields',
        'defaultLabelFields',
        'labelSeparator',
        'scoreFilter',
        'pValueFilter',
        'qValueFilter',
        'signalFilter',
        'scoreFilterLimits',
        'pValueFilterLimits',
        'qValueFilterLimits',
        'signalFilterLimits',
        'scoreFilterByRange',
        'pValueFilterByRange',
        'qValueFilterByRange',
        'signalFilterByRange',
    ]),
    'bigPsl': OrderedDict((i, _params[i]) for i in [
        'skipEmptyFields',
        'skipFields',
        'sepFields',
        'scoreLabel',
        'baseColorUseCds',
        'labelFields',
        'defaultLabelFields',
        'labelSeparator',
    ]),
    'bigWig': OrderedDict((i, _params[i]) for i in [
        'maxWindowToDraw',
        'alwaysZero',
        'autoScale',
        'graphTypeDefault',
        'maxHeightPixels',
        'maxWindowToQuery',
        'negateValues',
        'smoothingWindow',
        'transformFunc',
        'viewLimits',
        'windowingFunction',
        'yLineMark',
    ]),
    'halSnake': OrderedDict((i, _params[i]) for i in [
        'showSnpWidth'
    ]),
    'vcfTabix': OrderedDict((i, _params[i]) for i in [
        'bigDataIndex',
        "hapClusterEnabled",
        "hapClusterColorBy",
        "hapClusterTreeAngle",
        "hapClusterHeight",
        "applyMinQUal",
        "minQual",
        "minFreq",
    ]),
}

track_field_order = OrderedDict((i, _params[i]) for i in [
    'track',
    'bigDataUrl',
    'shortLabel',
    'longLabel',
    'type'
])
