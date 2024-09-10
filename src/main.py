import streamlit as st

from auth import handle_authentication


def main():
       
    # --- PAGE SETUP ---    
    home_page = st.Page(
        page='views/home_route.py', 
        title='Home', 
        default=True
    )
    
    add_recipe = st.Page(
        page='views/add_recipe_route.py',
        title='Rezept hinzufügen',
    )
     
    admin_panel = st.Page(
        page='views/admin_route.py',
        title='Admin Panel'
    )
    
    
    # --- CHECK USER ROLE ---
    if st.session_state['user_role'] == 'admin':    
        pages = {
            'App':[home_page, add_recipe, admin_panel]
        }
        st.sidebar.markdown("**Hinweis:** Sie haben die Rolle `Admin`.")
    else:
        pages = {
            'App': [home_page, add_recipe],
        }
        st.sidebar.markdown("**Hinweis:** Sie haben derzeit die Rolle `User`. Bitte wenden Sie sich an den Administrator, wenn Sie Zugang zu weiteren Funktionen benötigen.")


    # --- NAVIGATION SETUP ---
    pg = st.navigation(pages)   
    pg.run()


if __name__ == '__main__':
    # --- AUTHENTICATION ---
    auth_successful = handle_authentication()
    if auth_successful:
        main()
