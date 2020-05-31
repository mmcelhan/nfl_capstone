import json
import os
import shutil
import pandas as pd


def make_folder_if_not_exists(path):
    """ creates a folder if it doesn't exist already """
    if not os.path.exists(path):
        os.makedirs(path)


def main():


    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "madden_build.json"))
    data = json.load(f)

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    df = pd.DataFrame(columns=data['columns'])


    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    for file in data['file_list']:
        source = os.path.join(source_dir, file['folder'], file['file'])
        temp_df = pd.read_csv(source)
        temp_df.rename(columns=data['column_rename'], inplace=True)
        temp_df['year'] = data['year'][file['file']]  # add year
        temp_df['player_match_position'] = ""
        temp_df = temp_df[data['columns']]  # cut all extra columns
        df = df.append(temp_df)

    target_folder = os.path.join(target_dir, data['output_folder'])
    make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df_players = df = df.pivot_table(
    values=['madden_rating'],
    index=['first_name', 'last_name', 'position'],
    columns='madden_rating'
    )

# Formatting.
    df.reset_index(inplace=True)
    df_players.to_csv("output.csv",index=False)
    df.to_csv(target, index=False)


main()