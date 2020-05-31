import os
import json

def make_folder_if_not_exists(path):
    """ creates a folder if it doesn't exist already """
    if not os.path.exists(path):
        os.makedirs(path)


def return_matching_dict():
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "matching.json"))
    data = json.load(f)
    return data