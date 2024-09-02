import streamlit as st

from auth import handle_authentication
from recipes import load_recipe, handle_search, handle_optional_search, handle_add_recipe, handle_delete_recipe


st.set_page_config(page_title='Easy Eat | Home')   
 

def main():
    df, worksheet = load_recipe()
    
    st.title('Easy Eat')
    st.subheader('Rezeptvorschau')
    st.write(df.head())
    
    handle_search(df)
    handle_optional_search(df)
    handle_add_recipe(worksheet)
    handle_delete_recipe(df, worksheet)
            

if __name__ == '__main__':  
    # ---------- AUTHENTICATION ----------
    auth_successful = handle_authentication()
    if auth_successful:
        main()
