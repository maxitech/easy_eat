import streamlit as st


def display_recipe(df):
    """
    Displays recipe details from a DataFrame.

    This function takes a DataFrame containing recipe information 
    and iterates through each row to display the details of each recipe, 
    such as the title, duration, category, ingredients, and preparation steps. 
    The details are shown using Streamlit components.

    Params:
        df (pd.DataFrame): DataFrame with columns 'Gericht', 'Dauer', 'Kategorie', 
                           'Zutaten', and 'Zubereitung', containing recipe details.

    Returns:
        None
    """
    for _, row in df.iterrows():
        st.title(row['Gericht'])
        st.subheader('Dauer:')
        st.write(row['Dauer'])
        st.subheader('Kategorie:')
        st.write(row['Kategorie'])
        st.subheader('Zutaten:')
        st.write(row['Zutaten'])
        st.subheader('Zubereitung:')
        st.write(row['Zubereitung'])
        st.markdown("---")