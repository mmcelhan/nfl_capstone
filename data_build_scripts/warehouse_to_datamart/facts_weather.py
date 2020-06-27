import json
import os
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp


def main():



    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "facts_weather.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))
    source_dir = os.path.join(two_up, data['source'])
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(source_dir, data['weather_input']['folder'], data['weather_input']['file'])
    df = pd.read_csv(source)

    df = df[data['keep_columns']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()