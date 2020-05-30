import requests
import json
import pandas as pd
import os

def load_schools(length):
    school_list = []
    with open('schools.txt', 'r') as f:
        for row in f:
            school_list.append(row.rstrip("\n"))
    school_list = school_list[0:length]
    return school_list


def load_positions():
    position_list = []
    with open('positions.txt', 'r') as f:
        for row in f:
            position_list.append(row.rstrip("\n"))
    return position_list


def get_schools():
    url = "https://api.collegefootballdata.com/conferences"
    params = {"searchTerm": ""}
    response = requests.get(url, params=params)
    c = json.loads(response.content)
    for conference in c:
        print(conference)
        params = {"conference": conference['name']}
        response = requests.get(url, params=params)
        teams = json.loads(response)
        for t in teams:
            print(t)
    #result = list(map(lambda x: x['school'], dictionary))
    #with open('schools.txt', 'w') as f:
    #    for item in result:
    #        f.write('%s\n' % item)


def write_list_to_file(l, file_name):
    with open(file_name, 'w') as f:
        for item in l:
            f.write('%s\n' % item)


def get_positions():
    player_dict = {}
    url = "https://api.collegefootballdata.com/player/search"
    teams = ["Georgia", "Alabama", "Florida", "Pittsburgh", "Baylor", "Army", "Arizona", "BYU", "Iowa Wesleyan",
             "Ithaca"]  # has to be a wide enough net
    # a through c in alphabet
    letters = [chr(i) for i in range(ord('a'), ord('c') + 1)]

    positions = set()
    for team in teams:
        for letter in letters:
            params = {"team": team, "searchTerm": letter}
            response = requests.get(url, params=params)
            dictionary = json.loads(response.content)
            position_list = set(list(map(lambda x: x['position'], dictionary)))
            positions = positions.union(position_list)

    positions = list(positions)

    with open('positions.txt', 'w') as f:
        for item in positions:
            f.write('%s\n' % item)


def get_players(schools, years):

    if os.path.exists("raw_players.csv"):
        player_df = pd.read_csv("raw_players.csv")
    else:
        column_names = ["id", "first_name", "last_name", "weight", "height", "jersey", "year",
                        "position", "home_city", "home_state", "home_country", "school"]
        player_df = pd.DataFrame(columns=column_names)

    url = "https://api.collegefootballdata.com/roster"
    for school in schools:
        for year in years:
            params = {"team": school, "year": year}
            response = requests.get(url, params=params)
            temp_dict = json.loads(response.content)
            for value in temp_dict:
                value['school'] = school
                value['year'] = year
                df = pd.DataFrame([value], columns=value.keys())
                player_df = player_df.append(df, ignore_index=True)

    columns_order = ["id", "first_name", "last_name", "school", "year", "weight", "height", "jersey",
                     "position", "home_city", "home_state", "home_country"]

    player_df = player_df[columns_order]
    player_df = player_df[player_df["id"].notna()]
    player_df['id'] = player_df['id'].astype(int)
    player_df = player_df.where(player_df['id'] > 0)  # remove negative values (teams)
    player_df = player_df.sort_values('id', ascending=False)
    player_df.drop_duplicates(subset="id", keep="last", inplace=True)
    player_df = player_df[player_df["id"].notna()]
    player_df = player_df[player_df["last_name"].notna()]
    player_df['id'] = player_df['id'].astype(int)
    player_df['year'] = player_df['year'].astype(int)
    player_df.to_csv("raw_players.csv", index=False)

    return None  # end function


years = list(range(2010, 2012, 1))
print(years)
get_players(load_schools(738), years)