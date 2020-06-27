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
    f = open(os.path.join(local_path, "facts_cities.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))
    source_dir = os.path.join(two_up, data['source'])
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(source_dir, data['econ_input']['folder'], data['econ_input']['file'])
    df = pd.read_csv(source)

    source = os.path.join(source_dir, data['weather_input']['folder'], data['weather_input']['file'])
    weather_df = pd.read_csv(source)
    weather_df = weather_df[data['weather_keep_columns']]

    df = df.merge(weather_df, on=['fms_city_id'], how='inner')

    df = df[data['keep_columns']]
    df.drop_duplicates(subset='fms_city_id', keep='last', inplace=True)

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()