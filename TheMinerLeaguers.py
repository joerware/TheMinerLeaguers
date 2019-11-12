
# coding: utf-8

# In[ ]:


# Import necessary modules/libraries.
import numpy as np
import pandas as pd
import pandas_profiling
from datetime import datetime
from scipy.stats import zscore
from ast import literal_eval


# In[ ]:


#Define dataframe from local CSV file
my_data = pd.read_csv('C:\\Users\\Joe\\Desktop\\tmdb_5000_movies.csv')


# In[ ]:


# Generate new columns for cleaned attribute values; old values are retained for provenance.
my_data['genres_clean'] = 0
my_data['keywords_clean'] = 0
my_data['production_companies_clean'] = 0
my_data['roi'] = 0


# In[ ]:


#Must set new column as object type to allow insertion of lists into dataframes, otherwise Type error will occur.
my_data['genres_clean'] = my_data['genres_clean'].astype(object)
my_data['keywords_clean'] = my_data['keywords_clean'].astype(object)
my_data['production_companies_clean'] = my_data['production_companies_clean'].astype(object)
my_data['budget'] = my_data['budget'].astype(float)
my_data['revenue'] = my_data['revenue'].astype(float)
my_data['roi'] = my_data['revenue'].astype(float)


# In[ ]:


# From genre attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "genres_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "genres"])]
    


# In[ ]:


# From keywords attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "keywords_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "keywords"])]
    


# In[ ]:


# From production_companies attribute, this extracts values from 'name' keys as a list.
for i in range(len(my_data)):
    my_data.at[i, "production_companies_clean"] = [d['name'] for d in literal_eval(my_data.loc[i, "production_companies"])]
    


# In[ ]:


# Mark to delete rows that contain value of 0 for budget.
for i in range(len(my_data)):
    if my_data.at[i, "budget"] == 0:
        my_data.at[i, "delete"] = 'Delete'


# In[ ]:


# Mark to delete rows that contain value of 0 for revenue.
for i in range(len(my_data)):
    if my_data.at[i, "revenue"] == 0:
        my_data.at[i, "delete"] = 'Delete'


# In[ ]:


# Remove homepage, language, overview attributes.
my_data.drop(columns=['original_language', 'homepage', 'overview'])


# In[ ]:


# Delete all rows marked for deletion.
my_data.drop(my_data[my_data["delete"] == 'Delete'].index, inplace = True)

# Dataframe must be re-indexed after dropping rows, or this will causes error in subsequent loop functions.
my_data.reset_index(drop=True, inplace=True)


# In[ ]:


#Calculate return on investment a generate a new column.
for i in range(len(my_data)):
    my_data.at[i, "roi"] = round((my_data.at[i, "revenue"] - my_data.at[i, "budget"]) /  my_data.at[i, "budget"], 2)


# In[ ]:


#Generate separate a day of the year and year column.
for i in range(len(my_data)):
    d = datetime.strptime(my_data.at[i, "release_date"], '%Y-%m-%d')
    my_data.at[i, "day_of_year"] = d.timetuple().tm_yday
    my_data.at[i, "year"] = d.year


# In[ ]:


#Create dummy variables; nominal/categorical variables must be converted for regression analysis.
my_data["genres_clean"].str.join('|').str.get_dummies()


# In[ ]:


# Outlier analysis using z-score; adds columns to compute z-score for budget/revenue.
my_data['revenue_zscore'] = my_data[['revenue']].apply(zscore)
my_data['budget_zscore'] = my_data[['budget']].apply(zscore)

#Scatter plot with data standardized via z-score
#my_data.plot.scatter(x='budget_zscore', y='revenue_zscore', c='DarkBlue')


# In[ ]:


""""
#Normalize data test
from sklearn import preprocessing
# Create x, where x the 'scores' column's values as floats
x = my_data[['budget_zscore']].values.astype(float)
y = my_data[['revenue_zscore']].values.astype(float)

# Create a minimum and maximum processor object
min_max_scaler = preprocessing.MinMaxScaler()

# Create an object to transform the data to fit minmax processor
x_scaled = min_max_scaler.fit_transform(x)
y_scaled = min_max_scaler.fit_transform(y)

# Run the normalizer on the dataframe
my_data['budget_normalized'] = pd.DataFrame(x_scaled)
my_data['revenue_normalized'] = pd.DataFrame(y_scaled)
my_data.plot.scatter(x='budget_normalized', y='revenue_normalized', c='DarkBlue')

"""


# In[ ]:


# Show first 25 rows of dataframe
my_data.head(25)


# In[ ]:


#Save dataframe as CSV somewhere
#my_data.to_csv('C:\\Users\\Joe\\Desktop\\my_data_scores.csv')

