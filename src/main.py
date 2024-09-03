import streamlit as st

from auth import handle_authentication


def main():    
    # --- PAGE SETUP ---    
    home_page = st.Page(
        page='views/home.py', 
        title='Home', 
        default=True
    )
    
    add_recipe = st.Page(
        page='views/add_recipe.py',
        title='Rezept hinzufügen',
    )
  
    del_recipe = st.Page(
        page='views/delete_recipe.py',
        title='Rezept löschen'
    )

    # --- NAVIGATION SETUP ---
    pg = st.navigation(
        {
            'App':[home_page, add_recipe, del_recipe],
        }
    )   
    pg.run()

if __name__ == '__main__':  
    # --- AUTHENTICATION ---
    auth_successful = handle_authentication()
    if auth_successful:
        main()
