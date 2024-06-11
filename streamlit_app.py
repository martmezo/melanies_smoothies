# Import python packages
import streamlit as st

# Write directly to the app
st.title("Customize your Smoothie!")
st.write(
    """Choose the fruits you want in your custom Smoothie.
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.snowflake()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! NAME_ON_ORDER', icon="✅")
