import streamlit as st

from .search import search_recipes
from .recipe_management import add_recipe, delete_recipe


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
    search_input = st.text_input('Suche ein Rezept:', help='Suchparameter: Gericht | Kategorie | Ernährungsweise | Dauer | Zutaten').strip()

    if search_input:
        filtered_df = search_recipes(df, search_input)
        
        if not filtered_df.empty:
            st.subheader(f"Rezepte mit '{search_input}':")
            st.write(filtered_df)
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
    if st.button('Optionaler Filter'):
        columns = df.columns.tolist()
        selected_column = st.selectbox('Wähle eine Spalte nach der gefiltert werden soll:', columns, index=None, placeholder='Wähle eine Option')
        if selected_column is not None:
            unique_values = df[selected_column].unique()
            selected_value = st.selectbox(f'Filter nach {selected_column}:', unique_values, index=None)
            if selected_value:
                filtered_df = df[df[selected_column] == selected_value]
                st.write(filtered_df)
            else:
                st.warning('Bitte wähle einen zweiten Filter!')


def handle_add_recipe(worksheet):
    """
    Handles the form submission for adding a new recipe to the Google Sheet.

    This function displays a form where users can input details for a new recipe,
    including the meal name, ingredients, category, nutrition type, and duration.
    Once the form is submitted, the recipe is added to the Google Sheet.

    Params:
        worksheet (gspread.models.Worksheet): The worksheet object representing the Google Sheet.

    Returns:
        None
    """
    with st.form('recipe_form'):
        st.subheader('Füge ein Rezept hinzu') 
        meal_name = st.text_input('Name des Gerichts').strip().title() 
        ingredients = st.text_input('Zutaten').strip().title() 
        
        category = st.selectbox('Wähle eine Kategorie', ['Frühstück', 'Mittagessen', 'Abendessen'], index=None, placeholder='Welche Mahlzeit passt zu deinem Rezept?')
        nutrition = st.selectbox('Wähle eine Ernährungsweise:', ['vegan', 'vegetarisch', 'andere'], index=None, placeholder='Was ist die passende Ernährungsweise zu deinem Rezept?')
        duration = st.selectbox('Wähle eine Option:', ['kurz', 'mittel', 'lang'], index=None, placeholder='Wie lange dauert dein Gericht?')
        
        submitted = st.form_submit_button('Hinzufügen')
        if submitted:
            if not (meal_name and ingredients and category and nutrition and duration):
                st.error('Bitte füllen Sie die Felder aus!')
            else:
                add_recipe(worksheet, meal_name, ingredients, category, nutrition, duration)


def handle_delete_recipe(df, worksheet):
    """
    Handles the recipe deletion process within the application.

    This function allows the user to select a recipe to delete from the Google Sheet.
    The user can choose a recipe from a dropdown list, and if the recipe exists,
    it is displayed and can be deleted. Feedback is provided based on the success or failure
    of the deletion process.

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
        value_to_delete = search_recipes(df, delete_input)
        if not value_to_delete.empty:
            st.write(value_to_delete)
            if st.button('Löschen'):    
                delete_recipe(worksheet, delete_input) 
        else:
            st.write('Kein Rezept gefunden, bitte überprüfe deine Eingabe!')
