import pandas as pd

columns = ["first_name", "last_name", "position", "team","madden_rating"]
column_rename = {
    "Team": "team",
    "First Name": "first_name",
    "First": "first_name",
    "FIRST":"first_name",
    "Last": "last_name",
    "LAST": "last_name",
    "Last Name": "last_name",
    "Position": "position",
    "POSITION":"position",
    "OVR": "madden_rating",
    "Overall": "madden_rating",
    "OVERALL RATING": "madden_rating",
    "ovr rating": "madden_rating",
    "2016_madden_rating": 2016,
    "2017_madden_rating": 2017,
    "2018_madden_rating": 2018,
    "2019_madden_rating": 2019,
    "2020_madden_rating": 2020

}

sheets_dict = pd.read_excel('Madden 15 Player Ratings Entire League.xlsx', sheet_name=None)




full_table = pd.DataFrame()
for name, sheet in sheets_dict.items():
    sheet['team'] = name
    sheet = sheet.rename(columns=lambda x: x.split('\n')[-1])
    full_table = full_table.append(sheet)

full_table.reset_index(inplace=True, drop=True)

full_table.rename(columns=column_rename, inplace=True)
full_table = full_table[columns]

full_table.to_csv('madden_2015.csv', index=False)