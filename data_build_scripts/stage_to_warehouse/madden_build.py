import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp


def main():
    print("got to main madden build")
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
        temp_df['position_group'] = temp_df['position'].map(matching['position_groups'])
        temp_df = temp_df[data['columns']]  # cut all extra columns
        new_column_name = str(data['year'][file['file']]) + "_madden_rating"
        temp_df[new_column_name] = temp_df['madden_rating']
        if counter == 0:
            df = df.append(temp_df)
        else:
            df_1 = cm.fuzzy_merge(df, temp_df, ['first_name', 'last_name', 'position_group'],
                        ['first_name', 'last_name', 'position_group'], threshold=95, limit=1)  # inner join
            df_2 = pd.concat([temp_df, df_1])
            df = pd.concat([df, df_2])
            df = df.drop_duplicates(subset=['first_name', 'last_name', 'position_group'], keep='last')

        counter += 1

    df['section'] = df['position_group'].map(matching['section'])

    df.rename(columns=data['column_rename'], inplace=True)
    print(df.columns)
    df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


def add_espn_id():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "madden_build.json"))
    data = json.load(f)

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['target'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(source_dir, data['output_folder'], data['output_file'])

    df = pd.read_csv(source)
    espn_id_df = hlp.return_id_df(['first_name', 'last_name', 'position_group', 'id'])


    print("fuzzy merging madden outputs")
    df = cm.fuzzy_merge(df, espn_id_df, ['first_name', 'last_name', 'position_group'],
                        ['first_name', 'last_name', 'position_group'], threshold=95, limit=1)

    df = df[data['id_column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)

def add_fms_id():
    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "madden_build.json"))
    data = json.load(f)

    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source_dir = os.path.join(two_up, data['target'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(source_dir, data['output_folder'], data['output_file'])

    df = pd.read_csv(source)
    fms = hlp.return_fms_id_df(['first_name', 'last_name', 'position_group', 'fms_id'])

    print("fuzzy merging madden outputs")
    df = cm.fuzzy_merge(df, fms, ['first_name', 'last_name', 'position_group'],
                        ['first_name', 'last_name', 'position_group'], threshold=95, limit=1)

    df = df[data['fms_id_column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


