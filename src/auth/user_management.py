import streamlit as st
import pandas as pd


def registrate_new_user(authenticator, config, worksheet):
    """
    Registers a new user and updates the Google Sheet with their details.

    Params:
        config (dict): The configuration dictionary containing user credentials.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
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

    except Exception as e:
        st.sidebar.error(e)
        

def reset_pw(authenticator, config, curr_user, worksheet):
    """
    Resets a user's password and updates the Google Sheet.

    Params:
        config (dict): The configuration dictionary containing user credentials.
        search (str): The username of the user whose password is to be reset.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    try:
        if authenticator.reset_password(
            st.session_state['username'], 
            location='sidebar', 
            fields={'Form name':'Passwort zurückseten', 
                    'Current password':'Aktuelles Passwort',
                    'New password':'Neues Passwort',                                            'Repeat password':'Passwort bestätigen', 'Reset':'Zurücksetzen'}):
            update_config(config, curr_user, worksheet)
            st.sidebar.success('Passwort wurde erfolgreich geändert')
    except Exception as e:
        st.sidebar.error(e)
        
        
def update_config(config, curr_user, worksheet):
    """
    Updates the configuration and Google Sheet with new user data.

    Params:
        config (dict): The configuration dictionary containing user credentials.
        search (str): The username of the user whose data is to be updated.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
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
    
    filtered_df = df[df['username'] == curr_user]
    
    if not filtered_df.empty:
        data = worksheet.get_all_records()
        for i, row in enumerate(data):
            if row['username'] == curr_user:
                row_index = i + 2
                new_data = [
                    curr_user,
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