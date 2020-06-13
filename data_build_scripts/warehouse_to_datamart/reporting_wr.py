import json
import os
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import data_build_scripts.helpers as hlp


def main():

    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "reporting_wr.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))

    source = os.path.join(two_up, data['dimension_players']['folder'], data['dimension_players']['file'])
    target_dir = os.path.join(two_up, data['target'])
    df = pd.read_csv(source)
    df = df[df['position'].str.contains("WR")]

    ###  player stats ###

    source = os.path.join(two_up, data['facts_player_metrics']['folder'], data['facts_player_metrics']['file'])
    player_stats_df = pd.read_csv(source)

    df = pd.merge(df, player_stats_df, on='fms_id', how='left')
    df = df.drop_duplicates(subset='fms_id', keep='last')


    ### math transformations ###

    df['hw_ratio'] = df['college_height_inches'] / df['college_weight_pounds']

    ### apply z score ###

    z_score_list = []  # to add te output df
    for col in data['z_score_columns']:
        col_zscore = col + '_zscore'
        z_score_list.append(col_zscore)
        df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)

    #print(z_score_list)



    df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()