import copper
import pandas as pd
import requests
from bs4 import BeautifulSoup
copper.project.path = '../../'

url = 'http://espn.go.com/nba/teams'
r = requests.get(url)

soup = BeautifulSoup(r.text)
tables = soup.find_all('ul', class_='medium-logos')

teams = []
prefix_1 = []
prefix_2 = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        prefix_1.append(url.split('/')[-2])
        prefix_2.append(url.split('/')[-1])


dic = {'prefix_2': prefix_2, 'prefix_1': prefix_1}
teams = pd.DataFrame(dic, index=teams)
teams.index.name = 'name'
print(teams)
copper.save(teams, 'teams')

