# Importing the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Read the data

path_links = 'data/links.csv'
path_movies = 'data/movies.csv'
path_ratings = 'data/ratings.csv'
path_tags = 'data/tags.csv'

links = pd.read_csv(path_links)
movies = pd.read_csv(path_movies)
ratings = pd.read_csv(path_ratings)
tags = pd.read_csv(path_tags)

users_items = pd.pivot_table(data=ratings, values='rating', index='movieId', columns='userId')

"""## Movie Challenge 2:

Your task: create a function that takes the users userId, and a number (n) and outputs the n most recommended movies based on the cosine similarity of other users.
"""

# your code here

def recommendations_for_specific_user_id(user_id, top_n_movies):
  
  # replace NaNs with zeros, the cosine similarity can't be computed with NaN's
  users_items.fillna(0, inplace=True)

  # compute cosine similarities
  user_similarities = pd.DataFrame(cosine_similarity(users_items),
                                 columns=users_items.index, 
                                 index=users_items.index)
  
  # compute the weights for 'user_id'
  weights = (
      user_similarities.query("movieId!=@user_id")[user_id] / sum(user_similarities.query("movieId!=@user_id")[user_id]))
  users_items.loc[user_id,:]==0

  # select movies that the 'user_id' has not seen
  not_seen_movies = users_items.loc[users_items.index!=user_id, users_items.loc[user_id,:]==0]
  not_seen_movies.T

  # dot product between the not-visited-restaurants and the weights
  weighted_averages = pd.DataFrame(not_seen_movies.T.dot(weights), columns=["Score recommendation"])
  
  # scale features
  scaler = MinMaxScaler(feature_range=(0, 10), copy=False)
  model=scaler.fit(weighted_averages)
  scaled_data=model.transform(weighted_averages)
  #weighted_averages = weighted_averages.round(2)

  # find the top 'n' movies from the rating predictions
  recommendations = weighted_averages.merge(movies, left_index=True, right_on="movieId")
  recommendations = recommendations.drop(['movieId'], axis=1)
  top_n = recommendations.sort_values("Score recommendation", ascending=False).head(top_n_movies)
  top_n['Score recommendation'] = top_n['Score recommendation'].astype(int)
  top_n.rename(columns = {'title':'Title', 'genres': 'Genres'}, inplace = True)
  top_n = top_n.style.hide_index()

  return top_n
