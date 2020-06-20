import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import process
import json
import os

pd.options.mode.chained_assignment = None  # default='warn'

def format_match_string(string):
    """ function that converts to lower case and removes common words """
    string = string.lower().split()
    string = [word for word in string if word not in common_words]
    string = ' '.join(string)
    return string


def return_matching_dictionary(right_df, left_df, key, threshold=80):
    key = key[0]
    right_df = right_df.loc[right_df['not_matched'] == 0]  # keep the  matched columns
    right_df.rename(columns={key: 'original_key'}, inplace=True)

    left_df.loc[:, 'value_match'] = left_df.match.map(lambda x: x[0][0] if x[0][1] >= threshold else "")
    left_df = left_df[[key, 'value_match']]

    left_df = left_df.merge(right_df, how='inner', left_on='value_match', right_on='match_key')

    left_df = left_df[['original_key', key]]
    matching_dict = left_df.set_index('original_key')[key].to_dict()

    for k in list(matching_dict):
        if matching_dict[k] == k:
            del matching_dict[k]

    return matching_dict


def golden_source_merge(df_list, key, threshold=80, limit=1):
    """

    """


    # create null match columns

    matching_dict = {}

    df_1 = df_list.pop(0)
    df_1 = df_1[key]  # drop all other columns

    df_1.drop_duplicates(subset=key, inplace=True)  # drop duplicates

    for df_2 in df_list:

        df_2 = df_2[key]  # drop all other columns


        df_1['match_key'] = ''
        df_2['match_key'] = ''
        df_2.drop_duplicates(subset=key, inplace=True)  # drop duplicates


        # combines the list of column inputs into a single string for matching
        for value in key:
            df_1['match_key'] = df_1['match_key'].map(str) + ' ' + df_1[value].map(str)

        for value in key:
            df_2['match_key'] = df_2['match_key'].map(str) + ' ' + df_2[value].map(str)

        # remove periods for abreviated names
        df_1['match_key'] = df_1['match_key'].map(lambda x: x.strip(".,!"))
        df_2['match_key'] = df_2['match_key'].map(lambda x: x.strip(".,!"))

        # applies lower case and removes common words like "college" and "the"
        df_1['match_key'] = df_1['match_key'].apply(format_match_string)
        df_2['match_key'] = df_2['match_key'].apply(format_match_string)

        # the match process-creates the match keys to a list, matches, then saves them in the match column
        r = df_1['match_key'].tolist()
        s = df_2['match_key'].tolist()

        m = df_1['match_key'].apply(lambda x:
                                    process.extract(x, s, limit=limit, scorer=fuzzywuzzy.fuzz.token_sort_ratio))
        df_1['match'] = m


        df_2_matches = df_2['match_key'].apply(lambda x:
                                    process.extract(x, r, limit=limit, scorer=fuzzywuzzy.fuzz.token_sort_ratio))\
                                    .apply(lambda x: [i[1] for i in x if i[1] < threshold])\
                                    .apply(lambda x: 1 if x else 0)  # 0 if empty list

        df_2 = df_2.merge(df_2_matches.rename('not_matched'), left_index=True, right_index=True)

        matching_dict.update(return_matching_dictionary(df_2, df_1, key, threshold))

        df_2 = df_2.loc[df_2['not_matched'] == 1]

        # drop the score value and only keep the match words
        m2 = df_1['match'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
        df_1['match'] = m2

        # merge based on the matches, suffixes to drop the columns later
        temp_df = df_1.merge(df_2, left_on='match', right_on='match_key', suffixes=['', '_y'])

        # add back in df1 values that were dropped

        df_1 = pd.concat([df_1, temp_df]).drop_duplicates(key)

        # add in df2 values that weren't matched

        df_1 = pd.concat([df_1, df_2]).drop_duplicates(key)

        # drop the matching name columns since this is a left join
        df_1 = df_1[df_1.columns.drop(list(df_1.filter(regex='_y')))]
        df_1 = df_1[key]
        df_1.reset_index(drop=True, inplace=True)

    return df_1, matching_dict


local_path = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(local_path, "common_words.json"))
words = json.load(f)
common_words = words['words']

"""

# Example code

first_df = pd.read_csv("data_1.csv")
second_df = pd.read_csv("data_2.csv")
third_df = pd.read_csv('data_3.csv')

df_list = [first_df, second_df, third_df]

new_df, matching_dict = golden_source_merge(df_list, key=['name'])

print(matching_dict)
# check the results
#print(new_df)
new_df.to_csv('output.csv', index=False)
"""