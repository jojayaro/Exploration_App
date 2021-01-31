#!/usr/bin/python3

from datetime import date, timedelta
import pandas as pd
import urllib.request

today = date.today() - timedelta(days=1)

d1 = today.strftime("WELLS%m%d.TXT")
url1 = 'https://static.aer.ca/prd/data/well-lic/' + d1
urllib.request.urlretrieve(url1, '/home/sidefxs/Documents/Exploration_App/ST1/2021/'+d1)

d49 = today.strftime("SPUD%m%d.txt")
url49 = 'https://static.aer.ca/prd/data/wells/' + d49
urllib.request.urlretrieve(url49, '/home/sidefxs/Documents/Exploration_App/ST49/2021/'+d49)