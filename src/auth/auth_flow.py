import streamlit as st
from uuid import uuid4
from auth import authenticate_user, handle_auth_error, update_config, registrate_new_user, reset_pw


def handle_authentication():
    """
    Handles the entire authentication flow.

    Returns:
        bool: True if authentication was successful, False otherwise.
    """
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
        
        if 'show_pw_reset' not in st.session_state:
            st.session_state['show_pw_reset'] = False
    
        if st.sidebar.button('Passwort ändern'):
            st.session_state['show_pw_reset'] = not st.session_state['show_pw_reset']  
         
        if st.session_state['show_pw_reset']:
            reset_pw(authenticator, config, st.session_state['username'], worksheet)
        update_config(config, st.session_state['username'], worksheet)  
        return True
    else:
        if handle_auth_error(st.session_state['authentication_status']):
            if 'show_reg_new_user' not in st.session_state:
                st.session_state['show_reg_new_user'] = False
                
            if st.button('Erstellen Sie einen Account'):
                st.session_state['show_reg_new_user'] = not st.session_state['show_reg_new_user']
                 
            if st.session_state['show_reg_new_user']:
                registrate_new_user(authenticator, config, worksheet)
        return False