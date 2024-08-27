import gspread
import gspread.exceptions
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

import json
from uuid import uuid4
import yaml


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]


def load_credentials(secrets):
    creds_json = secrets
    creds_dict = json.loads(creds_json)
    return Credentials.from_service_account_info(creds_dict, scopes=SCOPES)


def load_sheet_data(sheet_id, secrets):
    '''
    Loads data from a Google Sheet and returns it as a Pandas DataFrame.

        Params:
            sheet_id (str): The ID of the Google Sheet to load data from.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the Google Sheet.
    '''
    creds = load_credentials(secrets)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    values_list = worksheet.get_all_values()
    
    if values_list:
        df = pd.DataFrame(values_list[1:], columns=values_list[0])
    else:
        df = pd.DataFrame(columns=worksheet.row_values(1))
    return df, worksheet


def authenticate_user():
    SHEET_ID = '1_nJOUU06XiRuq0W-d1kaY7e5oKa1tlXLettEh_T_xh8'
    secrets = st.secrets['google']['db_credentials']

    df, worksheet = load_sheet_data(SHEET_ID, secrets)
    st.write(df)

    credentials = {'usernames': {}}
    for _, row in df.iterrows():
        username = row['username']
        credentials['usernames'][username] = {
            'email': row['email'],
            'name': row['name'],
            'password': row['password']
        }
        
    with open('../config.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    
    config['credentials'] = credentials
    # Pre-hashing all plain text passwords once
    # Hasher.hash_passwords(config['credentials'])

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']
    )

    return authenticator, config, worksheet


def registrate_new_user(config, worksheet):
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            pre_authorization=False, 
            location='sidebar', 
            fields={
                'Form name': 'Registrierung', 
                'Email': 'Email', 
                'Username': 'Benutzername', 
                'Password': 'Passwort', 
                'Repeat password': 'Passwort bestätigen', 
                'Register': 'Registrieren'
            }, 
            captcha=False
        )

        if email_of_registered_user:
            st.sidebar.success('Registrierung erfolgreich! Sie können sich jetzt anmelden')

            password = config['credentials']['usernames'].get(username_of_registered_user, {}).get('password')

            config['credentials']['usernames'][username_of_registered_user] = {
                'email': email_of_registered_user,
                'name': name_of_registered_user,
                'password': password,
            }

            new_data = [
                username_of_registered_user,
                email_of_registered_user,
                name_of_registered_user,
                password,
            ]
            worksheet.append_row(new_data)
            st.write(f"Added new row for user {username_of_registered_user}")

    except Exception as e:
        st.sidebar.error(e)


def update_config(config, search, worksheet):
    users = config['credentials']['usernames']
    
    data_to_update = []
    for username, details in users.items():
        user_info = {
            "username": username,
            "email": details.get("email"),
            "name": details.get("name"),
            "password": details.get("password")
        }
        data_to_update.append(user_info)
        
    
    df = pd.DataFrame(data_to_update)
    
    filtered_df = df[df['username'] == search]
    
    if not filtered_df.empty:
        data = worksheet.get_all_records()
        for i, row in enumerate(data):
            if row['username'] == search:
                row_index = i + 2
                new_data = [
                    search,
                    filtered_df.iloc[0]['email'],  
                    filtered_df.iloc[0]['name'], 
                    filtered_df.iloc[0]['password']  
                ]
                
                worksheet.update(
                    range_name=f"A{row_index}:D{row_index}", 
                    values=[new_data]
                )
                return
    else:
        return None
  

def handle_auth_error(config, status, worksheet):
    if status is False:
        st.error('Username/Passwort ist falsch')
    elif status is None:
        st.warning('Bitte gebe deine Anmeldedaten ein')
    
    registrate_new_user(config, worksheet)


def reset_pw(config, search, worksheet):
    try:
        if authenticator.reset_password(
            st.session_state['username'], 
            location='sidebar', 
            fields={'Form name':'Passwort zurückseten', 
                    'Current password':'Aktuelles Passwort',
                    'New password':'Neues Passwort',                                            'Repeat password':'Passwort bestätigen', 'Reset':'Zurücksetzen'}):
            update_config(config, search, worksheet)
            st.sidebar.success('Passwort wurde erfolgreich geändert')
    except Exception as e:
        st.sidebar.error(e)


