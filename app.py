import streamlit as st
from src.functions import *

UserID = st.number_input("UserID",min_value=1, step=1)
Top_n_movies = st.number_input("Top_n_movies",min_value=1, step=1)

st.write("We have", Top_n_movies, "movie/s recomandation for user:", UserID, recommendations_for_specific_user_id(UserID, Top_n_movies))
