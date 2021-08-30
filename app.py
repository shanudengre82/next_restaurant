from streamlit_folium import folium_static
from next_restaurant.german_to_english import german_to_english
from next_restaurant.cuisine_info import cuisine_num_wise
from next_restaurant.parameters import *
from next_restaurant.functions_for_df import *

import streamlit as st
import folium
import pandas as pd
import json
import branca

# import ast
# import time
# import openrouteservice
# import json
# import datetime
# import geocoder
# import requests

# Setting the page layout to be wide
st.set_page_config(page_title="Next Restaurant",
                   initial_sidebar_state='expanded')

# making columns
col2, col3 = st.columns([2, 1])

df = pd.read_csv("raw_data//second_merge.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Converting the cuisine name to english
df["food_type_1_english"] = df["food_type"].apply(german_to_english)

# Printing the dataframe
col2.dataframe(df.head())

# Basic info about the website
st.sidebar.markdown('''### I will help you to find best place in Berlin to open a restaurant.
Thank you
''')

st.sidebar.subheader("Frequent restaurants")
# Selecting options
options = st.sidebar.selectbox('Select a type of a restaurant',
                                cuisine_num_wise)

if options != "All":
    df = df[df["food_type_1_english"] == options]

# df_copy is for making second plot
df_copy = df.copy()

#initial_address = st.text_input("Starting point", "New York")
# if input_type == "Italian":
#     st.sidebar.write("The intitial choice is Italian")

# The title
col2.title("Next Restaurant")

# making first map
m = map_instance()

# Making a sub header
col2.subheader('Distribution of restaurants in Berlin based on ratings')

# Adding a geojson layer
folium.GeoJson('raw_data//neighbourhoods.geojson', name='Berlin neighbourhood').add_to(m)

# user rating cutoff
rating_cutoff = st.sidebar.slider('Please select a rating cutoff',
                            min_value = 2.,
                            max_value = 5.,
                            step=0.1,
                            value = 4.)

# Determining color for ratings cutoff
df["ratings_color"] = df["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# df2["ratings_color"] = df2["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# user popularity cutoff
popularity_cutoff = st.sidebar.slider('Please select a popularity cutoff',
                            min_value = 0,
                            max_value = 2000,
                            step=1,
                            value = 10)

# Chopping data frame with respect to popularity cutoff
df = df[df["user_ratings_total"]>popularity_cutoff]

# Conditions for generating maps
blue_ratings = st.sidebar.checkbox("High rated restaurants")
red_ratings = st.sidebar.checkbox("Low rated restaurants")
# heat_map_rating = col2.checkbox("Would you lie to see a heatmap")

colorscale = branca.colormap.linear.PuRd_09.scale(0, 100000)
def style_function(feature):
    popularity_color = df["popularity_color"]
    return {
        "fillOpacity": 0.5,
        "weight": 0,
        "fillColor": "#black" if popularity_color is None else colorscale(popularity_color),
    }

if red_ratings and blue_ratings:
    m = generating_circles(m, df, "ratings_color")

elif red_ratings and not blue_ratings:
    df_red = df[df["ratings_color"] == "red"]
    heatmap_red_ratings = df_red[["lat", "lng", "rating"]]
    m = generating_circles(m, df_red, "ratings_color")

elif blue_ratings and not red_ratings:
    df_blue = df[df["ratings_color"] == "blue"]
    heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]
    m = generating_circles(m, df_blue, "ratings_color")

else:
    m = generating_circles(m, df, "ratings_color")

with col2:
    folium.LayerControl().add_to(m)
    folium_static(m)

col2.header('Distribution of restaurants in Berlin based on number of user reviews')

# Conditions for generating maps
blue_popular = st.sidebar.checkbox("High reviews restaurants")
red_popular = st.sidebar.checkbox("Low reviews restaurants")

# Determining color based on popularity cutoff
df_copy["popularity_color"] = df_copy["user_ratings_total"].apply(lambda x: "red" if x < popularity_cutoff else "blue")

# n = folium.Figure(width=100, height=100)
n = map_instance()

if red_popular and blue_popular:
# Making circles around the popularity and color coding it.
    n = generating_circles(n, df_copy, "popularity_color")

elif blue_popular and not red_popular:
    df_blue_2 = df_copy[df_copy["popularity_color"] == "blue"]
    n = generating_circles(n, df_blue_2, "popularity_color")

elif red_popular and not blue_popular:
    df_red_2 = df_copy[df_copy["popularity_color"] == "red"]
    # heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]
    n = generating_circles(n, df_red_2, "popularity_color")

else:
    n = generating_circles(n, df_copy, "popularity_color")

with col2:
    folium.LayerControl().add_to(n)
    folium_static(n)

# Making column 3
# col3.metric(label="Active developers", value=123, delta=123, delta_color="off")

# # Selecting options
# options_2 = col3.multiselect('Select a different restaurant',
#                             ['Italian', 'Turkish', 'French'],
#                             ['French'])
# # Printing out the selection
# # st.write('You selected:', options)

# # Making sure if the inputs are coordinates or proper address
# input_type_2 = col3.radio("'Select a different restaurant'", ('Italian', 'Turkish', 'French'))

# #initial_address = st.text_input("Starting point", "New York")
# if input_type_2 == "Italian":
#     col3.write("The intitial choice is Italian")

# # Defining number of people for the ride.
# number_of_people_2 = col3.slider('How many are you', 1, 5, 3)

col3.header("Stats based on selections")
total_num_of_restaurants = len(df)
col3.text(f"Total number of restaurants")
col3.write(f"{total_num_of_restaurants}")

number_of_restaurant_with_high_ratings = len(df[df["ratings_color"] == "blue"])
col3.text(f"Restaurants with ratings > {rating_cutoff} ")
col3.write(f"{number_of_restaurant_with_high_ratings}")

number_of_restaurant_with_low_ratings = len(df[df["ratings_color"] == "red"])
col3.text(f"Restaurants with ratings < {rating_cutoff} ")
col3.write(f"{number_of_restaurant_with_low_ratings}")

# col3.dataframe(df["popularity_color"].value_counts())
# col3.dataframe(df["ratings_color"].value_counts())
col3.dataframe(df["food_type_1_english"].value_counts())
