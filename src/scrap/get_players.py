import copper
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
copper.project.path = '../..'

games = copper.read_csv('games.csv').set_index('id')
BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'

request = requests.get(BASE_URL.format(games.index[0]))

table = BeautifulSoup(request.text).find('table', class_='mod-data')
heads = table.find_all('thead')
headers = heads[0].find_all('tr')[1].find_all('th')[1:]
headers = [th.text for th in headers]
columns = ['id', 'team', 'player'] + headers

players = pd.DataFrame(columns=columns)

def get_players(players, team_name):
    array = np.zeros((len(players), len(headers)+1), dtype=object)
    array[:] = np.nan
    for i, player in enumerate(players):
        cols = player.find_all('td')
        array[i, 0] = cols[0].text.split(',')[0]
        for j in range(1, len(headers) + 1):
            if not cols[1].text.startswith('DNP'):
                array[i, j] = cols[j].text
    
    frame = pd.DataFrame(columns=columns)
    for x in array:
        line = np.concatenate(([index, team_name], x)).reshape(1,len(columns))
        new = pd.DataFrame(line, columns=frame.columns)
        frame = frame.append(new)
    return frame

for index, row in games[:3].iterrows():
# for index, row in games.iterrows():
    print(index)
    request = requests.get(BASE_URL.format(index))
    table = BeautifulSoup(request.text).find('table', class_='mod-data')
    heads = table.find_all('thead')
    bodies = table.find_all('tbody')

    team_1 = heads[0].th.text
    team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
    team_1_players = get_players(team_1_players, team_1)
    players = players.append(team_1_players)
    
    team_2 = heads[3].th.text
    team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
    team_2_players = get_players(team_2_players, team_2)
    players = players.append(team_2_players)

players = players.set_index('id')
print(players)
copper.save(players, 'players')