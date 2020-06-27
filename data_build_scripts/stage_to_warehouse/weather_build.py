import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import data_build_scripts.helpers as hlp


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "weather_build.json"))
    data = json.load(f)

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(source_dir, data['homewtown_weather']['folder'], data['homewtown_weather']['file'])
    df = pd.read_csv(source)


    df.rename(columns=data['column_rename'], inplace=True)

    source = os.path.join(source_dir, data['collegetown_weather']['folder'], data['collegetown_weather']['file'])
    college_town_df = pd.read_csv(source)
    college_town_df.rename(columns=data['column_rename'], inplace=True)

    df = df.append(college_town_df, ignore_index=True)

    city_df = hlp.return_fms_city_id()

    df = df.merge(city_df, on='city_state', how='left')

    df = df[data['column_keep']]

    df.drop_duplicates(subset='fms_city_id', keep='last', inplace=True)

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()