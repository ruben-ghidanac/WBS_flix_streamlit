import streamlit as st
from src.functions import *

"""## Movie Challenge:
Your task: create a function that takes the users userId, and a number (n) and outputs the n most recommended movies based on the cosine similarity of other users.
"""

UserID = st.number_input("Please select your UserID",min_value=1, step=1)
Top_n_movies = st.number_input("Please select a number of Movies which you want to be recommended for you:",min_value=1, step=1)

st.write("We have", Top_n_movies, "movie/s recomandation for user:", UserID, recommendations_for_specific_user_id(UserID, Top_n_movies))
