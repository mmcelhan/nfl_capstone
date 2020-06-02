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