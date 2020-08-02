#!/bin/bash

(
    mkdir -p autoSql
    cd autoSql
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/barChart/barChartBed.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigGenePred.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigLink.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigMaf.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigNarrowPeak.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigPsl.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/interact/interact.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/mafFrames.as
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/mafSummary.as
)

(
    mkdir -p original_ucsc_examples
    cd original_ucsc_examples
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/barChart/exampleSampleData.txt
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/barChart/hg38.gtexTranscripts.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigChain.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigChain.link.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigGenePred.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigMaf.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigNarrowPeak.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/bigPsl.bb
    wget --no-clobber https://genome.ucsc.edu/goldenPath/help/examples/vcfExample.vcf.gz
)


(
    mkdir -p bin
    cd bin
    wget --no-clobber http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigBedToBed
    wget --no-clobber http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/fetchChromSizes
)

(
    mkdir -p ucsc_example_beds
    cd ucsc_example_beds

    for bb in ../original_ucsc_examples/*.bb; do
        bigBedToBed $bb $(basename $bb).bed
    done
)
