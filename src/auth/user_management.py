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
            fields={
                'Form name': 'Registrierung', 
                'Email': 'Email', 
                'Username': 'Benutzername', 
                'Password': 'Passwort', 
                'Repeat password': 'Passwort bestätigen', 
                'Register': 'Registrieren'
            }, 
            captcha=False, 
            domains=[
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "aol.com",
            "msn.com",
            "live.com",
            "comcast.net",
            "me.com",
            "protonmail.com",
            "ymail.com",
            "mail.com",
            "gmx.com"
            ]
        )

        if email_of_registered_user:
            st.success('Registrierung erfolgreich! Sie können sich jetzt anmelden')

            password = config['credentials']['usernames'].get(username_of_registered_user, {}).get('password')

            config['credentials']['usernames'][username_of_registered_user] = {
                'email': email_of_registered_user,
                'name': name_of_registered_user,
                'password': password,
                'role': 'user'
            }

            new_data = [
                username_of_registered_user,
                email_of_registered_user,
                name_of_registered_user,
                password,
                'user'
            ]
            worksheet.append_row(new_data)

    except Exception as e:
        st.error(e)
        
    st.text(body='Passwort', help='8-20 Zeichen | min. 1 Großbuchstabe, Kleinbuchstabe, Zahl & Sonderzeichen (@$!%*?&)')  

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
            fields={'Form name':'Passwort zurücksetzen', 
                    'Current password':'Aktuelles Passwort',
                    'New password':'Neues Passwort',
                    'Repeat password':'Passwort bestätigen', 
                    'Reset':'Zurücksetzen'}):
            update_config(config, curr_user, worksheet)
            st.sidebar.success('Passwort wurde erfolgreich geändert')
    except Exception as e:
        st.sidebar.error(e)
        
    st.sidebar.text(body='Passwort', help='8-20 Zeichen | min. 1 Großbuchstabe, Kleinbuchstabe, Zahl & Sonderzeichen (@$!%*?&)')
        
def update_config(config, user, worksheet, new_role=None):
    """
    Updates the configuration and Google Sheet with new user data.

    Params:
        config (dict): The configuration dictionary containing user credentials.
        user (str): The username of the user whose data is to be updated.
        worksheet (gspread.models.Worksheet):
        new_role (str): New role of the user | None 

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
            "password": details.get("password"),
            "role": details.get("role")
        }
        data_to_update.append(user_info)
        
    
    df = pd.DataFrame(data_to_update)
    
    filtered_df = df[df['username'] == user]
    
    if not filtered_df.empty:
        data = worksheet.get_all_records()
        for i, row in enumerate(data):
            if row['username'] == user:
                row_index = i + 2

                role = new_role if new_role else row['role']
                
                new_data = [
                    user,
                    filtered_df.iloc[0]['email'],  
                    filtered_df.iloc[0]['name'], 
                    filtered_df.iloc[0]['password'],
                    role
                      
                ]
                
                worksheet.update(
                    range_name=f"A{row_index}:E{row_index}", 
                    values=[new_data]
                )
                
                config['credentials']['usernames'][user] = {
                'email': filtered_df.iloc[0]['email'],  
                'name': filtered_df.iloc[0]['name'], 
                'password': filtered_df.iloc[0]['password'], 
                'role': role
                }
                return
    else:
        return None