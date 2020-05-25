import requests
import json
from operator import itemgetter


def get_teams():
    url = "https://api.collegefootballdata.com/teams"
    params = {"searchTerm":""}
    response = requests.get(url, params=params)
    dictionary = json.loads(response.content)
    result = list(map(lambda x: x['school'], dictionary))
    with open('schools.txt', 'w') as f:
        for item in result:
            f.write('%s\n' % item)

def get_player():
    url = "https://api.collegefootballdata.com/player/search"
    params = {"team": "Pittsburgh", "searchTerm": "a"}
    response = requests.get(url, params=params)
    print(response.content)


get_player()



#parameters = {"searchTerm": "a"}
#response = requests.get("https://api.collegefootballdata.com/player/search", params=parameters)

#response = requests.get("https://api.collegefootballdata.com/player/search?searchTerm=a")

#print(response.content)


#dictionary = json.loads(response.content)
#print(len(dictionary))