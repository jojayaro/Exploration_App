#!/usr/bin/python3
# coding: utf-8

# In[1]:


import os
import glob
import pandas as pd


# In[2]:


os.chdir("/home/sidefxs/Documents/Exploration_App/ST1/CSV")


# In[3]:


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


# In[4]:


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, encoding= 'unicode_escape') for f in all_filenames ])
#export to csv
combined_csv.to_csv("/home/sidefxs/Documents/Exploration_Data_Container/ST1-2021.csv", index=False, encoding='utf-8-sig')


# In[ ]:




