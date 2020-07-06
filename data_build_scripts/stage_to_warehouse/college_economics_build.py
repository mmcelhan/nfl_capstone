import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp


def main():
    school_matching = hlp.return_college_matching_dict()


    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "college_economics_build.json"))
    data = json.load(f)
    hlp.return_college_matching_dict()

    matching = hlp.return_matching_dict()

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['folder'], data['file'])
    df = pd.read_csv(source)
    df.rename(columns=data['column_rename'], inplace=True)
    df = df[data['column_keep']]

    for column in data['numerical_columns']:
        df[column] = df[column].apply(hlp.currency_to_float)  # convert currency to float, remove $ and ,

    df['college'] = df['college'].map(school_matching).fillna(df['college'])
    df['college'] = df['college'].map(matching['college']).fillna(df['college'])


    #df = df.groupby('college').mean().reset_index()

    master_college_df = hlp.return_fms_college_id()

    df = df.merge(master_college_df, on='college', how='left')

    df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()