import os # paths to file
import numpy as np # linear algebra
import pandas as pd # data processing
import warnings # warning filter
import scipy as sp # pivot egineering


# ML model
from sklearn.metrics.pairwise import cosine_similarity


# default theme and settings
pd.options.display.max_columns

# warning handle
warnings.filterwarnings("always")
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    # list all files under the input directory
    for dirname, _, filenames in os.walk('data/'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    # store file paths to variables
    anime_path = 'data/anime.csv'
    rating_path = 'data/rating.csv'

    anime_df = pd.read_csv(anime_path)
    #print(anime_df.head())
    
    rating_df = pd.read_csv(rating_path)
    #print(rating_df.head())

    # Percentage of null values in anime_df
    #print(round(anime_df.isnull().sum().sort_values(ascending=False)/len(anime_df.index), 4)*100) 
    # Null values in rating, genre, type

    # Percentage of null values in rating_df
    #print(round(rating_df.isnull().sum().sort_values(ascending=False)/len(rating_df.index), 4)*100) 
    # No null values!

    # Dropping data that has nan values for rating
    anime_df = anime_df[~np.isnan(anime_df["rating"])]

    # Filling nan values for genre with "Unknown"
    anime_df["genre"] = anime_df["genre"].fillna("Unknown")
    # Filling nan values for type with mode value of type
    anime_df["type"] = anime_df["type"].fillna(anime_df["type"].dropna().mode().values[0])

    # Checking to see we have no more null values
    #print(anime_df.isnull().sum())
    # No more null values!
