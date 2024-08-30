import gspread
import streamlit as st


def add_recipe(worksheet, meal_name, ingredients, category, nutrition, duration):
    """
    Adds a new recipe to the Google Sheet and handles potential errors.

    This function takes the details of a recipe, formats them into a dictionary, 
    and appends the recipe as a new row to the provided Google Sheets worksheet.
    It also provides error handling for API and network-related issues, 
    and gives feedback to the user via Streamlit.

    Params:
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.
        meal_name (str): The name of the recipe.
        ingredients (str): A string listing the ingredients for the recipe.
        category (str): The category of the meal (e.g., Breakfast, Lunch, Dinner).
        nutrition (str): The type of diet the recipe supports (e.g., vegan, vegetarian).
        duration (str): The estimated preparation time for the recipe (e.g., short, medium, long).

    Returns:
        bool: True if the recipe was successfully added, False if an error occurred.
    """
    
    try:
        new_recipe = {
                    'Gericht': meal_name, 
                    'Kategorie': category, 
                    'Ernährungsweise': nutrition, 
                    'Dauer': duration, 
                    'Zutaten': ingredients
                }
        
        worksheet.append_row(list(new_recipe.values()))
        st.success(f'Rezept {meal_name} wurde erfolgreich hinzugefügt!')
        return True
    
    except gspread.exceptions.APIError as api_error:
        st.error(f"API Fehler aufgetreten: {api_error}")
        return False
    except gspread.exceptions.RequestError as request_error:
        st.error(f"Netzwerkfehler aufgetreten: {request_error}")
        return False
    except Exception as error:
        st.error(f'Ein unerwarteter Fehler ist aufgetreten! {error}')
        return False
    
    
def delete_recipe(worksheet, meal_name):
    """
    Deletes a recipe from the Google Sheet based on the meal name.

    Params:
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.
        meal_name (str): The name of the recipe to delete.

    Returns:
        bool: True if the recipe was successfully deleted, False if the recipe was not found or an error occurred.
    """
    try:
        cell = worksheet.find(meal_name)
        
        if cell: 
            worksheet.delete_rows(cell.row)
            st.success('Das Rezept wurde erfolgreich gelöscht!')
            return True
        else:
            st.error('Das Rezept konnte nicht gelöscht werden, überprüfen Sie ihre Eingabe!')  
            return False
        
    except gspread.exceptions.APIError as api_error:
        st.error(f"API Fehler aufgetreten: {api_error}")
        return False
    except gspread.exceptions.RequestError as request_error:
        st.error(f"Netzwerkfehler aufgetreten: {request_error}")
        return False
    except Exception as error:
        st.error(f'Ein unerwarteter Fehler ist aufgetreten! {error}')
        return False