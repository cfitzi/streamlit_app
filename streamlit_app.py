import streamlit
import pandas 

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
