import json
import os
import pandas as pd
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import data_build_scripts.helpers as hlp


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "reporting_rb.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))
    target_dir = os.path.join(two_up, data['target'])

    source = os.path.join(two_up, data['dimension_players']['folder'], data['dimension_players']['file'])
    df = pd.read_csv(source)
    df = df[df['position'].str.contains("RB")]

    ### get city IDs for colleges

    source = os.path.join(two_up, data['dimension_colleges']['folder'], data['dimension_colleges']['file'])
    college_city_df = pd.read_csv(source)
    college_city_df = college_city_df[data['dimension_colleges_keep_columns']]
    print(college_city_df)

    ### merge dimension players and dimension colleges ###

    df = pd.merge(df, college_city_df, on='fms_college_id', how='left')
    df = df.drop_duplicates(subset='fms_id', keep='last')

    print(df)

    ### player stats ###

    source = os.path.join(two_up, data['facts_player_metrics']['folder'], data['facts_player_metrics']['file'])
    player_stats_df = pd.read_csv(source)

    df = pd.merge(df, player_stats_df, on='fms_id', how='left')
    df = df.drop_duplicates(subset='fms_id', keep='last')

    ### college stats ###

    source = os.path.join(two_up, data['facts_college_metrics']['folder'], data['facts_college_metrics']['file'])
    college_stats_df = pd.read_csv(source)
    college_stats_df = college_stats_df[data['college_stats_keep_columns']]
    college_stats_df = college_stats_df.groupby('fms_college_id').mean().reset_index()


    df = pd.merge(df, college_stats_df, left_on='fms_college_id', right_on='fms_college_id', how='left')
    df = df.drop_duplicates(subset='fms_id', keep='last')


    ### city stats ###

    source = os.path.join(two_up, data['facts_cities_metrics']['folder'], data['facts_cities_metrics']['file'])
    city_stats_df = pd.read_csv(source)

    df = pd.merge(df, city_stats_df, left_on='fms_city_id', right_on='fms_city_id', how='left')
    df = df.drop_duplicates(subset='fms_id', keep='last')




    ### math transformations ###

    df['hw_ratio'] = df['college_height_inches'] / df['college_weight_pounds']


    for column in data['per_game_columns']:
        new_name = str(column) + '_pg'
        df[new_name] = df[column]/df['rushing_games']

    ### apply z score ###


    z_score_list = []  # to add te output df
    for col in data['z_score_columns']:
        col_zscore = col + '_zscore'
        z_score_list.append(col_zscore)
        df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)


    df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()