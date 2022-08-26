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
    print(anime_df.head())
    
    rating_df = pd.read_csv(rating_path)
    print(rating_df.head())

    