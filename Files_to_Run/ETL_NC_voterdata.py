#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Python SQL toolkit and Object Relational Mapper
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine


# In[2]:


#Reading in the original .txt file as csv

nc_voter_df = pd.read_csv('NC_Resources/history_stats_20220726.txt', delimiter='\t')
#viewing the information
nc_voter_df.info()


# In[3]:


#Beginning the cleaning process, dropping any NaN values
nc_voter_df.dropna()


# In[4]:


#Specifying which columns to keep and eliminating ones irrelevant to our process:

nc_voter_df = nc_voter_df[['county_desc', 'party_cd', 'race_code','ethnic_code','total_voters','election_date']].copy()
nc_voter_df.head()


# In[5]:


#Creating a state column and filling it with the appropriate two character shorthand:
#This column's relevancy will be evident when comparing its information with the other states to be loaded in the SQL database.
nc_voter_df['State'] ='NC'


# In[6]:


#Reviewing the column names before renaming them
nc_voter_df.columns


# In[7]:


#Renaming the headings for increased standardization among the various datasets to be loaded into the SQL database:

new_cols = ['State','county_desc', 'party_cd', 'race_code', 'ethnic_code', 'total_voters',
       'election_date']
nc_voter_df = nc_voter_df[new_cols]


# In[8]:


#Changing the names of the columns to ensure consistent naming practice across all datasets:

nc_voter_df.rename(columns = {'county_desc':'County_Name', 'party_cd':'Party',
                            'race_code':'Race_Code', 'ethnic_code': 'Ethnic_Code',
                            'total_voters':'Total_Voters',
                            'election_date':'Election_Date'}, inplace=True)


# In[9]:


#checking the dtypes for quality control
nc_voter_df.dtypes


# In[10]:


# Change 'date' column into a 'datetime' datatype, eliminating the 'time' field as it is not used
nc_voter_df['Election_Date'] = pd.to_datetime(nc_voter_df['Election_Date'], errors='coerce')


# In[11]:


#checking the dtypes to ensure changes were kept

nc_voter_df.dtypes


# In[12]:


#Changing party values to ensure consistent naming practice across all datasets:

nc_voter_df['Party'] = nc_voter_df['Party'].replace(['UNA','LIB'], 'UNA')
nc_voter_df['Party'].unique()


# In[13]:


#Running some initial inquiries and visualization strategy to understand the dataset and check for possible red flags

nc_voter_df['County_Name'].unique()


# In[14]:


voter_turnout = nc_voter_df.groupby('County_Name')['Total_Voters'].sum().sort_values(ascending=False)
voter_turnout


# In[15]:


x = [1,2,3,4,5,6,7,8,9,10,11]
y = voter_turnout
labels = ['MECKLENBURG', 'NASH', 'WAKE', 'CATAWBA', 'CHATHAM', 'CRAVEN',
       'CUMBERLAND', 'FRANKLIN', 'GRAHAM', 'IREDELL', 'LEE']
plt.subplots_adjust(bottom=0.15)

plt.subplot(122)
plt.plot(x, y, marker='D')
plt.xticks(x, labels, rotation='vertical')
plt.margins(0.2)
plt.title("Vertical tick label")
plt.gcf().set_size_inches(10,8)
plt.grid(linewidth = 0.25)

plt.show()


# In[16]:


#Path for final dataframe destination:
protocol = 'postgresql'
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
database_name = 'state_voters_db'
rds_connection_string = f'{protocol}://{username}:{password}@{host}:{port}/{database_name}'
engine = create_engine(rds_connection_string)


# In[17]:


#using pandas to load converted dataframe into database
nc_voter_df.to_sql(name='nc_voter_data', con=engine, if_exists='replace', index=False)


# In[18]:


#storing the dataframe in a csv for review as/if needed
nc_voter_df.to_csv('NC_Resources/cleaned_nc_voterdata.csv')


# In[19]:


#Running a query to make sure our process is complete:
pd.read_sql_query('select * from nc_voter_data', con=engine).head()


# In[ ]:




