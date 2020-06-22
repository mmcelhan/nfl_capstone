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
    f = open(os.path.join(local_path, "college_master.json"))
    data = json.load(f)
    matching = hlp.return_matching_dict()
    school_matching = hlp.return_college_matching_dict()


    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    # pull in combine

    source = os.path.join(source_dir, data['combine']['folder'], data['combine']['file'])
    combine_df = pd.read_csv(source)
    combine_df = combine_df[data['combine_keep']].drop_duplicates(subset='college').reset_index(drop=True)
    combine_df['college'] = combine_df['college'].map(school_matching).fillna(combine_df['college'])

    # pull in college weather

    source = os.path.join(source_dir, data['college_weather']['folder'], data['college_weather']['file'])
    college_weather_df = pd.read_csv(source)
    college_weather_df.rename(columns=data['college_weather_rename'], inplace=True)
    college_weather_df = college_weather_df[data['college_weather_keep']].drop_duplicates(subset='college').reset_index(drop=True)
    college_weather_df['college'] = college_weather_df['college'].map(school_matching).fillna(college_weather_df['college'])

    # pull in college econ

    source = os.path.join(source_dir, data['college_econ']['folder'], data['college_econ']['file'])
    college_econ_df = pd.read_csv(source)
    college_econ_df.rename(columns=data['college_econ_rename'], inplace=True)
    college_econ_df = college_econ_df[data['college_econ_keep']].drop_duplicates(subset='college').reset_index(
        drop=True)
    college_econ_df['college'] = college_econ_df['college'].map(school_matching).fillna(college_econ_df['college'])

    # pull in college funding data
    source = os.path.join(source_dir, data['college_budget']['folder'], data['college_budget']['file'])
    college_budget_df = pd.read_csv(source)
    college_budget_df.rename(columns=data['college_budget_rename'], inplace=True)
    college_budget_df = college_budget_df[data['college_budget_keep']].drop_duplicates(subset='college').reset_index(
        drop=True)
    college_budget_df['college'] = college_budget_df['college'].map(school_matching).fillna(college_budget_df['college'])


    sources_list = [combine_df, college_weather_df, college_econ_df, college_budget_df]

    df, matching_dict = gld.golden_source_merge(sources_list, ['college'], 98)

    matching_dict['Texas'] = 'Texas'  # hand jam Texas so it doesn't match with Texas College

    # remap names
    combine_df['college'] = combine_df['college'].map(matching_dict).fillna(combine_df['college'])
    combine_df['college'] = combine_df['college'].map(matching['college']).fillna(combine_df['college'])

    college_weather_df['college'] = college_weather_df['college'].map(matching_dict).fillna(college_weather_df['college'])
    college_weather_df['college'] = college_weather_df['college'].map(matching['college']).fillna(college_weather_df['college'])

    college_econ_df['college'] = college_econ_df['college'].map(matching_dict).fillna(
        college_econ_df['college'])
    college_econ_df['college'] = college_econ_df['college'].map(matching['college']).fillna(
        college_econ_df['college'])

    college_budget_df['college'] = college_budget_df['college'].map(matching_dict).fillna(
        college_budget_df['college'])
    college_budget_df['college'] = college_budget_df['college'].map(matching['college']).fillna(
        college_budget_df['college'])


    df = df.merge(combine_df, how='left', on='college').drop_duplicates(subset='college').reset_index(
        drop=True)
    df = df.merge(college_weather_df, how='left', on='college').drop_duplicates(subset='college').reset_index(
        drop=True)
    df = df.merge(college_econ_df, how='left', on='college').drop_duplicates(subset='college').reset_index(
        drop=True)

    df = df.merge(college_budget_df, how='left', on='college').drop_duplicates(subset='college').reset_index(
        drop=True)


    df['city'] = df['city_state'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else "")
    df['state'] = df['city_state'].apply(lambda x: x.split(',')[1]if isinstance(x, str) else "")
    df = df.assign(fms_college_id=(df['college']).astype('category').cat.codes)

    df = df[data['keep_columns']]

    new_dict = {}
    new_dict['college'] = matching_dict



    matching.update(new_dict)
    hlp.write_matching_dict(matching)

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)

main()