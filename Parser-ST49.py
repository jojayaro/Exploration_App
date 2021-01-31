#!/usr/bin/python3
# coding: utf-8

# In[4]:


import re
import pandas as pd
import numpy as np
import datetime


# In[5]:


def parser(file):

    lines = []
    dfm = []

    with open(file, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    #Extract Date
    Date = (re.split('[\s]{4,}', lines[1].strip()))
    Date = Date[0]
    Date = Date.replace('Run Date: ', '')

    #Extract indices to cut list
    indices = [i for i, s in enumerate(lines) if '------' in s]
    indicest = [i for i, s in enumerate(lines) if 'TOTAL  -' in s]

    #Create list with only well licenses
    try:
        df1 = lines[(indices[1]+1):(indicest[0]-1)]
        
        dfsplit = lines[indices[1]]

        def find(s, ch):
            return [i for i, ltr in enumerate(s) if ltr == ch]

        cut = find(dfsplit,' ')

        df2 = []
        for line in df1:
            df2.append(line[0:cut[0]])
            df2.append(line[cut[0]:cut[1]])
            df2.append(line[cut[1]:cut[2]])
            df2.append(line[cut[2]:cut[3]])
            df2.append(line[cut[3]:cut[4]])
            df2.append(line[cut[4]:cut[5]])
            df2.append(line[cut[5]:cut[6]])
            df2.append(line[cut[6]:cut[7]])
            df2.append(line[cut[7]:cut[8]])
            df2.append(line[cut[8]:cut[9]])
            df2.append(line[cut[9]:cut[10]])
            df2.append(line[cut[10]:])

        #Create a list without all spaces
        df3 = []
        for line in df2:
            df3.extend(re.split('[\s]{5,}', line.strip()))

        df3 = [df3[x:x+12] for x in range(0, len(df3), 12)]

        #create a dataframe out of the list
        if df3 != []:
            data1 = pd.DataFrame(df3)
            data1.set_axis(['WELL ID', 'WELL NAME', 'LICENCE', 'CONTRACTOR BA ID', 'CONTRACTOR NAME', 'RIG NUMBER', 'ACTIVITY DATE', 'FIELD CENTRE', 'BA ID', 'LICENSEE', 'NEW PROJECTED TOTAL DEPTH', 'ACTIVITY TYPE'], axis = 1, inplace=True)
            data1['DATE'] = Date

            data1['ATS'] = data1['WELL ID'].str.replace(r'[^0-9]+', '', regex = True)
            data1['ATS'] = data1['ATS'].str[-9:-1]
            data1['ATS'] = data1['ATS'].astype('int64')
            
            data1['DATE'] = data1['DATE'].astype('datetime64')
            data1['WEEK'] = data1['DATE'].dt.isocalendar().week
            data1['MONTH'] = data1['DATE'].dt.month
            data1['YEAR'] = data1['DATE'].dt.year

            convcomp = pd.read_csv('/home/sidefxs/Documents/Exploration_App/ConvComp.csv')
            convcomp['ConvDF'] = convcomp['ConvDF'].astype('int64')
            dfm = pd.merge(data1, convcomp, how='left', left_on='ATS', right_on='ConvDF')
    except IndexError:
        columns = ['WELL ID', 'WELL NAME', 'LICENCE', 'CONTRACTOR BA ID', 'CONTRACTOR NAME', 'RIG NUMBER', 'ACTIVITY DATE', 'FIELD CENTRE', 'BA ID', 'LICENSEE', 'NEW PROJECTED TOTAL DEPTH', 'ACTIVITY TYPE', 'DATE', 'ATS', 'ConvDF', 'Lat', 'Long', 'WEEK', 'MONTH']

        dfm = pd.DataFrame(columns=columns)
        pass

    return dfm


# In[6]:


import os

from pathlib import Path

directory_in_str = "/home/sidefxs/Documents/Exploration_App/ST49/2021"

directory = os.fsencode(directory_in_str) 

columns = ['WELL ID', 'WELL NAME', 'LICENCE', 'CONTRACTOR BA ID', 'CONTRACTOR NAME', 'RIG NUMBER', 'ACTIVITY DATE', 'FIELD CENTRE', 'BA ID', 'LICENSEE', 'NEW PROJECTED TOTAL DEPTH', 'ACTIVITY TYPE', 'DATE', 'ATS', 'ConvDF', 'Lat', 'Long', 'WEEK', 'MONTH']

df = pd.DataFrame(columns=columns)

ext = ['.txt','.TXT']

for file in os.listdir(directory): 
    filename = os.fsdecode(file) 
    if filename.endswith(tuple(ext)):
        #print(filename)
        data = parser(os.path.join(directory_in_str, filename))
        data.to_csv("/home/sidefxs/Documents/Exploration_App/ST49/CSV/2021" + filename + ".csv", index = False)
        #df = df.append(data, ignore_index=True, sort=False)
        continue 
    else: 
        continue


# In[ ]:




