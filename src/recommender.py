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

def anime_recommendation():
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
    # No null values

    # Dropping data that has nan values for rating
    anime_df = anime_df[~np.isnan(anime_df["rating"])]
    
    # Filling nan values for genre with "Unknown"
    anime_df["genre"] = anime_df["genre"].fillna("Unknown")
    # Filling nan values for type with mode value of type
    anime_df["type"] = anime_df["type"].fillna(anime_df["type"].dropna().mode().values[0])
    #genre mode here is TV
    
    # Checking to see we have no more null values
    #print(anime_df.isnull().sum())
    # No more null values!

    # Convert any -1 rating values to Nan; this will be for the normaliing part later (part of the cosine sim model)
    rating_df['rating'] = rating_df['rating'].apply(lambda x: np.nan if x==-1 else x)


    # Get animes that are of TV type
    anime_df = anime_df[anime_df['type'] == 'TV']

     # Combine anime_df and rating_df (think of this as a SQL inner join)
    rated_anime = rating_df.merge(anime_df, left_on='anime_id', right_on='anime_id', suffixes=['_user', ''])
    # This is equivalent
    #rated_anime = rating_df.merge(anime_df, how='inner', on='anime_id', suffixes=['_user', ''])

    # Extract only user id, name, and user ratings from the combined df
    rated_anime = rated_anime[['user_id', 'name', 'rating_user']]

    # Create pivot table to simplify the formatting of the data
    pivot = rated_anime.pivot_table(index='user_id', columns='name', values='rating_user')

    # Normalize the data because cosine similarity function needs the data to be normalized (-1 to 1 scale)
    pivot_norm = pivot.apply(lambda x: (x-np.mean(x))/(np.max(x) - np.min(x)), axis=1)

    # Replace NaN values with 0
    pivot_norm.fillna(0, inplace=True)
    
    # Transpose the data
    pivot_norm = pivot_norm.T

    # Drop columns that have all 0 values
    pivot_norm = pivot_norm.loc[:, (pivot_norm != 0).any(axis = 0)]

    # Convert df into sparse matrix
    # Sparing: Spreading out the data with mostly 0s for the machine learning computation
    piv_sparse = sp.sparse.csr_matrix(pivot_norm.values)
    print(piv_sparse.head())

    # Cosine model; this is where the fun begins :)
    anime_simularity = cosine_similarity(piv_sparse)
    anime_sim_df = pd.DataFrame(anime_simularity, index = pivot_norm.index, columns = pivot_norm.index)

    return anime_sim_df

if __name__ == '__main__':
    # List all files under the input directory
    # for dirname, _, filenames in os.walk('data/'):
    #     for filename in filenames:
    #         print(os.path.join(dirname, filename))

    # Compute anime similarity data frame
    anime_sim_df=anime_recommendation()
    # Get anime name from user input
    anime=input('What show did you recently finish?')
    
    iter = 1
    print('Since you watched {}, you might like these shows:\n'.format(anime))
    for i in anime_sim_df.sort_values(by = anime, ascending = False).index[1:6]:
        print(f'#{iter}: {i}, {round(anime_sim_df[i][anime]*100,2)}% match') 
        iter += 1
