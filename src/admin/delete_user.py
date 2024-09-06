import streamlit as st

from utils import search, delete_row


def handle_delete_user(df, worksheet):
    """
    Handles the user deletion process within the application.

    This function allows the user to select a user from a dropdown list and delete them from the Google Sheet.
    If the user exists in the DataFrame, their name is displayed, and a confirmation button allows for deletion.
    The function provides feedback on whether the deletion was successful or if an error occurred.

    Params:
        df (pandas.DataFrame): The DataFrame containing the user data.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    delete_input = st.selectbox('Wählen Sie den Namen des Users, welchen Sie löschen möchten:', df['username'], index=None, placeholder='Wähle einen User', help='Am PC können Sie auch in das Feld schreiben um zu suchen')
    
    if df.empty:
        st.warning('Keine User in der Datenbank, fügen Sie erst welche hinzu.')
    if delete_input:
        value_to_delete = search(df, delete_input)
        if not value_to_delete.empty:
            st.write(f'Wollen Sie den Benutzer: `{delete_input}` wirklich löschen?')
            if st.button('Löschen'):    
                delete_row(worksheet, delete_input, entity_type='user') 
        else:
            st.write('Kein User gefunden, bitte überprüfe deine Eingabe!')