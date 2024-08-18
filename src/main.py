import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json


creds_json = st.secrets['google']['application_credentials']
creds_dict = json.loads(creds_json)


# loading sheet from google
scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)


sheet_id = '150FEJZreTXRc3NrDRhSouMDFdAVfuQFxJ5NnRzPrm98'
sheet = client.open_by_key(sheet_id)
worksheet = sheet.sheet1


values_list = worksheet.get_all_records()
df = pd.DataFrame(values_list)


st.title('Easy Eat')

st.subheader('Rezeptvorschau')
st.write(df.head())

# filter sheet
search_input = st.text_input('Suche ein Rezept:', help='Suchparameter: Gericht | Kategorie | Ernährungsweise | Dauer | Zutaten').strip()

def search_recipes(df, search_param): 
      return df[df.apply(lambda row: row.astype(str).str.contains(search_param, case=False, na=False).any(), axis=1)]

if search_input:
    filtered_df = search_recipes(df, search_input)
    
    if not filtered_df.empty:
        st.subheader('Gefundene Rezepte:')
        st.write(filtered_df)
    else:
        st.subheader('Es wurde kein Gericht gefunden.')
      
        
st.subheader('Optional:')
columns = df.columns.tolist()
selected_column = st.selectbox('Wähle eine Spalte nach der gefiltert werden soll:', columns)
unique_values = df[selected_column].unique()
selected_value = st.selectbox('Wähle einen Wert:', unique_values)

filtered_df = df[df[selected_column] == selected_value]
st.write(filtered_df)




