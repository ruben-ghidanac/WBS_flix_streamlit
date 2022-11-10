import streamlit as st
import pandas as pd
from src.functions import *

UserID = st.number_input("UserID")
Top_n_movies = st.number_input("Top_n_movies")
st.write("The top", Top_n_movies, "movies recomandation:", recommendations_for_specific_user_id(UserID, Top_n_movies))
