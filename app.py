from streamlit_folium import folium_static
from next_restaurant.german_to_english import german_to_english
from next_restaurant.cuisine_info import cuisine_num_wise, cuisine_most_frequent, cuisine_num_wise_clean_data_frame_capitalise
from next_restaurant.parameters import *
from next_restaurant.functions_for_df import *

import streamlit as st
import folium
import pandas as pd
import geocoder
import seaborn as sns
import matplotlib.pyplot as plt

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

df = pd.read_csv("raw_data//clean_dataframe.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Converting the cuisine name to english
df["food_type_1_english"] = df["food_type"].str.capitalize()

# df_copy is for making second plot
df_copy = df.copy()

# Printing the dataframe
col2.dataframe(df.head())

# Basic info about the website
st.sidebar.markdown('''### I will help you to find best place in Berlin to open a restaurant.
Thank you
''')

st.sidebar.subheader("Frequent restaurants")
# Selecting options
options = st.sidebar.selectbox('Select a type of a restaurant',
                                cuisine_num_wise_clean_data_frame_capitalise)

if options != "All":
    df = df[df["food_type_1_english"] == options]

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

# Conditions for generating maps
blue_popular = st.sidebar.checkbox("High reviews restaurants")
red_popular = st.sidebar.checkbox("Low reviews restaurants")

# Determining color based on popularity cutoff
df_copy["popularity_color"] = df_copy["user_ratings_total"].apply(lambda x: "red" if x < popularity_cutoff else "blue")

df_top_cuisine = df_copy.loc[df_copy["food_type_1_english"].isin(cuisine_most_frequent)]


# Count plot general
sns.set_theme(style="darkgrid")
fig, ax = plt.subplots()
ax = sns.countplot(x = "food_type_1_english",
                    data=df_top_cuisine,
                    order = df_top_cuisine["food_type_1_english"].value_counts().index)
ax.set_title("Food type")
#ax.set_label(False)
ax.xaxis.label.set_visible(False)
ax.set_xticklabels(ax.get_xticklabels(), rotation = 30)
col2.pyplot(fig)

# Heading for second map plot
col2.header('Distribution of restaurants in Berlin based on number of user reviews')

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

# Starting column 3
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
col3.dataframe(df["food_type"].value_counts())

#Input an address
user_input = col3.text_input("User local address input", "Koloniestrasse 36, Berlin")
g = geocoder.osm(user_input)

local_lat = g.osm["y"]
local_lng = g.osm["x"]

col3.write(f"Local lat: {local_lat}")
col3.write(f"Local lng: {local_lng}")

# n = folium.Figure(width=100, height=100)
o = map_instance(zoom=12, initial_location=[local_lat, local_lng],
                        width=300, height=300)

df_local = nearby_restaurants(df_copy, local_lat, local_lng)

# Determining color for ratings cutoff
df_local["ratings_color"] = df_local["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Making circles around the popularity and color coding it.
o = generating_circles(o, df_local, "ratings_color")

with col3:
    folium.LayerControl().add_to(o)
    folium_static(o)
