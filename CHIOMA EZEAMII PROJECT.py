#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random


# # LOADING DATA SET
# 

# In[15]:


df=pd.read_csv(r"C:\Users\EZEAMII CHIOMA\Downloads\capstone - capstone.csv")


# # DATA CLEANING

# In[17]:


df


# In[18]:


df.drop_duplicates


# In[19]:


df=df.drop(columns ="title")


# # CLEANING DATE COLUMN AND YEAR EXTRACTION
# 

# In[20]:


date_formats = ["(%m/%d/%Y)", "%m/%d/%Y", "%m/%d/%Y", "%m/%d/%Y"]


# In[21]:


df['date added'] = df['date added'].str.replace(r"\(|\)", "", regex=True)


# In[22]:


for date_format in date_formats:
    df['parsed_date'] = pd.to_datetime(df['date added'], format=date_format, errors='coerce')


# In[23]:


df['year_added'] = df['parsed_date'].dt.year


# In[28]:


# number of days from release to today
from datetime import datetime
today = datetime.today()
df['date added'] = pd.to_datetime(df['date added'])
df['date added'] = (today - df['date added']).dt.days


# # CLEANING DIRECTORS,MOVIE TYPE AND COUNTRY COLUMN 

# In[ ]:


#cleaning directors column
df["director"]=df["director"].str.strip()
#cleaning Country column
df["Country"]=df["Country"].str.strip()
#cleaning Type column
df["Type"]=df["Type"].str.strip()


# In[216]:


df['Country'] = df['Country'].str.title()


# In[217]:


df['director'] = df['director'].str.title()


# In[218]:


df['Type'] = df['Type'].str.title()


# In[220]:


country_mapping = {
    'us': 'united states',
    'ca': 'Canada',
    'uk': 'United Kingdom',
    'jp': 'Japan',
    'pk': 'Pakistan',
    'united state': 'united states',
    'nited states': 'united states',  # Explicitly include 'nited states'
    'uae': 'United Arab Emirates',
}

df['Country'] = df['Country'].replace(country_mapping)


# In[221]:


print(df['Country'].unique())


# In[215]:


df['Country'] = df['Country'].replace(country_mapping)


# In[202]:


df['Country'] = df['Country'].replace('nited State')


# In[223]:


corrections = {
    'Mvie': 'Movie',
    'Tv': 'TV Show',
    'Tvs': 'TV Show',
    'Mvi': 'Movie',
    'Mv': 'Movie',
    'TVS': 'TV Show',
    'tv': 'TV Show',
    'm': 'Movie',
    'MvE': 'Movie',
    'M': 'Movie',
    'Mve': 'Movie'
}

df['Type'] = df['Type'].replace(corrections)


# In[169]:


country_mapping2 = {
    'UEA': 'United Arab Emirates',
    'ITL': 'Italy',
    'ID': 'India',
    'HK': 'Hong Kong'
    
}


# In[170]:


df['Country'] = df['Country'].replace(country_mapping2)


# In[171]:


df['Country'] = df['Country'].replace('thailan', 'Thailand')


# 
# # SPLITTING LISTED_IN COLUMN 

# In[55]:


df = df.join(df['listed_in'].str.split(', ', expand=True).add_prefix('genre_'))
df = df.drop(columns=['listed_in'])


# In[84]:


df


# # RANDOM RATING FUNCTION

# In[232]:


# Generate random ratings for each movie
min_rating = 1.0  # Minimum rating
max_rating = 5.0  # Maximum rating
num_decimals = 2  # Number of decimal places



# # SPLIT DURATION FUNCTION

# In[233]:


def split_duration(df):
    df['tv_series_duration'] = df['duration'][df['type'] == 'TV Show']
    df['duration'] = df['duration'].apply(lambda x: x if not x.isdigit() else None)
    split_duration(df)
    df = df.join(df['duration'].str.split(' ', expand=True).add_prefix('duration_'))



# # TV SERIES DURATION IN SEPAREATE COLUMN 

# In[234]:


def separate_tv_series_duration(df):
    df['tv_series_duration'] = ""
    tv_series_rows = df[df['Type'] == 'TV Show']
    df.loc[tv_series_rows.index, 'tv_series_duration'] = tv_series_rows['duration']
    df.loc[tv_series_rows.index, 'duration'] = ""
    return df



# In[235]:


df = separate_tv_series_duration(df)


# In[103]:


df


# # THE MOST COMMON GENRE

# In[236]:


from collections import Counter

all_genres = df[['genre_0', 'genre_1', 'genre_2']].stack().str.strip().tolist()

genre_counts = Counter(all_genres)

most_common_genre, count = genre_counts.most_common(1)[0]

print("The most common genre is:", most_common_genre)
print("Count:", count)


# # THE MOST POPULAR DIRECTOR

# In[237]:


from collections import Counter

all_directors = df['director'].str.strip().tolist()

director_counts = Counter(all_directors)

most_popular_director, count = director_counts.most_common(1)[0]

print("The most popular director is:", most_popular_director)
print("Count:", count)


# In[238]:


most_popular_director, count = director_counts.most_common(1)[0]

second_most_popular_director, second_count = director_counts.most_common(2)[1]

print("The most popular director is:", second_most_popular_director)
print("Count:", second_count)


# # DATA VISUALIZATION
# 

# In[225]:


#Most Popular Director
director_counts = df['director'].value_counts()[:5]
plt.figure(figsize=(10, 6))
sns.barplot(x=director_counts.values, y=director_counts.index)
plt.title("Top 5 Directors with the Most Movies")
plt.xlabel("Number of Movies")
plt.ylabel("Director")
plt.show()


# In[129]:


#  Countries that Make the Most Movies
country_counts = df['Country'].value_counts()
top_countries = country_counts.head(5)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top 5 Countries Producing the Most Movies")
plt.xlabel("Number of Movies")
plt.ylabel("Country")
plt.show()


# In[227]:


# Bottom 5 Countries Producing the Least Movies                      
country_counts = df['Country'].value_counts()
bottom_countries = country_counts.tail(5)
plt.figure(figsize=(12, 6))
sns.barplot(x=bottom_countries.values, y=bottom_countries.index)
plt.title("Bottom 5 Countries Producing the Least Movies")
plt.xlabel("Number of Movies")
plt.ylabel("Country")
plt.show()


# In[266]:


# Movie Trends Over the Years
year_counts = df['year_added'].value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o", markersize=8)
plt.title("Movie Trends Over the Years")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.show()



# In[230]:


#Types  
type_counts = df['Type'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Types')
plt.axis('equal')
plt.show()


# In[229]:


df['Type'] = df['Type'].str.strip()
unique values in the 'Type' column again
print(df['Type'].unique())


# In[247]:


#Top 10 Most Popular Genres
genre_counts = df[['genre_0', 'genre_1', 'genre_2']].stack().value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index)
plt.title("Top 10 Most Popular Genres")
plt.xlabel("Number of Movies/TV Shows")
plt.ylabel("Genre")
plt.show()



# In[272]:


#Number of Movies and TV Shows Added Over the Years
df['parsed_year'] = df['parsed_date'].dt.year
yearly_counts = df.groupby(['parsed_year', 'Type']).size().unstack()
plt.figure(figsize=(12, 12))
yearly_counts.plot(kind='line', marker='o', markersize=8)
plt.title("Number of Movies and TV Shows Added Over the Years")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend(title="Type", loc="upper left")
plt.show()


# In[ ]:




