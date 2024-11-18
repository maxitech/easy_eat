import streamlit as st

from recipes import load_recipe, handle_add_recipe


df, worksheet = load_recipe()
if st.session_state['user_role'] == 'demo':
    st.info('Im Demo-Account können Sie keine Rezepte hinzufügen! Erstellen Sie einen Account, um Rezepte hinzuzufügen.')
    handle_add_recipe(worksheet)
else:
    handle_add_recipe(worksheet)
