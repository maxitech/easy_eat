import streamlit as st

from utils import init_btn_session_state, toggle_btn_session_state, search, delete_row

from .recipe_management import add_recipe
from .display_recipe import display_recipe


def handle_search(df):
    """
    Handles the recipe search functionality within the application.

    This function prompts the user to input a search query for recipes, then filters
    the DataFrame based on the input. The results are displayed if any matching recipes
    are found; otherwise, a message is shown indicating that no recipes were found.

    Params:
        df (pandas.DataFrame): The DataFrame containing the recipe data.

    Returns:
        None
    """
    search_input = st.text_input('Suche ein Rezept:', help='Suchparameter: Gericht | Zutaten').strip()

    if search_input:
        filtered_df = search(df, search_input)
        
        if not filtered_df.empty:
            st.write(f"Rezepte mit '{search_input}':")
            display_recipe(filtered_df)
        else:
            st.write(f"Keine Rezepte gefunden mit '{search_input}'.")


def handle_optional_search(df):
    """
    Handles the optional filter search functionality within the application.

    This function allows the user to filter recipes based on specific columns.
    The user can select a column and filter the recipes by its unique values.
    The filtered results are displayed accordingly.

    Params:
        df (pandas.DataFrame): The DataFrame containing the recipe data.

    Returns:
        None
    """
    init_btn_session_state('show_optional_filter')
    
    if st.button('Optionaler Filter'):
        toggle_btn_session_state('show_optional_filter')
    
    if st.session_state['show_optional_filter']:
        columns = df.columns.tolist()
        selected_column = st.selectbox('Wähle eine Spalte nach der gefiltert werden soll:', columns, index=None, placeholder='Wähle eine Option')
        
        if selected_column is not None:
            unique_values = df[selected_column].unique()
            selected_value = st.selectbox(f'Filter nach {selected_column}:', unique_values, index=None)

            if selected_value:
                filtered_df = df[df[selected_column] == selected_value]
                display_recipe(filtered_df)
            else:
                st.warning('Bitte wähle einen zweiten Filter!')


def handle_add_recipe(worksheet):
    """
    Handles the form submission for adding a new recipe to the Google Sheet.

    This function displays a form where users can input details for a new recipe,
    including the meal name, ingredients, category, nutrition type, duration and preparation.
    Once the form is submitted, the recipe is added to the Google Sheet.

    Params:
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    with st.form('recipe_form'):
        st.subheader('Füge ein Rezept hinzu') 
        meal_name = st.text_input(label='Name des Gerichts', placeholder='Thunfisch Wraps').strip().title() 
        ingredients = st.text_area(label='Zutaten', placeholder='100g Thunfisch, 2 Blätter Salat, 1/4 Gurke...').strip() 
        
        category = st.selectbox('Wähle eine Kategorie', ['Frühstück', 'Mittagessen', 'Abendessen', 'Beliebige Mahlzeit'], index=None, placeholder='Welche Mahlzeit passt zu deinem Rezept?')
        nutrition = st.selectbox('Wähle eine Ernährungsweise:', ['vegan', 'vegetarisch', 'andere'], index=None, placeholder='Was ist die passende Ernährungsweise zu deinem Rezept?')
        duration = st.selectbox('Wähle eine Option:', ['kurz', 'mittel', 'lang'], index=None, placeholder='Wie lange dauert dein Gericht?')
        preparation = st.text_area(label='Wie wird das Gericht zubereitet?', placeholder='Beschreibe die Zubereitung')
        
        confirm_submit = st.checkbox("Ja, ich habe alles überprüft und möchte das Rezept abschicken.")
        submitted = st.form_submit_button('Hinzufügen')
        
        if st.session_state['user_role'] == 'demo':
            return
        
        if submitted:
            if not confirm_submit:
                st.error('Bitte bestätigen Sie, dass Sie alles überprüft haben.')
            elif not (meal_name and ingredients and category and nutrition and duration and preparation):
                st.error('Bitte füllen Sie die Felder aus!')
            else:
                add_recipe(worksheet, meal_name, ingredients, category, nutrition, duration, preparation)


def handle_delete_recipe(df, worksheet):
    """
    Handles the recipe deletion process within the application.

    This function allows the user to select a recipe from a dropdown list and delete it from the Google Sheet.
    If the recipe exists in the DataFrame, it is displayed, and a confirmation button allows for deletion.
    The function provides feedback on whether the deletion was successful or if an error occurred.

    Params:
        df (pandas.DataFrame): The DataFrame containing the recipe data.
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    delete_input = st.selectbox('Wählen Sie den Namen des Rezeptes, welches Sie löschen möchten:', df['Gericht'], index=None, placeholder='Wähle das Rezept', help='Am PC können Sie auch in das Feld schreiben um zu suchen')
    
    if df.empty:
        st.warning('Keine Rezepte zum Löschen, fügen Sie erst welche hinzu.')
    if delete_input:
        value_to_delete = search(df, delete_input)
        if not value_to_delete.empty:
            st.write(value_to_delete)
            if st.button('Löschen'):    
                delete_row(worksheet, delete_input, entity_type='recipe') 
        else:
            st.write('Kein Rezept gefunden, bitte überprüfe deine Eingabe!')
