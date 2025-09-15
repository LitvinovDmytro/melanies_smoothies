# Import python packages
import streamlit as st
import pandas as pd
import requests
import pandas
from snowflake.snowpark.functions import col

# --- Streamlit UI ---
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# --- Snowflake Connection ---
cnx = st.connection("snowflake")
session = cnx.session()  # ✅ Call the session method

# --- Query available fruits ---
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()

# Collect data and convert to list
fruit_rows = my_dataframe.collect()
fruit_names = [row['FRUIT_NAME'] for row in fruit_rows]

# --- Multiselect for ingredients ---
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

# --- Handle user selection ---
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    for fruit_chosen in ingredients_list:
    # Try to find matching SEARCH_ON safely
    match = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
    
    if match.empty:  # ✅ No match found → skip
        st.warning(f"No SEARCH_ON value found for '{fruit_chosen}'. Skipping API call.")
        continue  # ✅ Go to next fruit

    search_on = str(match.iloc[0]).strip()

    st.write(f"The search value for {fruit_chosen} is {search_on}.")
   
    st.subheader(fruit_chosen + ' Nutrition information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
    st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
   
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


