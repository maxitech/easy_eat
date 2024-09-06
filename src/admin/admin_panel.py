import streamlit as st 

from auth import load_users
from recipes import load_recipe, handle_delete_recipe

from .delete_user import handle_delete_user


def show_admin_panel():
    st.title('Admin Panel')
    
    # --- DELETE RECIPE ---
    df, worksheet = load_recipe()
    handle_delete_recipe(df, worksheet)
    
    # --- DELETE USER ---
    df, worksheet = load_users()
    handle_delete_user(df, worksheet)
    st.write(df)