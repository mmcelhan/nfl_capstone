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
    f = open(os.path.join(local_path, "dimensions_players_build.json"))
    data = json.load(f)
    matching = hlp.return_matching_dict()
    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['draft']['folder'], data['draft']['file'])
    df = pd.read_csv(source)
    print(len(df['college']))
    source = os.path.join(source_dir, data['college_players']['folder'], data['college_players']['file'])

    df2 = pd.read_csv(source)

    print("before merge")

    df = cm.fuzzy_merge(df, df2, ['full_name', 'position_group', 'college'],
                          ['full_name', 'position_group', 'college'], threshold=95, limit=1)  # inner join

    print("after merge")
    print(df)



    df.rename(columns=data['column_rename'], inplace=True)

    #df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()