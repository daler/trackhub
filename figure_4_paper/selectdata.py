import encode_dataframe as edf
import pandas as pd
import trackhub

#only run once. takes 20 mins
#edf.mirror_metadata_files('hg19')

df = edf.encode_dataframe('hg19')
interesting = df.antibody == 'CTCF'
interesting &= df.dataType == 'ChipSeq'

interesting &= df.cell.isin(['MCF-7','LNCaP'])

interesting &= df.type.isin(['bam','bed','bigWig','narrowPeak'])
interesting &= df.objStatus.isnull()
interesting &= df.dataType == 'ChipSeq'
interesting &= df.lab == 'UT-A'
#interesting &= df.treatment == 'None'
#interesting &= df.cell.isin(['MCF-7','LNCaP'])
interesting &= df.treatment.isin(['None','estrogen','androgen','serum_stimulated_media','serum_starved_media'])
m = df[interesting]

urls = m.url.values
f = pd.DataFrame(urls)
f.to_csv('urls2download.txt',header=False,index=False)

hub, genomes_file, genome, trackdb = trackhub.default_hub(
    hub_name="ENCODE_CTCF_ChipSeq",
    short_label='ctcf',
    long_label='ENCODE ChipSeq data',
    genome="hg19",
    email="eva.jason@nih.gov")

subgroups = [
   trackhub.SubGroupDefinition(
        name='treatment',
        label='treatment',
        mapping={
            'None':'None',
            'estrogen':'estrogen',
            'androgen':'androgen',
            'serum_stimulated_media':'serum_stimulated_media',
            'serum_starved_media':'serum_starved_media'
        }),
]

for i in list(m.cell.unique()):
    df_cell = m[m["cell"]==i]
    supertrack = trackhub.SuperTrack(
        name = i+'_SuperTrack',
    )
    trackdb.add_tracks(supertrack)

    composite = trackhub.CompositeTrack(
        name = i+'_composite',
        short_label = 'bam, peaks, and signal',
        tracktype = 'bigWig',
        dimensions = 'dimX=treatment',
        visibility = 'full',
    )
    supertrack.add_tracks(composite)

    signal_view = trackhub.ViewTrack(
        name = i+'_signal_view_track',
        view='signal',
        visibility='full',
        tracktype='bigWig',
        short_label='signal')

    composite.add_view(signal_view)

    #bws = m[m["type"] == "bigWig"]
    for fn in df_cell[df_cell["type"] == "bigWig"].filename:
        track = trackhub.Track(
            name = fn.split(".")[0],
            tracktype ="bigWig",
            subgroups = {#'cell' : row.cell,
                'treatment' : df_cell.loc[fn].treatment,
                }
            ,
            color = "182,108,30",
            visibility="full",
            bigDataUrl = df_cell.loc[fn].url
        )
        signal_view.add_tracks(track)
       # print(fn)
    #npks = m[m["type"] == "narrowPeak"]

    regions_view = trackhub.ViewTrack(
        name = i+'_region_view_track',
        view='region',
        tracktype='bigNarrowPeak',
        short_label='region')
    composite.add_view(regions_view)

    #npks = vm[m["type"] == "narrowPeak"]^
    for fn in df_cell[df_cell["type"] == "narrowPeak"].filename:
        track = trackhub.Track(
            name = fn.split(".")[0],
            tracktype ="bigNarrowPeak",
            subgroups = {#'cell' : row.cell,
                'treatment' : df_cell.loc[fn].treatment},
            color = "30,104,182",
            visibility="dense",
            bigDataUrl = df_cell.loc[fn].url
            )
        regions_view.add_tracks(track)

    alignment_view = trackhub.ViewTrack(
        name = i+'_alignment_view_track',
        view='alignment',
        tracktype='bam',
        short_label='alignment')
    composite.add_view(alignment_view)
    #bams = m[m["type"] == "bam"]
    for fn in df_cell[df_cell["type"] == "bam"].filename:
        track = trackhub.Track(
            name = fn.split(".")[0],
            tracktype ="bam",
            subgroups = {
                'treatment' : df_cell.loc[fn].treatment,
                },
            bigDataUrl = df_cell.loc[fn].url
            )
        alignment_view.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='helix.nih.gov', remote_dir='/data/NICHD-core0/datashare/example_hubs/figure4paper/')

