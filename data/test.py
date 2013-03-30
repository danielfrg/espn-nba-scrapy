import requests
from bs4 import BeautifulSoup


url = 'http://espn.go.com/nba/schedule'
r = requests.get(url)

soup = BeautifulSoup(r.text)
# tables = [table for table in soup.findAll('table')]
print(soup.findAll('table'))


