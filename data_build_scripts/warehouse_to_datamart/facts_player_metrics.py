import json
import os
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp

def moving_average(l, window=3):
    l = [a for a in l if pd.notnull(a)]
    l = l[-window:]
    l = [float(a) for a in l]
    print(l)
    moving_avg = sum(l)/len(l)
    return moving_avg

def test_roll(data):
    return data.rolling(window=3, min_periods=1, axis=0).mean()


def main():



    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "facts_player_metrics.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))
    source = os.path.join(two_up, data['dimension_players']['folder'], data['dimension_players']['file'])
    df = pd.read_csv(source)
    df = df['fms_id']
    #print(len(df))

    ###  madden stats ###

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['madden_ratings']['folder'], data['madden_ratings']['file'])

    madden_df = pd.read_csv(source)
    madden_df = madden_df[data["madden_keep_pre"]]
    # drop duplicates, need to fix this later
    madden_df = madden_df.drop_duplicates(subset='fms_id', keep='last')

    madden_df['max_madden'] = np.nanmax(madden_df[madden_df.columns.difference(['fms_id'])].values, axis=1)
    # madden_df['max_madden'] = madden_df.apply(moving_average(list(madden_df.columns.difference(['fms_id']))))
    # madden_df['max_madden'] = madden_df.apply(lambda row: moving_average(madden_df.columns.difference(['fms_id'])))
    #madden_df['max_madden'] = madden_df.apply(test_roll, axis=1)

    madden_df = madden_df[data['madden_keep_post']]

    df = pd.merge(df, madden_df, left_on=['fms_id'], right_on=['fms_id'], how='left')
    #print(len(df['fms_id']))

    ### combine stats ###

    source = os.path.join(source_dir, data['combine_stats']['folder'], data['combine_stats']['file'])
    combine_df = pd.read_csv(source)

    # drop duplicates, need to fix this later
    combine_df = combine_df.drop_duplicates(subset='fms_id', keep='last')
    df = pd.merge(df, combine_df, left_on=['fms_id'], right_on=['fms_id'], how='left')
    #print(len(df['fms_id']))


    ### college stats ###

    source = os.path.join(source_dir, data['college_stats']['folder'], data['college_stats']['file'])

    df_college_stats = pd.read_csv(source)

    # drop duplicates, need to fix this later
    df_college_stats = df_college_stats.drop_duplicates(subset='fms_id', keep='last')

    df = pd.merge(df, df_college_stats, on='fms_id', how='left')  # left join

    df.rename(columns=data['column_rename'], inplace=True)

    df = df[data['column_order']]

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()