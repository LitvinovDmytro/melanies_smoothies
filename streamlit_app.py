# Import python packages
import streamlit as st
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Collect data and convert to list
fruit_rows = my_dataframe.collect()
fruit_names = [row['FRUIT_NAME'] for row in fruit_rows]

# Optional: show table in the app
st.dataframe(pd.DataFrame(fruit_rows), use_container_width=True)

# --- Multiselect for ingredients ---
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_names,
    max_selections=5
)

# --- Handle user selection ---
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

# new section to display 
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefruit_response.json(), use_container_width=True)
