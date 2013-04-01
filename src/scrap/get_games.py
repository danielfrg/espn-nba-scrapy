import copper
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
copper.project.path = '../../'

year = 2013
teams = copper.read_csv('teams.csv')
BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'
BASE_GAME_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'

game_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
for index, row in teams.iterrows():
# for index, row in teams[:1].iterrows():
    _team = row['name']
    print(_team)
    r = requests.get(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
    table = BeautifulSoup(r.text).table
    for row in table.find_all('tr')[1:]:
    # for row in table.find_all('tr')[1:3]:
        columns = row.find_all('td')
        try: 
            _id = columns[2].a['href'].split('?id=')[1]
            _home = True if columns[1].li.text == 'vs' else False
            _other_team = columns[1].find_all('a')[1].text
            _score = columns[2].a.text.split(' ')[0].split('-')
            _won = True if columns[2].span.text == 'W' else False

            game_id.append(_id)
            home_team.append(_team if _home else _other_team)
            visit_team.append(_team if not _home else _other_team)
            d = datetime.strptime(columns[0].text, '%a, %b %d')
            dates.append(date(year, d.month, d.day))
            
            if _home:
                if _won:
                    home_team_score.append(_score[0])
                    visit_team_score.append(_score[1])
                else:
                    home_team_score.append(_score[1])
                    visit_team_score.append(_score[0])
            else:
                if _won:
                    home_team_score.append(_score[1])
                    visit_team_score.append(_score[0])
                else:
                    home_team_score.append(_score[0])
                    visit_team_score.append(_score[1])

            # Extra stats
            # r = requests.get(BASE_GAME_URL.format(_id))
            # table = BeautifulSoup(r.text).find('table', class_='mod-data')
            # heads = table.find_all('thead')
            # bodies = table.find_all('tbody')
            # # print(heads)
            # headers = heads[2].tr.find_all('th')[2:]
            # headers = [th.text for th in headers]
            # headers[3] = headers[3].split('\n')[0]
            # del headers[-2]
            # visit_stats = bodies[2].tr.find_all('td')[1:]
            # visit_stats = [td.text for td in visit_stats]
            # del visit_stats[-2]
            # print(headers)
            # print(visit_stats)

        except Exception as e:
            pass # Not all columns row are a game, is OK
            # print(e)

dic = {'id': game_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team, 
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}
        
games = pd.DataFrame(dic).drop_duplicates(cols='id').set_index('id')
print(games)
copper.save(games, 'games')