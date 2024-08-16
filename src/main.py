import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import os
from dotenv import load_dotenv

load_dotenv()
creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
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






