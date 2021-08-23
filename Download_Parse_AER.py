#!/usr/bin/python3

from datetime import date, timedelta
import urllib.request
import pymongo
import urllib, json
import pandas as pd
import re
import numpy as np
import datetime
import os
from pathlib import Path

#ST1 Parser
def parser1(file):
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

        #For MongoDB Date needs to be converted back to Text
        datac['DATE'] = datac['DATE'].astype('str')
        datac['WEEK'] = datac['WEEK'].astype('str')
        datac['MONTH'] = datac['MONTH'].astype('str')
        datac['YEAR'] = datac['YEAR'].astype('str')

        #Merging with coordinates
        convcomp = pd.read_csv('/home/sidefxs/Documents/Exploration_App/ConvComp.csv')
        convcomp['ConvDF'] = convcomp['ConvDF'].astype('int64')
        dfm = pd.merge(datac, convcomp, how='left', left_on='ATS', right_on='ConvDF')

    return dfm

#Parser ST49
def parser49(file):

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

            #For MongoDB Date needs to be converted back to Text
            data1['DATE'] = data1['DATE'].astype('str')
            data1['WEEK'] = data1['WEEK'].astype('str')
            data1['MONTH'] = data1['MONTH'].astype('str')
            data1['YEAR'] = data1['YEAR'].astype('str')

            convcomp = pd.read_csv('/home/sidefxs/Documents/Exploration_App/ConvComp.csv')
            convcomp['ConvDF'] = convcomp['ConvDF'].astype('int64')
            dfm = pd.merge(data1, convcomp, how='left', left_on='ATS', right_on='ConvDF')
    except IndexError:
        columns = ['WELL ID', 'WELL NAME', 'LICENCE', 'CONTRACTOR BA ID', 'CONTRACTOR NAME', 'RIG NUMBER', 'ACTIVITY DATE', 'FIELD CENTRE', 'BA ID', 'LICENSEE', 'NEW PROJECTED TOTAL DEPTH', 'ACTIVITY TYPE', 'DATE', 'ATS', 'ConvDF', 'Lat', 'Long', 'WEEK', 'MONTH']

        dfm = pd.DataFrame(columns=columns)
        pass

    return dfm

#Get Yesterday's date
today = date.today() - timedelta(days=1)

#Connect to Database
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["AER"]

#Download ST1 Data
d1 = today.strftime("WELLS%m%d.TXT")
url1 = 'https://static.aer.ca/prd/data/well-lic/' + d1
urllib.request.urlretrieve(url1, '/home/sidefxs/Documents/Exploration_App/ST1/2021/'+d1)

#Parse file into Dataframe
data1 = parser1('/home/sidefxs/Documents/Exploration_App/ST1/2021/'+d1)

#Sent data to Database
colst1 = mydb["ST1"]

if data1.shape[0] == 1:
    x = colst1.insert_one(data1.to_dict('records'))

if data1.shape[0] >1:
    x = colst1.insert_many(data1.to_dict('records'))

if data1.empty:
    pass

#Download ST49 Data
d49 = today.strftime("SPUD%m%d.txt")
url49 = 'https://static.aer.ca/prd/data/wells/' + d49
urllib.request.urlretrieve(url49, '/home/sidefxs/Documents/Exploration_App/ST49/2021/'+d49)

#Parse file into Dataframe
data2 = parser49('/home/sidefxs/Documents/Exploration_App/ST49/2021/'+d49)

#Sent data to Database
colst49 = mydb["ST49"]

if data2.shape[0] == 1:
    x = colst49.insert_one(data2.to_dict('records'))

if data2.shape[0] >1:
    x = colst49.insert_many(data2.to_dict('records'))

if data2.empty:
    pass