import json
import os
import pandas as pd
import numpy as np
import sys
sys.path.append("..")
sys.path.append("../../column_matching")
import column_matching.column_match as cm
import data_build_scripts.helpers as hlp


def main():



    local_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(local_path, "facts_college_metrics.json"))
    data = json.load(f)
    two_up = os.path.abspath(os.path.join(local_path, "../.."))
    source = os.path.join(two_up, data['dimension_colleges']['folder'], data['dimension_colleges']['file'])
    df = pd.read_csv(source)
    df = df['fms_college_id']

    source_dir = os.path.join(two_up, data['source'])  # should work in both mac and windows
    target_dir = os.path.join(two_up, data['target'])
    source = os.path.join(source_dir, data['college_budget']['folder'], data['college_budget']['file'])

    college_budget_df = pd.read_csv(source)

    df = pd.merge(df, college_budget_df, left_on=['fms_college_id'], right_on=['fms_college_id'], how='left')

    df.rename(columns=data['column_rename'], inplace=True)

    #df = df[data['column_order']]

    """
    z_score_list = []  # to add te output df
    for col in data['z_score_columns']:
        col_zscore = col + '_zscore'
        z_score_list.append(col_zscore)
        df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)
    """

    target_folder = os.path.join(target_dir, data['output_folder'])
    hlp.make_folder_if_not_exists(target_folder)
    target = os.path.join(target_folder, data['output_file'])
    df.to_csv(target, index=False)


main()