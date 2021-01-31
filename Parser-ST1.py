#!/usr/bin/python3
# coding: utf-8

# In[1]:


import re
import pandas as pd
import numpy as np
import datetime


# In[2]:


def parser(file):
    #Initialize list
    lines = []
    dfm = []

    #Initializes the Dataframe in case the file is empty
    columns = ['WELL NAME', 'LICENCE NUMBER', 'MINERAL RIGHTS', 'GROUND ELEVATION', 'UID', 'SURFACE CO-ORDINATES', 'BOARD FIELD CENTRE', 'PROJECTED DEPTH', 'DRILLING OPERATION', 'WELL PURPOSE', 'WELL TYPE', 'SUBSTANCE', 'DATE', 'LAHEE CLASSIFICATION', 'FIELD', 'TERMINATING ZONE', 'LICENSEE', 'SURFACE LOCATION', 'ATS', 'Lat', 'Long', 'WEEK', 'MONTH']

    dfm = pd.DataFrame(columns=columns)

    #Open File
    with open(file, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    #Extract Date
    Date = (re.split('[\s]{4,}', lines[6].strip()))
    Date = Date[0]
    Date = Date.replace('DATE: ', '')
    Date

    #Extract indices to cut list
    indices = [i for i, s in enumerate(lines) if '------' in s]

    #Create list with only well licenses
    df1 = lines[(indices[1]+2):(indices[2]-1)]

    #Create indexes to slice
    length = len(df1)
    times = length//5
    index3 = np.arange(2, length, 6).tolist()
    index4 = np.arange(4, length, 6).tolist()
    indexr = np.arange(0, length, 1).tolist()
    index = index3 + index4
    indexr = np.delete(indexr, index)

    #Create 3 lists to bypass issue with 3rd line and 5th line  
    dfline3 = []
    dfline4 = []
    dfliner = []
    for line in index3:
        dfline3.append(df1[line])

    for line in index4:
        dfline4.append(df1[line])    

    for line in indexr:
        dfliner.append(df1[line])

    df2 = []
    for line in dfliner:
        df2.append(line[0:40])
        df2.append(line[41:50])
        df2.append(line[51:71])
        df2.append(line[72:104])

    df3 = []
    for line in dfline3:
        df3.append(line[0:40])
        df3.append(line[41:71])
        df3.append(line[72:104])

    dfl = []
    for line in dfline4:
        dfl.append(line[0:60])
        dfl.append(line[72:104])    

    #Create a list without all spaces
    df4 = []
    for line in df2:
        df4.extend(re.split('[\s]{5,}', line.strip()))

    #Create list without blank items
    df4 = [x for x in df4 if x != '']

    #Create lists for all 17 elements in the table
    df4 = [df4[x:x+12] for x in range(0, len(df4), 12)]

    #Create list for 3rd line
    dfr1 = []
    for line in df3:
        dfr1.extend(re.split('[\s]{4,}', line.strip()))

    #Create lists for all 17 elements in the table
    dfr1 = [dfr1[x:x+3] for x in range(0, len(dfr1), 3)]

    #Create list for 5th line
    dfr2 = []
    for line in dfl:
        dfr2.extend(re.split('[\s]{4,}', line.strip()))

    #Create lists for all 17 elements in the table
    dfr2 = [dfr2[x:x+2] for x in range(0, len(dfr2), 2)]

    #create a dataframe out of the list
    if df4 != []:
        data1 = pd.DataFrame(df4)
        data1.set_axis(['WELL NAME', 'LICENCE NUMBER', 'MINERAL RIGHTS', 'GROUND ELEVATION', 'UID', 'SURFACE CO-ORDINATES', 'BOARD FIELD CENTRE', 'PROJECTED DEPTH', 'DRILLING OPERATION', 'WELL PURPOSE', 'WELL TYPE', 'SUBSTANCE'], axis = 1, inplace=True)
        data1['DATE'] = Date

        data2 = pd.DataFrame(dfr1)
        data2.set_axis(['LAHEE CLASSIFICATION', 'FIELD', 'TERMINATING ZONE'],axis = 1, inplace=True)

        data3 = pd.DataFrame(dfr2)
        data3.set_axis(['LICENSEE', 'SURFACE LOCATION'],axis = 1, inplace=True)

        datac = pd.concat([data1, data2, data3], axis=1, sort=False)
        
        #Conversion of Surface Location to numbers only in order to search ATS values and match them to latitude and longitude
        datac['ATS'] = datac['SURFACE LOCATION'].str.replace(r'[^0-9]+', '', regex = True)
        datac['ATS'] = datac['ATS'].str[-8:]
        datac['PROJECTED DEPTH'] = datac['PROJECTED DEPTH'].str[:-1]
        
        #Conversion to integers
        datac['ATS'] = datac['ATS'].astype('int64')
        datac['PROJECTED DEPTH'] = datac['PROJECTED DEPTH'].astype('float64')

        #Separating Date in Weeks, Month, Year
        datac['DATE'] = datac['DATE'].astype('datetime64')
        datac['WEEK'] = datac['DATE'].dt.isocalendar().week
        datac['MONTH'] = datac['DATE'].dt.month
        datac['YEAR'] = datac['DATE'].dt.year

        #Merging with coordinates
        convcomp = pd.read_csv('/home/sidefxs/Documents/Exploration_App/ConvComp.csv')
        convcomp['ConvDF'] = convcomp['ConvDF'].astype('int64')
        dfm = pd.merge(datac, convcomp, how='left', left_on='ATS', right_on='ConvDF')

    return dfm


# In[3]:


import os

from pathlib import Path

directory_in_str = "/home/sidefxs/Documents/Exploration_App/ST1/2021"

directory = os.fsencode(directory_in_str) 

columns = ['WELL NAME', 'LICENCE NUMBER', 'MINERAL RIGHTS', 'GROUND ELEVATION', 'UID', 'SURFACE CO-ORDINATES', 'BOARD FIELD CENTRE', 'PROJECTED DEPTH', 'DRILLING OPERATION', 'WELL PURPOSE', 'WELL TYPE', 'SUBSTANCE', 'DATE', 'LAHEE CLASSIFICATION', 'FIELD', 'TERMINATING ZONE', 'LICENSEE', 'SURFACE LOCATION', 'ATS', 'Lat', 'Long', 'WEEK', 'MONTH']

df = pd.DataFrame(columns=columns)

ext = ['.txt','.TXT']

for file in os.listdir(directory): 
    filename = os.fsdecode(file) 
    if filename.endswith(tuple(ext)):
        #print(filename)
        data = parser(os.path.join(directory_in_str, filename))
        data.to_csv("/home/sidefxs/Documents/Exploration_App/ST1/CSV/2021" + filename + ".csv", index = False)
        #df = df.append(data, ignore_index=True, sort=False)
        continue 
    else: 
        continue


# In[ ]:




