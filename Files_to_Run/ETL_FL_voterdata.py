#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy import create_engine


# In[2]:


import psycopg2


# In[3]:


flvd_df = pd.read_csv("Resources/fl_voter_data_2022.csv")
#Check initial dimensionality
flvd_df.shape


# In[4]:


#Drop extranenous header rows created by an image at the top of the original excel.
flvd_df=flvd_df.drop([0,1,2,3,4,5,6])
#Recheck dimensionality
flvd_df.shape


# In[5]:


#Get column names for renaming:
for col in flvd_df.columns:
    print(col)


# In[6]:


#Rename columns
flvd_df=flvd_df.rename(columns={"FLORIDA DEPARTMENT OF STATE": "Party",
                       "Unnamed: 1": "County_Name",
                       "Unnamed: 2": "Native",
                       "Unnamed: 3": "Asian",
                       "Unnamed: 4": "Black",         
                       "Unnamed: 5": "Hispanic",
                       "Unnamed: 6": "White",
                       "Unnamed: 7": "Other",
                       "Unnamed: 8": "Multi",
                       "Unnamed: 9": "Unknown",
                       "Unnamed: 10": "Total_Voters"
                       })
#Check column rename
for col in flvd_df.columns:
    print(col)


# # Eliminating null values

# In[7]:


#Drop empty rows and check dimensionality
flvd_df.dropna(inplace=True)
flvd_df.shape


# In[8]:


#Confirm there are no null values
flvd_df.isnull().sum()


# # Convert Columns to Usable Datatypes

# In[9]:


#Check column datatypes
flvd_df.dtypes


# In[10]:


#The Race/Ethniciy columns contain numeric data that was created as text that includes commas.
#Remove commas
flvd_df[['Native','Asian','Black','Hispanic','White','Other','Multi','Unknown','Total_Voters']] = flvd_df[['Native','Asian','Black','Hispanic','White','Other','Multi','Unknown','Total_Voters']].replace(',','', regex=True)
#Change object columns to numeric
flvd_df[['Native','Asian','Black','Hispanic','White','Other','Multi','Unknown','Total_Voters']] = flvd_df[['Native','Asian','Black','Hispanic','White','Other','Multi','Unknown','Total_Voters']].apply(pd.to_numeric)


# In[11]:


#Confirm changes to column datatypes
flvd_df.dtypes


# # Inspect and Clean Object Datatype Columns

# ### Clean County Names

# In[12]:


#Inspect County Names
flvd_df['County_Name'].unique()


# In[13]:


#Drop rows in 'County Name' where the name equals 'Total'
#This is due to the orignial file contain Total rows for Partys.
#Previous row check was 816
totindx=flvd_df[flvd_df['County_Name']=='Total'].index
flvd_df.drop(totindx, inplace=True)


# In[14]:


#Count of unique party names
flvd_df['Party'].nunique()


# In[15]:


#816 - 12 is 804 which should match in a new dimensionality check
flvd_df.shape


# In[16]:


# Per https://www2.census.gov/geo/pdfs/reference/GARM/Ch4GARM.pdf , the number of Florida counties is 67
# This matches the return from nunique().
flvd_df['County_Name'].nunique()


# ### Clean Party Names

# In[17]:


#Examine strings in 'Party' column
flvd_df['Party'].unique()


# In[18]:


# Function to standarize 'Party' to "REP", "DEM", and "UNA"
# 'UNA' will be used to sum the counts of all other political parties, including "No affiliation",
# that are not Republican or Democrat.
def rename_party(party):
    #if party = Repub... then REP
    if party =='Republican Party of Florida                                        ':
        return "REP"
    #elif party = Democ... then DEM
    elif "Democrat" in party: 
        return "DEM"
    #else then UNA
    else:
        return "UNA"
#                                          apply(lambda x:rename_party(x))
#.copy() is used to avoid a SettingWithCopyWarning
flvd_df['Party'] = flvd_df['Party'].apply(lambda party:rename_party(party))
#lambda "says" we are taking the value from a function and then .apply to the column
#It's a way for a function to exist temporarily.


# In[19]:


#Confirm changes to data in 'Party' column
flvd_df['Party'].unique()


# In[20]:


#Add a column for state and populate the column with 'FL' in each row.
flvd_df['State']= 'FL'


# In[21]:


#Examine dataframe
flvd_df


# In[22]:


#Reset Dataframe index
flvd_df.reset_index(drop=True, inplace=True)


# In[23]:


#Add one to the index to conform with normal behavior of a sql table key.
flvd_df.index = flvd_df.index + 1


# In[24]:


#Confirm index starts at 1
flvd_df.head(5)


# In[25]:


#Confirm dataframe is working with some light analysis: County_Name
votes_by_county = flvd_df.groupby('County_Name')['Total_Voters'].sum().sort_values(ascending=False)
votes_by_county


# In[ ]:


#Confirm dataframe is working with some light analysis: Party
votes_by_county = flvd_df.groupby('Party')['Total_Voters'].sum().sort_values(ascending=False)
votes_by_county


# In[ ]:


#Connect to local database
protocol = 'postgresql'
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
database_name = 'state_voters_db'
rds_connection_string = f'{protocol}://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(rds_connection_string)


# In[ ]:


#Check tables
engine.table_names()


# In[ ]:


#Confirm inserted row count. Should = 804
flvd_df.to_sql(name='floridavoter', con=engine, if_exists='replace', index=False)


# In[ ]:


#Examine table data
pd.read_sql_query('select * from floridavoter', con=engine).head()

