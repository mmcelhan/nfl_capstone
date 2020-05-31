import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import process
import json
import os

def format_match_string(string):
    """ function that converts to lower case and removes common words """
    string = string.lower().split()
    string = [word for word in string if word not in common_words]
    string = ' '.join(string)
    return string


def fuzzy_merge(df_1, df_2, key1, key2, threshold=80, limit=1):
    """
    df_1 is the left table to join
    df_2 is the right table to join
    key1 is the key column of the left table
    key2 is the key column of the right table
    threshold is how close the matches should be to return a match, based on Levenshtein distance
    limit is the amount of matches that will get returned, these are sorted high to low
    """

    # create null match columns
    df_1['match_key'] = ''
    df_2['match_key'] = ''

    # combines the list of column inputs into a single string for matching
    for value in key1:
        df_1['match_key'] = df_1['match_key'].map(str) + ' ' + df_1[value].map(str)

    for value in key2:
        df_2['match_key'] = df_2['match_key'].map(str) + ' ' + df_2[value].map(str)

    # applies lower case and removes common words like "college" and "the"
    df_1['match_key'] = df_1['match_key'].apply(format_match_string)
    df_2['match_key'] = df_2['match_key'].apply(format_match_string)

    # the match process-creates the match keys to a list, matches, then saves them in the match column
    s = df_2['match_key'].tolist()
    m = df_1['match_key'].apply(lambda x:
                                process.extract(x, s, limit=limit, scorer=fuzzywuzzy.fuzz.token_sort_ratio))
    df_1['match'] = m

    # drop the score value and only keep the match words
    m2 = df_1['match'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['match'] = m2

    # merge based on the matches, suffixes to drop the columns later
    df_1 = df_1.merge(df_2, left_on='match', right_on='match_key', suffixes=['', '_y'])

    # drop the matching name columns since this is a left join
    df_1 = df_1[df_1.columns.drop(list(df_1.filter(regex='_y')))]
    df_1 = df_1[df_1.columns.drop(['match_key', 'match'])]
    return df_1


local_path = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(local_path, "common_words.json"))
words = json.load(f)
#with open('common_words.json') as f:
    #words = json.load(f)
common_words = words['words']

# Example code
"""
first_df = pd.read_csv("data_1.csv")
second_df = pd.read_csv("data_2.csv")



new_df = fuzzy_merge(first_df, second_df, key1=['last_name', 'first_name', 'school'],
                     key2=['first_name', 'school', 'last_name'])

# check the results
print(new_df)
new_df.to_csv('output.csv', index=False)
"""