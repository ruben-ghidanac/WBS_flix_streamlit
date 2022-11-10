# Importing the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Read the data

links = 'data/links.csv'
movies = 'data/movies.csv'
ratings = 'data/ratings.csv'
tags = 'data/tags.csv'

users_items = pd.pivot_table(data=ratings, values=['rating'], index=['movieId'], columns=['userId'])

"""## Movie Challenge:

Your task: create a function that takes the users userId, and a number (n) and outputs the n most recommended movies based on the cosine similarity of other users.
"""

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
  weighted_averages = pd.DataFrame(not_seen_movies.T.dot(weights), columns=["predicted_rating"])

  # find the top 'n' movies from the rating predictions
  recommendations = weighted_averages.merge(movies, left_index=True, right_on="movieId")
  top_n = recommendations.sort_values("predicted_rating", ascending=False).head(top_n_movies)
  
  return top_n

def show_seen_movies_for_specific_user_id(user_id):
  
  users_items_with_names = users_items.merge(movies, left_index=True, right_on="movieId")

  my_list = []

  for i in users_items_with_names.index:
    if users_items_with_names[user_id][i]>0:
      my_list.append(i)

  my_list = pd.DataFrame(my_list)
  my_list = my_list.merge(movies, left_index=True, right_on="movieId")
  my_list = my_list.drop(['movieId'], axis=1)
  my_list.rename(columns = {0:'movieId'}, inplace = True)
  
  return my_list
