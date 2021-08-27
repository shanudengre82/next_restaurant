from streamlit_folium import folium_static
from folium.plugins import HeatMap
from next_restaurant.german_to_english import german_to_english
from next_restaurant.cuisine_info import cuisine_num_wise

import streamlit as st
import folium
import pandas as pd

# import ast
# import time
# import openrouteservice
# import json
# import datetime
# import geocoder
# import requests

# st.set_option('wideMode' , True)
# Setting the page layout to be wide
st.set_page_config(page_title="Next Restaurant",
                   initial_sidebar_state='expanded')


# making columns
col2, col3 = st.columns([2, 1])

df = pd.read_csv("raw_data//second_merge.csv")

# df2 = pd.read_csv("raw_data//Berlin_restaurant_5000.csv")
# df = df.drop_duplicates(subset="name")

# df["food_type_english"] = df["food_type_english"]
# lat = []
# lng = []

# for i in range(len(df2)):
#     try:
#         lat.append(ast.literal_eval(df2.geometry.iloc[i])['location']['lat'])
#         lng.append(ast.literal_eval(df2.geometry.iloc[i])['location']['lng'])
#     except:
#         pass

# df2['lng'] = lng
# df2['lat'] = lat

def popularity(pop):
    return int(pop/20)+1

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Converting the cuisine name to english
df["food_type_1_english"] = df["food_type"].apply(german_to_english)

# Making a list for a first cuisine type
# cuisine_tuple = tuple(df["food_type_1_english"].value_counts().index.tolist())
# st.write(cuisine_tuple)

# df2["popularity_res"] = df2["user_ratings_total"].apply(popularity)
# heatmap_ratings_data = df[["lat", "lng", "rating"]]
# heatmap_populatity_data = df[["lat", "lng", "popularity_res"]]

# Make dataframe smaller
# df = df.head(500)

# Printing the dataframe
# col2.dataframe(df.head())

# Basic info about the website
st.sidebar.markdown('''### I will help you to find best place in Berlin to open a restaurant.
Thank you
''')

# Selecting options
options = st.sidebar.selectbox('Select a type of a restaurant',
                            cuisine_num_wise)

if options != "All":
    df = df[df["food_type_1_english"] == options]

# Making sure if the inputs are coordinates or proper address
# input_type = st.sidebar.radio("Select a type of a restaurant", cuisine_num_wise)

#initial_address = st.text_input("Starting point", "New York")
# if input_type == "Italian":
#     st.sidebar.write("The intitial choice is Italian")

