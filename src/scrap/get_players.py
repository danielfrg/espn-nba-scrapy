import copper
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
copper.project.path = '../..'

year = 2013
matches = copper.read_csv('matches.csv').set_index('id')
# print(matches)

URL = 'http://espn.go.com/nba/boxscore?gameId={0}'

for index, row in matches[:1].iterrows():
    print(index)

