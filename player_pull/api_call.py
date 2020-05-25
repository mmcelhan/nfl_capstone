import requests
import json
from operator import itemgetter

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
    url = "https://api.collegefootballdata.com/teams"
    params = {"searchTerm":""}
    response = requests.get(url, params=params)
    dictionary = json.loads(response.content)
    result = list(map(lambda x: x['school'], dictionary))
    with open('schools.txt', 'w') as f:
        for item in result:
            f.write('%s\n' % item)


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

def get_players(schools, positions, letters):
    player_list = []
    temp_dict = {}
    url = "https://api.collegefootballdata.com/player/search"
    counter = 0
    for school in schools:
        for letter in letters:
            for position in positions:
                params = {"team": school, "position": position, "searchTerm": letter}
                response = requests.get(url, params=params)
                temp_dict = json.loads(response.content)
                for value in temp_dict:
                    player_list.append(value)

                counter += 1
                print(len(player_list))
    print(player_list)
    player_list = [dict(t) for t in {tuple(d.items()) for d in player_list}]
    print(player_list)
    print(len(player_list))

    write_list_to_file(player_list, "players.txt")

    return None  # end function


letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
letters.remove("q")
letters.remove("z")
letters.remove("x")
letters.remove("v")

#get_players(load_schools(738), load_positions(), letters)
get_players(['Pittsburgh'], load_positions(), letters)


"""
params = {"team": team, "searchTerm": letter}
response = requests.get(url, params=params)
print(response.content)
dictionary = json.loads(response.content)
position_list = set(list(map(lambda x: x['position'], dictionary)))
positions = positions.union(position_list)
"""
