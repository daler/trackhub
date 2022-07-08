import pandas as pd
import numpy as np
import trackhub

# import argparse
from openpyxl import load_workbook
import xlrd
import sys

# excel_file = argparse.ArgumentParser(description='Process some integers.')
# excel_file.add_argument('excel-file', metavar='e', type=str,nargs='?',help='path to excel file for track hub')
# args = parser.parse_args()

# file = sys.argv[1]

file = "universal_trackhub.xlsx"

# destination = sys.argv[2]

# get the sheet names
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
# TODO: without assembly
genome_dict = sheet_to_dict(file, sheet="genome")
genome = trackhub.Assembly(**genome_dict)

genomes_file = trackhub.GenomesFile()
hub.add_genomes_file(genomes_file)
trackdb = trackhub.TrackDb()
genome.add_trackdb(trackdb)
genomes_file.add_genome(genome)

# we also need to create a trackDb and add it to the genome
trackdb = trackhub.TrackDb()
genome.add_trackdb(trackdb)

# all_tracks =  add the genome to the genomes file here:
genomes_file.add_genome(genome)

sheets.remove("hub")
sheets.remove("genome")

all_super_tracks = {}
all_composite_tracks = {}
all_view_tracks = {}
all_aggregate_tracks = {}

if "super_config" in sheets:
    # takes a data frame and returns a list of dictionaries
    # the keys are the headers and the values are row values
    list_of_super_tracks_as_dict = pd.read_excel(
        file, sheet_name="super_config"
    ).to_dict(orient="records")
    for supertrack in list_of_super_tracks_as_dict:
        supertrack_object = trackhub.SuperTrack(**supertrack)
        all_super_tracks[supertrack["name"]] = supertrack_object
        trackdb.add_tracks(supertrack_object)
    if "composite_config" in sheets:
        # takes a data frame and returns a list of dictionaries
        # the keys are the headers and the values are row values
        list_of_composite_tracks_as_dict = pd.read_excel(
            file, sheet_name="composite_config"
        ).to_dict(orient="records")
        for composite in list_of_composite_tracks_as_dict:
            supertrack = composite["super"]
            del composite["super"]

            compositetrack_object = trackhub.CompositeTrack(**composite)
            all_composite_tracks[composite["name"]] = compositetrack_object
            all_super_tracks[supertrack].add_tracks(compositetrack_object)
    if "view_config" in sheets:
        list_of_view_tracks_as_dict = pd.read_excel(
            file, sheet_name="view_config"
        ).to_dict(orient="records")
        for view in list_of_view_tracks_as_dict:
            compositetrack = view["composite"]
            del view["composite"]
            viewtrack_object = trackhub.ViewTrack(**view)
            all_view_tracks[view["name"]] = viewtrack_object
            all_composite_tracks[compositetrack].add_tracks(viewtrack_object)

elif "composite_config" in sheets:
    list_of_composite_tracks_as_dict = pd.read_excel(
        file, sheet_name="composite_config"
    ).to_dict(orient="records")
    for composite in list_of_composite_tracks_as_dict:
        compositetrack_object = trackhub.CompositeTrack(**composite)
        all_composite_tracks[composite["name"]] = compositetrack_object
        trackdb.add_tracks(compositetrack_object)
    if "view_config" in sheets:
        list_of_view_tracks_as_dict = pd.read_excel(
            file, sheet_name="view_config"
        ).to_dict(orient="records")
        for view in list_of_view_tracks_as_dict:
            #new_dict = {key: val for key, val in view.items() if key != "composite"}
            comp = view["composite"]

            del view["composite"]
            viewtrack_object = trackhub.ViewTrack(**new_dict)
            all_view_tracks[view["name"]] = viewtrack_object
            all_composite_tracks[view[comp]].add_tracks(viewtrack_object)

track_sheets = [item for item in sheets if "config" not in item]
all_tracks_dict = []
track_dicts = []
for t in track_sheets:
    #turns rows of sheet into list of dictionaries
    track_dicts.extend(pd.read_excel(file, sheet_name=t).to_dict(orient="records"))

def prepare_track_dict(track_dictionary):
    new_dict = {}
    for k,v in track_dictionary.items():
        if not isinstance(v,str) and np.isnan(float(v)):
            continue
        else:
            new_dict[k]=v
    #print(new_dict)
    parameters = trackhub.constants.track_fields[new_dict['tracktype']][:]
    #print(parameters)
    parameters.extend(trackhub.constants.track_fields['all'][:])
    parameters.extend(["source", "tracktype","name"])
    track_dict_new = {k:v for k,v in new_dict.items() if k in parameters}
    #print(track_dict_new)
    return track_dict_new
#trackhub.Track(**track_dict_new)

composite_to_subgroups_dict = {}
track_to_subgroups = {}
# iterate through all of the tracks
subgroup_to_options={}
for track_dict in track_dicts:
    # add the track to the appropriate container
    track = prepare_track_dict(track_dict)
    track = trackhub.Track(**track)

    if 'view' in track_dict:
        all_view_tracks[track_dict['view']].add_tracks(track)
    elif 'composite' in track_dict:
        all_composite_tracks[track_dict['composite']].add_tracks(track)
    elif 'supertrack' in track_dict:
        all_super_tracks[track_dict['supertrack']].add_tracks(track)
    else:
        trackdb.add_tracks(track)

    # here we are dealing with subgroups
    subgroups_set = set()
    # what about the case where there is a composite but no subgroups?
    # subgroups are present in composite track. is there is no composite track define then there can be no subgroups
    if 'composite' in track_dict:
        subgroup_dict = {}
        for k,v in track_dict.items():
            # find items in dicitonary that start with subgroup
            if "subgroup" in k:

                new_subgroup = k.replace("subgroup_","")
                #get the full set of subgroups for the track
                if new_subgroup in subgroup_to_options:
                    subgroup_to_options[new_subgroup].extend([v])
                    subgroup_to_options[new_subgroup] = list(set(subgroup_to_options[new_subgroup]))
                else:
                    subgroup_to_options[new_subgroup] = [v]
                #print(subgroup_to_options)
                # keep track of subgroup and value for the track
                subgroup_dict[new_subgroup] = v
        if len(subgroup_dict) == 0:
            continue
        # add the full set of subgroups the a dictioary the converts composite to subgroups
        # turn it into a list so it can be iterated on later
        composite_to_subgroups_dict[track_dict['composite']] = subgroup_to_options
        # add the dictionary pf subgroups to a dictionary that goes from track to subgroup
        track_to_subgroups[track_dict['name']] = subgroup_dict

for composite,subgroup_options in composite_to_subgroups_dict.items():
    subgroups = []

    for subgroup_name, options in subgroup_options.items():

        mapping_dict = {group: group for group in subgroup_options}

        s = trackhub.SubGroupDefinition(
            name = subgroup_name,
            label = subgroup_name,
            mapping = mapping_dict)

        subgroups.append(s)
    all_composite_tracks[composite].add_subgroups(subgroups)



# trackhub.upload.upload_hub(hub=hub, host="helix.nih.gov", remote_dir=destination, staging=s)
