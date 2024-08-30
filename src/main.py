import streamlit as st

from uuid import uuid4

from database import load_sheet_data
from auth import authenticate_user, handle_auth_error,registrate_new_user, reset_pw, update_config
from recipes import search_recipes, add_recipe, delete_recipe


st.set_page_config(page_title='Easy Eat | Home')   
 

def main():
    """
    Main function that loads the Google Sheet data, displays a preview, and provides search and filter functionality.

    This function:
    - Loads data from a Google Sheet into a Pandas DataFrame.
    - Displays the first few rows of the DataFrame.
    - Provides a text input for searching recipes based on various parameters.
    - Displays the filtered recipes based on the search input.
    - Allows user to add their own recipes to the sheet (db).
    - Provides an optional filter to select and display recipes based on a specific column value.

    Returns:
        None
    """
    SHEET_ID = '150FEJZreTXRc3NrDRhSouMDFdAVfuQFxJ5NnRzPrm98'
    secrets = st.secrets['google']['application_credentials']
    
    df, worksheet = load_sheet_data(SHEET_ID, secrets)
    
    st.title('Easy Eat')
    st.subheader('Rezeptvorschau')
    st.write(df.head())
    

    search_input = st.text_input('Suche ein Rezept:', help='Suchparameter: Gericht | Kategorie | Ernährungsweise | Dauer | Zutaten').strip()

    if search_input:
        filtered_df = search_recipes(df, search_input)
        
        if not filtered_df.empty:
            st.subheader(f"Rezepte mit '{search_input}':")
            st.write(filtered_df)
        else:
            st.write(f"Keine Rezepte gefunden mit '{search_input}'.")
            

    with st.form('recipe_form'):
        st.subheader('Füge ein Rezept hinzu') 
        meal_name = st.text_input('Name des Gerichts').strip().title() 
        ingredients = st.text_input('Zutaten').strip().title() 
        
        category = st.selectbox('Wähle eine Kategorie', ['Frühstück', 'Mittagessen', 'Abendessen'], index=None, placeholder='Welche Mahlzeit passt zu deinem Rezept?')
        nutrition = st.selectbox('Wähle eine Ernährungsweise:', ['vegan', 'vegetarisch', 'andere'], index=None, placeholder='Was ist die passende Ernährungsweise zu deinem Rezept?')
        duration = st.selectbox('Wähle eine Option:', ['kurz', 'mittel', 'lang'], index=None, placeholder='Wie lange dauert dein Gericht?')
        
        submitted = st.form_submit_button('Hinzufügen')
        if submitted:
            if not (meal_name and ingredients and category and nutrition and duration):
                st.error('Bitte füllen Sie die Felder aus!')
            else:
                add_recipe(worksheet, meal_name, ingredients, category, nutrition, duration)


    delete_input = st.selectbox('Wählen Sie den Namen des Rezeptes, welches Sie löschen möchten:', df['Gericht'], index=None, placeholder='Wähle das Rezept', help='Am PC können Sie auch in das Feld schreiben um zu suchen')
    
    if df.empty:
        st.warning('Keine Rezepte zum Löschen, fügen Sie erst welche hinzu.')
    if delete_input:
        value_to_delete = search_recipes(df, delete_input)
        if not value_to_delete.empty:
            st.write(value_to_delete)
            if st.button('Löschen'):    
                delete_recipe(worksheet, delete_input) 
        else:
            st.write('Kein Rezept gefunden, bitte überprüfe deine Eingabe!')
             
                       
    st.subheader('Optional:')
    columns = df.columns.tolist()
    selected_column = st.selectbox('Wähle eine Spalte nach der gefiltert werden soll:', columns, index=None, placeholder='Wähle eine Option')
    if selected_column is not None:
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox(f'Filter nach {selected_column}:', unique_values, index=None)
        if selected_value:
            filtered_df = df[df[selected_column] == selected_value]
            st.write(filtered_df)
        else:
            st.warning('Bitte wähle einen zweiten Filter!')
            

if __name__ == '__main__':  
    # ---------- AUTHENTICATION ----------
    if 'uuid_key' not in st.session_state:
        st.session_state['uuid_key'] = str(uuid4())
    uuid_key = st.session_state['uuid_key']
    
    authenticator, config, worksheet = authenticate_user()
    authenticator.login(
        location='main', 
        fields={'Form name':'Anmeldung', 'Username':'Nutzername', 'Password':'Passwort', 'Login':'Anmelden'}, 
        key=uuid_key)
    
    if st.session_state['authentication_status']:
        st.sidebar.write(f'Wilkommen {st.session_state["name"]}')
        authenticator.logout(button_name='Abmelden', location='sidebar', key=uuid_key)
        reset_pw(authenticator, config, st.session_state['username'], worksheet)
        update_config(config, st.session_state['username'], worksheet)  
        main()
    else:
        if handle_auth_error(st.session_state['authentication_status']):
            registrate_new_user(authenticator, config, worksheet)