import streamlit as st

from recipes import load_recipe, handle_search, handle_optional_search
  

df, worksheet = load_recipe()

st.title('Easy Eat')
st.subheader('Rezeptvorschau')
st.write(df.head())

handle_search(df)
handle_optional_search(df)