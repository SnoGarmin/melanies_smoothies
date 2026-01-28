# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session                       # Remove this line for Streamlit Not in Snowflake

#New section to display smoothiefroot nutrition information   API Requests
import requests


# To use a Snowpark COLUMN function named "col" we need to import it into our app
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.title(""" Choose the fruits you want in your custom Smoothie!""")

# Text Input Box
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")                                                 # This line for Streamlit Not in Snowflake
session = cnx.session()                                                          # This line for Streamlit Not in Snowflake

#Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 
#========================================================================
#session = get_active_session()                                                   # Remove this line for Streamlit Not in Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

# API Requests
#==============
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())


#st.write(ingredients_list)
#st.text(ingredients_list)

# if ingredients_list is not null: then do everything below this line that is indented. 
if ingredients_list:
 #st.write(ingredients_list)
 #st.text(ingredients_list)

 ingredients_string = ''

#which actually means...
#for each fruit_chosen in ingredients_list multiselect box: do everything below this line that is indented. 

 for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

 #st.write(ingredients_string)

# Build a SQL Insert Statement & Test It
 my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
 values ('""" + ingredients_string + """','""" + name_on_order + """')"""

 #st.write(my_insert_stmt)
 #st.stop()

 time_to_insert = st.button('Submit Order')

 if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")








    
