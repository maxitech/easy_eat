from recipes import load_recipe, handle_delete_recipe


df, worksheet = load_recipe()
handle_delete_recipe(df, worksheet)