# Making a background
CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://avatars1.githubusercontent.com/u/9978111?v=4);
    background-size: cover;
}
"""

# The title
col2.title("Next Restaurant")

# if col2.checkbox('Inject CSS'):
#     st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# Starting point
# Berlin_center = [52.5200066, 13.404954]
Berlin_center = [52.5, 13.404954]

# Making a map
# f = folium.Figure(width=500, height=500)
width = 500
height = 500
zoom = 11

# defining gradient for heatmaps
gradient = {0.2: 'purple',
            0.4: 'purple',
            0.6: 'purple',
            0.8: "orange",
            1: 'orange'}

# col2.write('Getting all restaurants in Berlin')

col2.header('Distribution of restaurants in Berlin based on ratings')
# First map, focused on the ratings of the restaurant
m = folium.Map(width=width, height=height, location=Berlin_center,
               tiles = "Stamen Toner",
               zoom_start=zoom)

# add marker to intial address
# tooltip = "Liberty Bell"
# folium.Marker(Berlin_center, color='blue', popup="City center", tooltip=tooltip).add_to(m)

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

df = df[df["user_ratings_total"]>popularity_cutoff]

# user popularity color
df["popularity_color"] = df["popularity_res"].apply(lambda x: "red" if x < popularity_cutoff else "blue")

# Adding checkboxes for layers
# Conditions for generating maps
red_ratings = st.sidebar.checkbox("Select only low rated restaurant")
blue_ratings = st.sidebar.checkbox("Select only high rated restaurant")
# heat_map_rating = col2.checkbox("Would you lie to see a heatmap")

if red_ratings and blue_ratings:
    for i in range(len(df)):
        folium.Circle(
            location=[df.iloc[i]["lat"], df.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color=df.iloc[i]["ratings_color"],
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(m)

    # if heat_map_rating:
    #     HeatMap(data=heatmap_ratings_data, radius=10, blur = 0,
    #             min_opacity = 1, max_val = 0.01,
    #             gradient={0: "blue", 0.5: "lime",
    #                     0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    #     folium.LayerControl().add_to(m)

elif red_ratings and not blue_ratings:
    df_red = df[df["ratings_color"] == "red"]
    heatmap_red_ratings = df_red[["lat", "lng", "rating"]]

    # col2.checkbox("Great", value = True)
    # Making circles around the ratings and color coding it.
    for i in range(len(df_red)):
        folium.Circle(
            location=[df_red.iloc[i]["lat"], df_red.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color="red",
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(m)

    # if heat_map_rating:
    #     HeatMap(data=heatmap_red_ratings, radius=10, blur = 0,
    #             min_opacity = 1, max_val = 0.01,
    #             gradient={0: "blue", 0.5: "lime",
    #                       0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    #     folium.LayerControl().add_to(m)

elif blue_ratings and not red_ratings:
    df_blue = df[df["ratings_color"] == "blue"]
    heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]

    # col2.checkbox("Great", value = True)
    # Making circles around the ratings and color coding it.
    for i in range(len(df_blue)):
        folium.Circle(
            location=[df_blue.iloc[i]["lat"], df_blue.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color="blue",
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(m)

    # if heat_map_rating:
    #     HeatMap(data=heatmap_blue_ratings, radius=10, blur = 0,
    #             min_opacity = 1, max_val = 0.01,
    #             gradient={0: "blue", 0.5: "lime",
    #                     0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    #     folium.LayerControl().add_to(m)

else:
    for i in range(len(df)):
        folium.Circle(
            location=[df.iloc[i]["lat"], df.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color=df.iloc[i]["ratings_color"],
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(m)

    # if heat_map_rating:
    #     HeatMap(data=heatmap_ratings_data, radius=10, blur = 0,
    #             min_opacity = 1, max_val = 0.01,
    #             gradient={0: "blue", 0.5: "lime",
    #                     0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    #     folium.LayerControl().add_to(m)

with col2:
    folium_static(m)

col2.header('Distribution of restaurants in Berlin based on number of user reviews')


# Conditions for generating maps
blue_popular = st.sidebar.checkbox("Popular restaurant")
red_popular = st.sidebar.checkbox("Not so popular restaurant")


# n = folium.Figure(width=100, height=100)
n = folium.Map(width=width, height=height, location=Berlin_center,
                tiles = "Stamen Toner",
                zoom_start=zoom)

if red_popular and blue_popular:
# Making circles around the popularity and color coding it.
    for i in range(len(df)):
        folium.Circle(
            location=[df.iloc[i]["lat"], df.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color=df.iloc[i]["popularity_color"],
            #fill=True,
            #fill_color=df.iloc[i]["popularity_color"]
            ).add_to(n)

    # HeatMap(data=heatmap_populatity_data,
    #         radius=20,
    #         gradient=gradient,
    #         max_zoom=10).add_to(folium.FeatureGroup(name='Heat Map').add_to(n))
    # folium.LayerControl().add_to(n)

elif blue_popular and not red_popular:
    df_blue = df[df["popularity_color"] == "blue"]
    for i in range(len(df_blue)):
        folium.Circle(
            location=[df_blue.iloc[i]["lat"], df_blue.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color="blue",
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(n)

elif red_popular and not blue_popular:
    df_red = df[df["popularity_color"] == "red"]
    for i in range(len(df_red)):
        folium.Circle(
            location=[df_red.iloc[i]["lat"], df_red.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color="red",
            # fill=True,
            # fill_color=df.iloc[i]["ratings_color"]
            ).add_to(n)

else:
    for i in range(len(df)):
        folium.Circle(
            location=[df.iloc[i]["lat"], df.iloc[i]["lng"]],
            #popup=data.iloc[i]['name'],
            radius=20,
            color=df.iloc[i]["popularity_color"],
            #fill=True,
            #fill_color=df.iloc[i]["popularity_color"]
            ).add_to(n)

with col2:
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
# col3.dataframe(df["food_type_1_english"].value_counts())
