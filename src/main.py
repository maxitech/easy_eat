import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]
SHEET_ID = '150FEJZreTXRc3NrDRhSouMDFdAVfuQFxJ5NnRzPrm98'


def load_credentials():
    '''
    Loads google API login data from steamlit-secrets TOML file.
    
        Returns: 
            google.oauth2.service_account.Credentials: A Credentials object that contains the credentials for accessing Google APIs.
    '''
    creds_json = st.secrets['google']['application_credentials']
    creds_dict = json.loads(creds_json)
    return Credentials.from_service_account_info(creds_dict, scopes=SCOPES)


def load_sheet_data(sheet_id):
    '''
    Loads data from a Google Sheet and returns it as a Pandas DataFrame.

        Params:
            sheet_id (str): The ID of the Google Sheet to load data from.

        Returns:
            pandas.DataFrame: A DataFrame containing the data from the Google Sheet.
    '''
    creds = load_credentials()
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1
    values_list = worksheet.get_all_records()
    return pd.DataFrame(values_list)


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


def main():
    '''
     Main function that loads the Google Sheet data, displays a preview, and provides search and filter functionality.

        This function:
        - Loads data from a Google Sheet into a Pandas DataFrame.
        - Displays the first few rows of the DataFrame.
        - Provides a text input for searching recipes based on various parameters.
        - Displays the filtered recipes based on the search input.
        - Provides an optional filter to select and display recipes based on a specific column value.
    '''
    df = load_sheet_data(SHEET_ID)
    
    st.title('Easy Eat')
    st.subheader('Rezeptvorschau')
    st.write(df.head())

    search_input = st.text_input('Suche ein Rezept:', help='Suchparameter: Gericht | Kategorie | Ernährungsweise | Dauer | Zutaten').strip()


    if search_input:
        filtered_df = search_recipes(df, search_input)
        
        if not filtered_df.empty:
            st.subheader(f"Rezepte mit '{search_input}:")
            st.write(filtered_df)
        else:
            st.write(f"Keine Rezepte gefunden mit '{search_input}'.")
        
            
    st.subheader('Optional:')
    columns = df.columns.tolist()
    selected_column = st.selectbox('Wähle eine Spalte nach der gefiltert werden soll:', columns, index=None, placeholder='Wähle eine Option')
    if selected_column is not None:
        unique_values = df[selected_column].unique()
        selected_value = st.selectbox(f'Filter nach {selected_column}:', unique_values)
        filtered_df = df[df[selected_column] == selected_value]
        st.write(filtered_df)


if __name__ == '__main__':
    main()