def search_recipes(df, search_params):
    '''
    Searches for recipes in the DataFrame that match the given search parameters.

        Params:
            df (pandas.DataFrame): The DataFrame containing recipe data.
            search_params (str): A string of search terms separated by spaces.

        Returns:
            pandas.DataFrame: A DataFrame containing the recipes that match the search terms.
    '''
    search_terms = search_params.split()
    
    for term in search_terms:
        df = df[df.apply(lambda row: row.astype(str).str.contains(term, case=False, na=False).any(), axis=1)]
    return df


def add_recipe(worksheet, meal_name, ingredients, category, nutrition, duration):
    '''
    Adds a new recipe to the Google Sheet and handles potential errors.

    This function takes the details of a recipe, formats them into a dictionary, 
    and appends the recipe as a new row to the provided Google Sheets worksheet.
    It also provides error handling for API and network-related issues, 
    and gives feedback to the user via Streamlit.

        Params:
            worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.
            meal_name (str): The name of the recipe.
            ingredients (str): A string listing the ingredients for the recipe.
            category (str): The category of the meal (e.g., Breakfast, Lunch, Dinner).
            nutrition (str): The type of diet the recipe supports (e.g., vegan, vegetarian).
            duration (str): The estimated preparation time for the recipe (e.g., short, medium, long).

        Returns:
            bool: True if the recipe was successfully added, False if an error occurred.
    '''
    
    try:
        new_recipe = {
                    'Gericht': meal_name, 
                    'Kategorie': category, 
                    'Ernährungsweise': nutrition, 
                    'Dauer': duration, 
                    'Zutaten': ingredients
                }
        
        worksheet.append_row(list(new_recipe.values()))
        st.success(f'Rezept {meal_name} wurde erfolgreich hinzugefügt!')
        return True
    
    except gspread.exceptions.APIError as api_error:
        st.error(f"API Fehler aufgetreten: {api_error}")
        return False
    except gspread.exceptions.RequestError as request_error:
        st.error(f"Netzwerkfehler aufgetreten: {request_error}")
        return False
    except Exception as error:
        st.error(f'Ein unerwarteter Fehler ist aufgetreten! {error}')
        return False


def delete_recipe(worksheet, meal_name):
    '''
    Deletes a recipe from the Google Sheet based on the meal name.

    This function searches for the row that contains the specified meal name and deletes it 
    from the Google Sheet.

        Params:
            worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.
            meal_name (str): The name of the recipe to delete.

        Returns:
            bool: True if the recipe was successfully deleted, False if the recipe was not found or an error occurred.
    '''
    try:
        cell = worksheet.find(meal_name)
        
        if cell: 
            worksheet.delete_rows(cell.row)
            st.success('Das Rezept wurde erfolgreich gelöscht!')
            return True
        else:
            st.error('Das Rezept konnte nicht gelöscht werden, überprüfen Sie ihre Eingabe!')  
            return False
        
    except gspread.exceptions.APIError as api_error:
        st.error(f"API Fehler aufgetreten: {api_error}")
        return False
    except gspread.exceptions.RequestError as request_error:
        st.error(f"Netzwerkfehler aufgetreten: {request_error}")
        return False
    except Exception as error:
        st.error(f'Ein unerwarteter Fehler ist aufgetreten! {error}')
        return False
    

def main():
    '''
     Main function that loads the Google Sheet data, displays a preview, and provides search and filter functionality.

        This function:
        - Loads data from a Google Sheet into a Pandas DataFrame.
        - Displays the first few rows of the DataFrame.
        - Provides a text input for searching recipes based on various parameters.
        - Displays the filtered recipes based on the search input.
        - Allows user to add his own recepis to the sheet(db)
        - Provides an optional filter to select and display recipes based on a specific column value.
    '''
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
        reset_pw(config, st.session_state['username'], worksheet)
        update_config(config, st.session_state['username'], worksheet)  
        main()
    else:
        handle_auth_error(config, st.session_state['authentication_status'], worksheet) 