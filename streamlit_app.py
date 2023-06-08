import streamlit
import pandas 
import requests
import snowflake.connector


streamlit.title("My parent's new fancy diner")
streamlit.header("Breakfast Menu") 
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")   
streamlit.text("🥗 Kale, Spinach, and Rocket Smoothie")
streamlit.text("🐔 Hard-boiled free-range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Import csv
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Fruit picker, list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Show table
# streamlit.dataframe(my_fruit_list)

#Show only selected 
streamlit.dataframe(fruits_to_show)

# Make API call, parse out json
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Create and show dataframe for parsed data 
streamlit.dataframe(fruityvice_normalized)

# Query Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)


