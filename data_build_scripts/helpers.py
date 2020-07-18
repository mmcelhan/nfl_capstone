import os
import json
import pandas as pd
import csv
from scipy.stats import zscore

def make_folder_if_not_exists(path):
    """ creates a folder if it doesn't exist already """
    if not os.path.exists(path):
        os.makedirs(path)


def return_matching_dict():
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "matching.json"))
    data = json.load(f)
    return data


def write_matching_dict(d):
    local_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(local_path, "matching.json"), "w") as fp:
        json.dump(d, fp)
    None  # end function

def currency_to_float(f):
    f = str(f)
    f = f.replace(',', '')
    f = f.replace('$', '')
    f = pd.to_numeric(f, errors='coerce')
    f = f.astype("Float32")
    return f


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


def return_fms_college_id(keep_columns = ['fms_college_id', 'college']):
    local_path = os.path.dirname(os.path.abspath(__file__))
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    source = open(os.path.join(one_up, "data_warehouse", "master_wh", "college_master.csv"))
    df = pd.read_csv(source)
    df = df[keep_columns]
    return df


def return_fms_city_id(keep_columns = ['fms_city_id', 'city_state']):
    local_path = os.path.dirname(os.path.abspath(__file__))
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    source = open(os.path.join(one_up, "data_warehouse", "master_wh", "geo_master.csv"))
    df = pd.read_csv(source)
    df = df[keep_columns]
    return df


def write_representative_statistics(attribute, mean=0, stdev=0, min=0, max=0):
    local_path = os.path.dirname(os.path.abspath(__file__))
    one_up = os.path.abspath(os.path.join(local_path, ".."))
    path = os.path.join(one_up, "data_mart", "representative_statistics.csv")
    if not os.path.exists(path):
        index = ["mean", "stden", "min", "max"]
        df = pd.DataFrame(index=index)
        df.to_csv(path)
    else:
        source = open(os.path.join(one_up, "data_mart", "representative_statistics.csv"))
        df = pd.read_csv(source)
        df[attribute] = [mean, stdev, min, max]
        df.to_csv(path, index=False)


