import streamlit as st
import streamlit_authenticator as stauth

import yaml

from database import load_sheet_data


def authenticate_user():
    """
    Authenticates a user using credentials stored in a Google Sheet.

    Returns:
        stauth.Authenticate: The Streamlit Authenticator object for handling user authentication.
        dict: The configuration dictionary used by the authenticator.
        gspread.models.Worksheet: The worksheet object representing the Google Sheet.
    """
    SHEET_ID = '1_nJOUU06XiRuq0W-d1kaY7e5oKa1tlXLettEh_T_xh8'
    secrets = st.secrets['google']['db_credentials']

    df, worksheet = load_sheet_data(SHEET_ID, secrets)

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


def handle_auth_error(status):
    """
    Handles authentication errors and prompts user registration if necessary.

    Params:
        config (dict): The configuration dictionary containing user credentials.
        status (bool or None): The authentication status. False indicates a failure, None indicates no attempt yet.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    if status is False:
        st.error('Username/Passwort ist falsch')
        return True
    elif status is None:
        st.warning('Bitte gebe deine Anmeldedaten ein')
        return True
    
    return False