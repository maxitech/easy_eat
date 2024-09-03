import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

import json


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]


def load_credentials(secrets):
    """
    Loads Google API credentials from a JSON string.

    Params:
        secrets (str): A JSON string containing the service account credentials.

    Returns:
        google.oauth2.service_account.Credentials: The credentials object used to authenticate with Google APIs.
    """
    creds_json = secrets
    creds_dict = json.loads(creds_json)
    return Credentials.from_service_account_info(creds_dict, scopes=SCOPES)


def load_sheet_data(sheet_id, secrets):
    """
    Loads data from a Google Sheet and returns it as a Pandas DataFrame along with the worksheet object.

    This function uses the provided Google Sheets API credentials to authenticate and retrieve data from the specified
    Google Sheet. The data is returned as a Pandas DataFrame, with the first row used as the header. The function also
    returns the worksheet object for further operations.

    Params:
        sheet_id (str): The ID of the Google Sheet to load data from.
        secrets (str): A JSON string containing the service account credentials.

    Returns:
        tuple: A tuple containing:
            - pandas.DataFrame: A DataFrame containing the data from the Google Sheet.
            - gspread.models.Worksheet: The worksheet object representing the Google Sheet.
    """
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
