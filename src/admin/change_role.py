import streamlit as st

from uuid import uuid4

from auth import update_config

def change_role():
    """
    Displays the user interface for changing the role of a selected user in the system.

    This function allows administrators to select a user and change their role to either 'admin' or 'user'.
    The function restricts modification of the main admin account and provides a streamlined UI that only
    presents roles the user does not currently have. If the selected role is different from the current role, 
    the function updates the role in the configuration and the connected Google Sheet.

    Functionality:
    - Loads the current configuration and worksheet from session state.
    - Displays a list of available users to choose from.
    - Prevents modification of the main admin account.
    - Filters available roles based on the selected user's current role.
    - Allows role change and updates the configuration and worksheet if the new role is different.

    Returns:
        None
    """
    st.subheader('Rollen ändern')
    if 'config' not in st.session_state or 'worksheet' not in st.session_state:
        st.error("Rollen Änderung, nicht verfügbar.")
        return

    config = st.session_state['config']
    worksheet = st.session_state['worksheet']    

    selected_user = st.selectbox('Wählen Sie einen Benutzer', options=list(config['credentials']['usernames'].keys()), index=None)
    
    if selected_user is None:
        st.info('Bitte wähle einen Benutzer aus.')
    elif selected_user == 'admin':
        st.error('Dieser Benutzer kann nicht verändert werden.')
    else:
        current_role = config['credentials']['usernames'][selected_user]['role']
        st.write(f"Aktuelle Rolle von `{selected_user}`: `{current_role}`")
        
        available_roles = [role for role in ['admin', 'user'] if role != current_role]
        new_role = st.selectbox('Neue Rolle auswählen', options=available_roles, index=None)
        
        if st.button('Rolle ändern', key=uuid4()):
            if new_role is None:
                st.warning('Wähle eine Rolle für den Benutzer aus.')
            elif new_role != current_role:
                update_config(config, selected_user, worksheet, new_role=new_role)
                
                st.session_state['config'] = config
                
                st.success(f"Die Rolle wurde auf **{new_role.title()}** geändert.")