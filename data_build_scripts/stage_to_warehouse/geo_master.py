import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp
import gold_source_mapping.gold_source_merging as gld


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "geo_master.json"))
    data = json.load(f)
    matching = hlp.return_matching_dict()

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    # pull in colleges

    source = os.path.join(source_dir, data['colleges']['folder'], data['colleges']['file'])
    college_cities_df = pd.read_csv(source)

    college_cities_df = college_cities_df[data['college_keep']]
    college_cities_df.rename(columns=data["college_df_rename"], inplace=True)


    source = os.path.join(source_dir, data['hometowns']['folder'], data['hometowns']['file'])
    hometown_df = pd.read_csv(source)

    hometown_df = hometown_df[data['hometowns_keep']]
    hometown_df.rename(columns=data["hometown_df_rename"], inplace=True)

    sources_list = [college_cities_df, hometown_df]

    df, matching_dict = gld.golden_source_merge(sources_list, ['city_state'], 98)
    hometown_df['city_state'] = hometown_df['city_state'].map(matching_dict).fillna(hometown_df['city_state'])
    college_cities_df['city_state'] = college_cities_df['city_state'].map(matching_dict).fillna(college_cities_df['city_state'])

    print(hometown_df)

    df = df.merge(hometown_df, how='left', on='city_state')
    df = df.merge(college_cities_df, how='left', on='city_state')
    df['latitude'] = df['latitude_x'].combine_first(df['latitude_y'])
    df['longitude'] = df['longitude_x'].combine_first(df['longitude_y'])

    df['city'] = df['city_state'].apply(lambda x: x.split(',')[0])
    df['state'] = df['city_state'].apply(lambda x: x.split(',')[1])
    df = df.assign(fms_city_id=(df['city_state']).astype('category').cat.codes)
    df['country'] = ""  # to be filled in later

    df = df[data['keep_columns']]

    new_dict = {}
    new_dict['cities'] = matching_dict



    matching.update(new_dict)
    hlp.write_matching_dict(matching)

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()