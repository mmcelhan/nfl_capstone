import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "draft_stats_build.json"))
    data = json.load(f)

    matching = hlp.return_matching_dict()

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['folder'], data['file'])
    df = pd.read_csv(source)
    df['first_name'] = df['player'].str.split(' ').str[0]
    df['last_name'] = df['player'].str.split(' ').str[1]
    df['position_group'] = df['pos'].map(matching['position_groups'])
    df['section'] = df['position_group'].map(matching['section'])
    df['position_rank'] = df.groupby(['year', 'pos'])['pick'].rank(method='first')
    df['position_group_rank'] = df.groupby(['year', 'position_group'])['pick'].rank(method='first')
    df['section_rank'] = df.groupby(['year', 'section'])['pick'].rank(method='first')
    df.rename(columns=data['column_rename'], inplace=True)

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()