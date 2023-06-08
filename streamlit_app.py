import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError


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


# Define function 
def get_fruitvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


# Make API call, parse out json
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get more information.")
  else: 
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
     # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
     # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    
      
except URLError as e:
  streamlit.error()

  #streamlit.write('The user entered ', fruit_choice

# Query Snowflake
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
 
# Add button to load list 
if streamlit.button('Get Fruit Load List:'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
#streamlit.write('Thanks for choosing ', add_fruit)


def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlit')")
    return "Thanks for adding " + new_fruit
  
  add_fruit = streamlit.text_input('What fruit would you like to add?')
  if streamlit.button('Add a fruit to the list:'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(new_fruit)
    streamlit.text(back_from_function)
  
#stop command
streamlit.stop()

