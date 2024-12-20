import streamlit as st
from uuid import uuid4

from auth import authenticate_user, handle_auth_error, update_config, registrate_new_user, reset_pw
from utils import init_btn_session_state, toggle_btn_session_state


def handle_authentication():
    """
    Handles the entire authentication flow.

    Returns:
        bool: True if authentication was successful, False otherwise.
    """
    try:
        if 'uuid_key' not in st.session_state:
            st.session_state['uuid_key'] = str(uuid4())
        uuid_key = st.session_state['uuid_key']
        
        authenticator, config, worksheet = authenticate_user()

        if 'config' not in st.session_state or st.session_state['config'] != config:
            st.session_state['config'] = config

        if 'worksheet' not in st.session_state or st.session_state['worksheet'] != worksheet:
            st.session_state['worksheet'] = worksheet
        
        authenticator.login(
            location='main', 
            fields={'Form name':'Anmeldung', 'Username':'Nutzername', 'Password':'Passwort', 'Login':'Anmelden'}, 
            key=uuid_key)
        
        if st.session_state['authentication_status']:
            user_role = config['credentials']['usernames'][st.session_state['username']]['role']
            
            if 'user_role' not in st.session_state or st.session_state['user_role'] != user_role:
                st.session_state['user_role'] = config['credentials']['usernames'][st.session_state['username']]['role']
                
            st.sidebar.write(f'Wilkommen {st.session_state["name"]}')
            authenticator.logout(button_name='Abmelden', location='sidebar', key=uuid_key)
            
            init_btn_session_state('show_pw_reset')
            if st.sidebar.button('Passwort ändern'):
                toggle_btn_session_state('show_pw_reset')
                
            if st.session_state['show_pw_reset']:
                if st.session_state['user_role'] != 'demo':
                    reset_pw(authenticator, config, st.session_state['username'], worksheet)
                else:
                    st.sidebar.info('Im Demo-Account können Sie das Passwort nicht ändern! Erstellen Sie einen Account, um das Passwort zu ändern.')
                
            update_config(config, st.session_state['username'], worksheet)  
            return True
        else:
            if handle_auth_error(st.session_state['authentication_status']):
                init_btn_session_state('show_reg_new_user')
                if st.button('Erstellen Sie einen Account'):
                    toggle_btn_session_state('show_reg_new_user')
                    
                if st.session_state['show_reg_new_user']:
                    registrate_new_user(authenticator, config, worksheet)
            return False
    except Exception as e:
        st.error('Ein Fehler bei der Authentifizierung ist aufgetreten. Wenn dieser Fehler weiterhin besteht, überprüfen Sie bitte Ihre Netzwerkverbingung und versuchen Sie es später erneut.')