import copper
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
copper.project.path = '..'

year = 2013
matches = copper.read_csv('teams.csv')

