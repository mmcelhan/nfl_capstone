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
    f = open(os.path.join(local_path, "madden_build.json"))
    data = json.load(f)

    matching = hlp.return_matching_dict()  # get global matching dictionary

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    df = pd.DataFrame(columns=data['columns'])


    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    counter = 0  # first one will not be matched

    for file in data['file_list']:
        source = os.path.join(source_dir, file['folder'], file['file'])
        temp_df = pd.read_csv(source)
        temp_df.rename(columns=data['column_rename'], inplace=True)
        temp_df['year'] = data['year'][file['file']]  # add year
        temp_df['player_match_position'] = temp_df['position'].map(matching['position_groups'])
        temp_df = temp_df[data['columns']]  # cut all extra columns
        new_column_name = str(data['year'][file['file']]) + "_madden_rating"
        temp_df[new_column_name] = temp_df['madden_rating']
        print(temp_df)
        if counter == 0:
            df = df.append(temp_df)
        else:
            df = cm.fuzzy_merge(df, temp_df, ['first_name', 'last_name', 'position'],
                        ['first_name', 'last_name', 'position'], threshold=95, limit=1)
        counter += 1

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()