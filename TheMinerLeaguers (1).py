
# coding: utf-8

# In[2]:


# Import necessary modules/libraries.
import numpy
import pandas as pd
import pandas_profiling
from ast import literal_eval


# In[3]:


#Define dataframe from local CSV file
my_data = pd.read_csv('C:\\Users\\Joe\\Desktop\\tmdb_5000_movies.csv')


# In[73]:


# Generate new columns for cleaned attribute values to track provenance.
my_data['genres_clean'] = 0
my_data['keywords_clean'] = 0
my_data['production_companies_clean'] = 0


# In[75]:


#Must set new column as object type to allow insertion of lists into dataframes, otherwise Type error will occur.
my_data['genres_clean'] = my_data['genres_clean'].astype(object)
my_data['keywords_clean'] = my_data['keywords_clean'].astype(object)
my_data['production_companies_clean'] = my_data['production_companies_clean'].astype(object)


# In[76]:


# From genre attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "genres_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "genres"])]
    


# In[77]:


# From keywords attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "keywords_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "keywords"])]
    


# In[78]:


# From production_companies attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "production_companies_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "production_companies"])]
    


# In[60]:


# Mark rows that contain value of 0 for budget.
for i in range(len(my_data)):
    if my_data.at[i, "budget"] == 0:
        my_data.at[i, "delete"] = 'Delete'


# In[61]:


# Mark rows that contain value of 0 for revenue.
for i in range(len(my_data)):
    if my_data.at[i, "revenue"] == 0:
        my_data.at[i, "delete"] = 'Delete'


# In[65]:


# Delete all rows marked for deletion.
my_data.drop(my_data[my_data["delete"] == 'Delete'].index, inplace = True)


# In[1]:


my_data

