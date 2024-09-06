import streamlit as st
import gspread

def delete_row(worksheet, del_val, entity_type):
    """
    Deletes a row from the Google Sheet based on the del_val.

    Params:
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.
        del_val (str): The name of the recipe to delete.
        entity_type(str): Either 'recipe' | 'user' for the custom promt of the status. 

    Returns:
        bool: True if the row was successfully deleted, False if the row was not found or an error occurred.
    """
    try:
        cell = worksheet.find(del_val)
        
        if cell: 
            worksheet.delete_rows(cell.row)
            if entity_type == 'recipe':
                st.success(f'Das Rezept: {del_val} wurde erfolgreich gelöscht!')
            elif entity_type == 'user':
                st.success(f'Der Benutzer: {del_val} wurde erfolgreich gelöscht!')
            else:
                st.warning('Löschen war erfolgreich, aber der Entitätstyp ist unbekannt.')
            return True
        else:
            if entity_type == 'recipe':
                st.error(f'Das Rezept: {del_val} konnte nicht gefunden werden, überprüfen Sie Ihre Eingabe!')
            elif entity_type == 'user':
                st.error(f'Der Benutzer: {del_val} konnte nicht gefunden werden, überprüfen Sie Ihre Eingabe!')
            else:
                st.error('Ein unerwarteter Fehler ist aufgetreten!')
            return False
        
    except gspread.exceptions.APIError as api_error:
        st.error(f"API-Fehler aufgetreten: {api_error}")
        return False
    except gspread.exceptions.RequestError as request_error:
        st.error(f"Netzwerkfehler aufgetreten: {request_error}")
        return False
    except Exception as error:
        st.error(f'Ein unerwarteter Fehler ist aufgetreten: {error}')
        return False