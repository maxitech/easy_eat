def search_recipes(df, search_params):
    """
    Searches for recipes in the DataFrame that match the given search parameters.

    Params:
        df (pandas.DataFrame): The DataFrame containing recipe data.
        search_params (str): A string of search terms separated by spaces.

    Returns:
        pandas.DataFrame: A DataFrame containing the recipes that match the search terms.
    """
    search_terms = search_params.split()
    
    for term in search_terms:
        df = df[df.apply(lambda row: row.astype(str).str.contains(term, case=False, na=False).any(), axis=1)]
    return df