import pandas as pd
import numpy as np
import trackhub
from collections import defaultdict

# import argparse
from openpyxl import load_workbook
import xlrd
import sys

file = sys.argv[1]
# destination = sys.argv[2]

#file = "universal_trackhub.xlsx"

# Get the sheet names from the Excel Workbook
sheets = xlrd.open_workbook(file, on_demand=True).sheet_names()


def sheet_to_dict(file, sheet):
    """
    Read a  two columns sheet and make it into a dictionary with the first
    column as keys and the second as the values of a dictionary

    Parameters
    ----------
    file : str
        Name of the Excel file to be read

    sheet : str
        Name of sheet in the Excel file to be read

    Returns
    -------
    dict
        A dictionary of a two column sheet with the keys as the first column
        and values as the second column
    """
    sheet = pd.read_excel(file, sheet_name=sheet, header=None)
    sheet_dict = dict(sheet.values.tolist())
    return sheet_dict


# There must be a sheet named "hub"
hub_dict = sheet_to_dict(file, sheet="hub")

# If using an assembly, then there must be a "genome" sheet
if "genome" in sheets:

    hub = trackhub.Hub(**hub_dict)
    sheets.remove("hub")
    # Make the genome
    genome_dict = sheet_to_dict(file, sheet="genome")
    genome = trackhub.Assembly(**genome_dict)

    genomes_file = trackhub.GenomesFile()
    hub.add_genomes_file(genomes_file)

    trackdb = trackhub.TrackDb()
    trackdb = trackhub.TrackDb()

    genome.add_trackdb(trackdb)
    genomes_file.add_genome(genome)

    # Create a trackDb and add it to the genome
    genome.add_trackdb(trackdb)

    # Add the genome to the genomes file here:
    genomes_file.add_genome(genome)
    sheets.remove("genome")

else:
    hub, genomes_file, genome, trackdb = trackhub.default_hub(**hub_dict)

# These dictionary keep track of all of the container tracks
all_super_tracks = {}
all_composite_tracks = {}
all_view_tracks = {}
all_aggregate_tracks = {}


# ALL THE POSSIBLE WAYS TO ADD A TRACK
# trackdb <- super track <- composite track <- view track <- aggregate track <- track
# trackdb <- super track <- composite track <- aggregate track <- track
# trackdb <- composite track <- aggregate track <- track
# trackdb <- super track <- aggregate track <- track
# trackdb <- super track <- composite track <- track
# trackdb <- aggregate track <- track
# trackdb <- composite track <- track
# trackdb <- track

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
        if supertrack in all_super_tracks:
            all_super_tracks[supertrack].add_tracks(compositetrack_object)
        else:
            trackdb.add_tracks(compositetrack_object)

if "view_config" in sheets:
    list_of_view_tracks_as_dict = pd.read_excel(file, sheet_name="view_config").to_dict(
        orient="records"
    )
    for view in list_of_view_tracks_as_dict:
        composite = view["composite"]
        del view["composite"]
        viewtrack_object = trackhub.ViewTrack(**view)
        all_view_tracks[view["name"]] = viewtrack_object
        all_composite_tracks[composite].add_tracks(viewtrack_object)

if "aggregate_config" in sheets:
    list_of_aggregate_tracks_as_dict = pd.read_excel(
        file, sheet_name="aggregate_config"
    ).to_dict(orient="records")
    for agg in list_of_aggregate_tracks_as_dict:
        container = agg["container"]
        del agg["container"]
        agg_object = trackhub.AggregateTrack(**agg)
        all_aggregate_tracks[agg["name"]] = agg_object
        if container in all_view_tracks:
            all_view_tracks[container].add_tracks(agg_object)
        if container in all_composite_tracks:
            all_composite_tracks[container].add_tracks(agg_object)
        if container in all_super_tracks:
            all_super_tracks[container].add_tracks(agg_object)
        else:
            trackdb.add_tracks(agg_object)

all_tracks_dict_list = []


def prepare_track_dict(track_dictionary):
    new_dict = {}
    for k, v in track_dictionary.items():
        if not isinstance(v, str) and np.isnan(float(v)):
            continue
        else:
            new_dict[k] = v
    parameters = trackhub.constants.track_fields[new_dict["tracktype"]][:]
    parameters.extend(trackhub.constants.track_fields["all"][:])
    parameters.extend(trackhub.constants.trackhub_specific)
    track_dict_new = {k: v for k, v in new_dict.items() if k in parameters}
    return track_dict_new


for sheet in sheets:
    if "config" not in sheet:
        list_of_dicts = pd.read_excel(file, sheet_name=sheet).to_dict(orient="records")
        all_tracks_dict_list.extend(list_of_dicts)

# iterate through all of the tracks
composite_to_subgroups_dict = {}
track_to_subgroups = {}
subgroup_to_options = {}
for track_dict in all_tracks_dict_list:
    # add the track to the appropriate container
    track = prepare_track_dict(track_dict)
    track = trackhub.Track(**track)
    if "parent" in track_dict:
        parent = track_dict["parent"]
    else:
        parent = "none"

    if parent in all_aggregate_tracks:
        all_aggregate_tracks[parent].add_tracks(track)
    if parent in all_view_tracks:
        all_view_tracks[parent].add_tracks(track)
    if parent in all_composite_tracks:
        all_composite_tracks[parent].add_tracks(track)
    if parent in all_super_tracks:
        all_super_tracks[parent].add_tracks(track)
    else:
        trackdb.add_tracks(track)

    # here we are dealing with subgroups
    subgroups_set = set()
    # what about the case where there is a composite but no subgroups?
    # subgroups are present in composite track. is there is no composite track define then there can be no subgroups
    if "composite" in track_dict:
        subgroup_to_options = defaultdict(set)
        subgroup_dict = {}
        for k, v in track_dict.items():
            # find items in dictionary that start with subgroup
            if "subgroup" in k:
                # print(k)

                new_subgroup = k.replace("subgroup_", "")
                # get the full set of subgroups for the track
                # if new_subgroup in subgroup_to_options:
                subgroup_to_options[new_subgroup] |= set([v])
                # else:
                #   subgroup_to_options[new_subgroup] = set([v])
                # print(subgroup_to_options)
                # keep track of subgroup and value for the track
                subgroup_dict[new_subgroup] = v
        if len(subgroup_dict) == 0:
            continue
        # add the full set of subgroups the a dictioary the converts composite to subgroups
        # turn it into a list so it can be iterated on later
        composite_to_subgroups_dict[track_dict["composite"]] = subgroup_to_options
        # add the dictionary pf subgroups to a dictionary that goes from track to subgroup
        track_to_subgroups[track_dict["name"]] = subgroup_dict

for composite, subgroup_options in composite_to_subgroups_dict.items():
    subgroups = []

    for subgroup_name, options in subgroup_options.items():

        mapping_dict = {group: group for group in subgroup_options}

        s = trackhub.SubGroupDefinition(
            name=subgroup_name, label=subgroup_name, mapping=mapping_dict
        )

        subgroups.append(s)
    all_composite_tracks[composite].add_subgroups(subgroups)
