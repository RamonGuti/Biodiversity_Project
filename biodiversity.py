#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Python Modules
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Loading Species Data Set
species = pd.read_csv('species_info.csv')
species.head()


# In[3]:


#Loading Observations Data Set
observations = pd.read_csv('observations.csv', encoding='utf-8')
observations.head()


# In[4]:


#Finding The different number of distinct species
print(f"number of species:{species.scientific_name.nunique()}")


# In[6]:


#Finding The Number of Unique Categories
print(f"nnumber of categories:{species.category.nunique()}")
print(f"categories:{species.category.unique()}")


# In[7]:


#Checking The Size of Each Category
species.groupby("category").size()


# In[8]:


#Seeing How Many and Names of Conservation Statuses
print(f"number of conservation statuses:{species.conservation_status.nunique()}")
print(f"unique conservation statuses:{species.conservation_status.unique()}")


# In[9]:


#Breakdown of Conservation Status
print(f"na values:{species.conservation_status.isna().sum()}")

print(species.groupby("conservation_status").size())


# In[10]:


#Seeing The Number of Parks and Names
print(f"number of parks:{observations.park_name.nunique()}")
print(f"unique parks:{observations.park_name.unique()}")


# In[11]:


#Total Number of Observations
print(f"number of observations:{observations.observations.sum()}")


# In[12]:


#Changing nan values in Species to No Intervention
species.fillna('No Intervention', inplace=True)
species.groupby("conservation_status").size()


# In[13]:


#Digging into the conservation Statues that are not No Intervention
conservationCategory = species[species.conservation_status != "No Intervention"]    .groupby(["conservation_status", "category"])['scientific_name']    .count()    .unstack()

conservationCategory


# In[14]:


#Plotting Conservation Statues to get a better look
ax = conservationCategory.plot(kind = 'bar', figsize=(8,6), 
                               stacked=True)
ax.set_xlabel("Conservation Status")
ax.set_ylabel("Number of Species");


# In[16]:


#Creating new column is_protected to see if certain species are more likely to be endangered
species['is_protected'] = species.conservation_status != 'No Intervention'


# In[17]:


#Seeing the breakdown of species and protection status
category_counts = species.groupby(['category', 'is_protected'])                        .scientific_name.nunique()                        .reset_index()                        .pivot(columns='is_protected',
                                      index='category',
                                      values='scientific_name')\
                        .reset_index()
category_counts.columns = ['category', 'not_protected', 'protected']

category_counts


# In[18]:


#Calculating the rate of protection for each category
category_counts['percent_protected'] = category_counts.protected /                                       (category_counts.protected + category_counts.not_protected) * 100

category_counts


# In[19]:


#Loading Scipy to see if different species have statistically significant differences in conservation status rates
from scipy.stats import chi2_contingency

contingency1 = [[30, 146],
              [75, 413]]
chi2_contingency(contingency1)


# In[20]:


#Testing the difference between Reptile and Mammal
contingency2 = [[30, 146],
               [5, 73]]
chi2_contingency(contingency2)


# In[21]:


#Checking the most prevalent animals in dataset
from itertools import chain
import string

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

common_Names = species[species.category == "Mammal"]    .common_names    .apply(remove_punctuations)    .str.split().tolist()

common_Names[:6]


# In[22]:


#Cleaning duplicate words in each row
cleanRows = []

for item in common_Names:
    item = list(dict.fromkeys(item))
    cleanRows.append(item)
    
cleanRows[:6]


# In[23]:


#Collapsing words into one list
res = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in cleanRows))
res[:6]


# In[24]:


#Counting the number of occurrences in each word
words_counted = []

for i in res:
    x = res.count(i)
    words_counted.append((i,x))

pd.DataFrame(set(words_counted), columns =['Word', 'Count']).sort_values("Count", ascending = False).head(10)


# In[25]:


#Checking which are names are referring to a species of bat
species['is_bat'] = species.common_names.str.contains(r"\bBat\b", regex = True)

species.head(10)


# In[26]:


#Looking at the data where is_bat is true
species[species.is_bat]


# In[27]:


#Merging results of bat species with observations
bat_observations = observations.merge(species[species.is_bat])
bat_observations


# In[28]:


#Seeing total number of bat observations at each national park
bat_observations.groupby('park_name').observations.sum().reset_index()


# In[29]:


#Breakdown of protected bats vs. non-protected bat sightings
obs_by_park = bat_observations.groupby(['park_name', 'is_protected']).observations.sum().reset_index()
obs_by_park


# In[30]:


#Plotting the observations
plt.figure(figsize=(16, 4))
sns.barplot(x=obs_by_park.park_name, y= obs_by_park.observations, hue=obs_by_park.is_protected)
plt.xlabel('National Parks')
plt.ylabel('Number of Observations')
plt.title('Observations of Bats per Week')
plt.show()


# Conclusions
# The project was able to make several data visualizations and inferences about the various species in four of the National Parks that comprised this data set.
# 
# This project was also able to answer some of the questions first posed in the beginning:
# 
# What is the distribution of conservation status for species?
#     The vast majority of species were not part of conservation.(5,633 vs 191)
# Are certain types of species more likely to be endangered?
#     Mammals and Birds had the highest percentage of being in protection.
# Are the differences between species and their conservation status significant?
#     While mammals and Birds did not have significant difference in 
#     conservation percentage, mammals and reptiles exhibited a 
#     statistically significant difference.
# Which animal is most prevalent and what is their distribution amongst parks?
#     the study found that bats occurred the most number of times and they were 
#     most likely to be found in Yellowstone National Park.
