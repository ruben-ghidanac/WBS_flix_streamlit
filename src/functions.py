# -*- coding: utf-8 -*-
"""RUBEN_the name of a movie, and a number (n).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oJwiEfNgZ0AWvjL9h-ihpUKr3Ja5kDAf

## Importing the libraries and read the data
"""

# Importing the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data

links = 'data/links.csv'
movies = 'data/movies.csv'
ratings = 'data/ratings.csv'
tags = 'data/tags.csv'

"""## Movie Challenge 1:"""

movies_crosstab = pd.pivot_table(data=ratings, values='rating', index='userId', columns='movieId')

movies_crosstab.sample()

def similar_movies(movies_id, n):
    
  movie_ratings = movies_crosstab[movies_id]
  movie_ratings = movie_ratings[movie_ratings>=0] # exclude NaNs

  similar_to_movie_id = movies_crosstab.corrwith(movies_crosstab[movies_id])
  similar_to_movie_id.dropna(inplace=True)
  similar_to_movie_id = pd.DataFrame(similar_to_movie_id, columns=['PearsonR'])
  similar_to_movie_id.dropna(inplace=True)
      
  rating_r = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
  rating_r['rating_count'] = ratings.groupby('movieId')['rating'].count()

  similar_to_movie_id = similar_to_movie_id.join(rating_r['rating_count'])
  similar_to_movie_id.drop(movies_id, inplace=True)
  top_n = similar_to_movie_id[similar_to_movie_id['rating_count']>=10].sort_values('PearsonR', ascending=False).head(n)
  return top_n

"""## Movie Challenge 2:

Your task: create a function that takes the users userId, and a number (n) and outputs the n most recommended movies based on the cosine similarity of other users.
"""

users_items = pd.pivot_table(data=ratings, values='rating', index='movieId', columns='userId')

users_items.head()

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
