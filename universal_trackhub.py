import pandas as pd
import trackhub
#import argparse
from openpyxl import load_workbook
import xlrd
import sys


#excel_file = argparse.ArgumentParser(description='Process some integers.')
#excel_file.add_argument('excel-file', metavar='e', type=str,nargs='?',help='path to excel file for track hub')
#args = parser.parse_args()

#file = sys.argv[1]

file ='universal_trackhub.xlsx'

#destination = sys.argv[2]

#get the sheet names
# there must be sheets named "genome" and "hub"
# TODO: check that there are sheets names "genome" and "hub"
sheets = xlrd.open_workbook(file, on_demand=True).sheet_names()


def sheet_to_dict(file, sheet):
    """ read a  two columns sheet and make it into a dictionary with the first column as keys and the second as the values"""
    sheet = pd.read_excel(file, sheet_name=sheet, header=None)
    sheet_dict = dict(sheet.values.tolist())
    return sheet_dict

# there must be sheets named "genome" and "hub"
# Make the hub
hub_dict = sheet_to_dict(file, sheet="hub")
hub = trackhub.Hub(**hub_dict)

# Make the genome
genome_dict = sheet_to_dict(file, sheet="genome")
genome = trackhub.Assembly(**genome_dict)

genomes_file = trackhub.GenomesFile()
hub.add_genomes_file(genomes_file)
trackdb = trackhub.TrackDb()
genome.add_trackdb(trackdb)
genomes_file.add_genome(genome)

sheets.remove("hub")
sheets.remove("genome")

# next loop through the config to make the containers


f    elif sh=="bigbed":
        bb = pd.read_excel(file, sheet_name=sh)
        bb_d = dict(zip(bb.columns.values.tolist(),bb.iloc[0,:].tolist()))
        bb_track = trackhub.Track(**bb_d)
        trackdb.add_tracks(bb_track)

    # if it's not a hub or a genome, then make a new track out of it
    elif sh=="bigwig":
        #what if there is no composite?
        # new empy subgroup list for each track type
        subgroups_list=[]
        #how to remove the composite specific params and keep the track and vice versa
        df = pd.read_excel(file, sheet_name=sh)
        #subgroups = track_df.filter(regex='^subgroup', axis=1)

        composite_list = df.composite.unique().tolist()
        for c in composite_list:
            composite_df = df[df['composite'] == c]
            composite = composite_df[["composite", "visibility", "tracktype"]]
            #track_df_no_composite = df.drop(track_df.filter(regex='composite|subgroup|super').columns, axis=1)
                # get the header
                # add only composite params
            composite_params = list(composite.columns.values)
            composite_dict = dict(zip(composite_params, composite.iloc[0,:].tolist()))
            composite_dict['name'] = composite_dict['composite']+'_composite'
            composite_dict.pop('composite')
            composite = trackhub.CompositeTrack(**composite_dict)

            view_list = composite_df.view.unique().tolist()

            track_df = df.drop(df.filter(regex='composite').columns, axis=1)

            subgroups = composite_df.filter(regex='^subgroup', axis=1)
            sub = subgroups.columns.tolist()
            for s in sub:
                group = s.split('_', 1)[1]
                a = list(set(subgroups[s].tolist()))
                # for each columns make a sub group def
                g = trackhub.SubGroupDefinition(
                    name=group,
                    label=group,
                    mapping={r:r for r in a}
                )
                #add to the list of subgroups for the composite track
                subgroups_list.append(g)
            composite.add_subgroups(subgroups_list)
            trackdb.add_tracks(composite)
            for v in view_list:

                view_df = df[df['view'] == v]
                view = view_df[["view", "visibility", "tracktype"]]
                # get the header
                params = list(track_df.columns.values)
                # add only view params
                view_params = list(view.columns.values)
                view_dict = dict(zip(view_params, view.iloc[0,:].tolist()))
                view_dict['name'] = view_dict['view']+'_view'
                view_track = trackhub.ViewTrack(**view_dict)
                composite.add_view(view_track)
                for index, row in view_df.iterrows():
                    #print(index)
                    track_df = df.drop(df.filter(regex='view|subgroup|composite').columns, axis=1)
                    subgroups = df.filter(regex='^subgroup', axis=1)

                    sub = subgroups.columns.tolist()
                    new_names = list()
                    for s in sub:
                        group_name = s.split('_', 1)[1]
                        new_names.append(group_name)
                    sub_dict = dict(zip(new_names, subgroups.iloc[index,:].tolist()))
                        # for each columns make a sub group def
                                        #add to the list of subgroups for the composite track
                    track_params = list(track_df.columns.values)
                    track_info = dict(zip(track_params, track_df.iloc[index,:].tolist()))
                    track_info['subgroups']=sub_dict
                    if sub_dict["strand"] == "positive":
                        track_info.pop('negateValues')

                    track = trackhub.Track(**track_info)

                    view_track.add_tracks(track)



#"/data/NICHD-core0/datashare/storz/borrelia-bb0268/track_hub"
s = file.split(".")[0]+"_staging"

trackhub.upload.upload_hub(hub=hub, host="helix.nih.gov", remote_dir=destination, staging=s)
