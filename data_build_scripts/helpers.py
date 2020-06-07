import os
import json
import pandas as pd
import csv

def make_folder_if_not_exists(path):
    """ creates a folder if it doesn't exist already """
    if not os.path.exists(path):
        os.makedirs(path)


def return_matching_dict():
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "matching.json"))
    data = json.load(f)
    return data


def return_college_matching_dict():
    local_path = os.path.dirname(os.path.abspath(__file__))
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    f = open(os.path.join(one_up, "school_mapping", "school_mapping.csv"), encoding='utf-8-sig')
    data = {row["title"]: row["value"] for row in csv.DictReader(f, ("title", "value"))}
    return data


def return_id_df(keep_columns=['last_name', 'position_group', 'college', 'espn_id']):
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "stage_to_warehouse", "college_players_build.json"))
    data = json.load(f)
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    source_dir = os.path.join(one_up, data['source'])  # should work in both mac and windows
    source = os.path.join(source_dir, data['folder'], data['file'])
    df = pd.read_csv(source)
    df['position_group'] = df['position'].map(return_matching_dict()['position_groups'])
    df.rename(columns={'school': 'college', 'id': 'espn_id'}, inplace=True)
    df = df[keep_columns]
    return df


def return_fms_id_df(keep_columns=['fms_id', 'first_name', 'last_name', 'college', 'position_group']):
    local_path = os.path.dirname(os.path.abspath(__file__))
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    source = open(os.path.join(one_up, "data_warehouse", "master_wh", "player_master.csv"))
    df = pd.read_csv(source)
    df = df[keep_columns]
    return df

