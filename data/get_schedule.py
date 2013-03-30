import copper
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
copper.project.path = '..'

year = 2013
teams = copper.read_csv('teams.csv')

team_1 = []
team_2 = []
dates = []
home = []
won = []
team_1_score = []
team_2_score = []
match_id = []
# for index, row in teams[:1].iterrows():
for index, row in teams.iterrows():
    _team, url = row['team'], row['url'] 
    url = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'
    r = requests.get(url.format(row['prefix_1'], year, row['prefix_2']))
    table = BeautifulSoup(r.text).table
    for row in table.find_all('tr')[1:]: # Remove header
        columns = row.find_all('td')
        try: 
            team_1.append(_team)
            d = datetime.strptime(columns[0].text, '%a, %b %d')
            dates.append(date(year, d.month, d.day))
            _home = True if columns[1].li.text == 'vs' else False
            home.append(_home)
            team_2.append(columns[1].find_all('a')[1].text)
            _won = True if columns[2].span.text == 'W' else False
            won.append(_won)
            _score = columns[2].a.text.split(' ')[0].split('-')
            match_id.append(columns[2].a['href'].split('?id=')[1])
            team_1_score.append(_score[0] if _home else _score[1])
            team_2_score.append(_score[1] if _home else _score[0])
        except Exception as e:
            pass # Not all columns row are a match
            # print(e)

dic = {'id': match_id, 'date': dates, 'team_1': team_1, 'team_2': team_2, 
        'home': home, 'team_1_score': team_1_score, 
        'team_2_score': team_2_score, 'won': won}
# Fix dtypes
for key in ['id', 'team_1_score', 'team_2_score']:
    dic[key] = np.array(dic[key], dtype=int)
# Fix not yet played matchs
lens = [len(dic[key]) for key in dic]
dic = {key: dic[key][:min(lens)] for key in dic}

matches = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')
print(matches)
copper.save(matches, 'matches')

