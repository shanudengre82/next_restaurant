from streamlit_folium import folium_static
from next_restaurant.german_to_english import german_to_english
from next_restaurant.cuisine_info import *
from next_restaurant.local_search_coordinates import generating_circular_coordinates, locating_best_place_based_on_distance
from next_restaurant.parameters import *
from next_restaurant.functions_for_df import *
from next_restaurant.suggestion_feature import k_neighbours_df, calc_centers

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

# The title
st.title("Next Restaurant")

# making columns
# col2, col3 = st.columns([2, 1])

df = pd.read_csv("raw_data//clean_dataframe_1.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Converting the cuisine name to english
df["food_type_1_english"] = df["food_type"].str.capitalize()

# df_copy is for making second plot
df_copy = df.copy()

# Printing the dataframe
# st.dataframe(df.head())

# Basic info about the website
st.sidebar.markdown('''## I will help you to find best place in Berlin to open a restaurant.''')

# Selecting foodtype options
st.sidebar.subheader("Do you have a food type in mind?")
options = st.sidebar.selectbox("", cuisine_num_wise_clean_data_frame_capitalise)
if options != "All":
    df = df[df["food_type_1_english"] == options]

# Selecting district options
st.sidebar.subheader("Do you have a district in mind?")
options_district = st.sidebar.selectbox('', district_list)
if options_district != "All":
    df = df[df["district"] == options_district]

# making first map
m = map_instance()

# Making a sub header
st.subheader('Distribution of restaurants in Berlin based on rating and user reviews number cutoff')

# Adding a geojson layer
# folium.GeoJson('raw_data//neighbourhoods.geojson', name='Berlin neighbourhood').add_to(m)

# Selecting district options
st.sidebar.subheader("Would you like to just explore?")
# user rating cutoff
# st.sidebar.markdown("Rating cutoff")
rating_cutoff = st.sidebar.slider('Rating cutoff',
                            min_value = 2.,
                            max_value = 5.,
                            step=0.1,
                            value = 4.)

# Determining color for ratings cutoff
df["ratings_color"] = df["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# user popularity cutoff
# st.sidebar.markdown("User reviews number cutoff")
popularity_cutoff = st.sidebar.slider("User reviews number cutoff",
                            min_value = 0,
                            max_value = 2000,
                            step=1,
                            value = 0)

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

# with col2:
folium.LayerControl().add_to(m)
folium_static(m)

# Making list of clean cuisine for global choices
cuisine_list = df["food_type_1_english"].value_counts().index.tolist()
cuisine_list = [i for i in cuisine_list if i not in cuisine_clean_data_frame_to_remove]

df_top_cuisine = df.loc[df["food_type_1_english"].isin(cuisine_list[0:10])]
if len(cuisine_list) < 10:
    df_top_cuisine = df_top_cuisine.loc[df_top_cuisine["food_type_1_english"].isin(cuisine_list)]
else:
    df_top_cuisine = df_top_cuisine.loc[df_top_cuisine["food_type_1_english"].isin(cuisine_list[0:10])]

# Count plot general
# Heading for second map plot
if options_district == "All":
    st.subheader('Popular cusines in Berlin')
else:
    st.subheader(f'Popular cusines in {options_district}')

sns.set_theme(style="darkgrid")
fig, ax = plt.subplots()
ax = sns.countplot(x = "food_type_1_english",
                    data=df_top_cuisine,
                    order = df_top_cuisine["food_type_1_english"].value_counts().index)
# ax.set_title("Food type")
ax.xaxis.label.set_visible(False)
ax.set_xticklabels(ax.get_xticklabels(), rotation = 45)
st.pyplot(fig)

# Selecting an address
st.sidebar.subheader("Do you have an address in mind?")
if options_district == "All":
    user_input = st.sidebar.text_input("", "Mitte, Berlin")
else:
    user_input = st.sidebar.text_input("", "Koloniestrasse 36, Berlin")
g = geocoder.osm(user_input)

# Number of restaurants to be considered locally
number_of_nearby_restaurant_to_be_considered = st.sidebar.slider('number_of_nearby_restaurant_to_be_considered',
                            min_value = 5,
                            max_value = 100,
                            step=5,
                            value = 20)

local_lat = g.osm["y"]
local_lng = g.osm["x"]

st.sidebar.markdown("Coordinates corresponding to the address")
st.sidebar.write(f"Local lat: {local_lat}")
st.sidebar.write(f"Local lng: {local_lng}")

df_local = k_neighbours_df(df_copy, local_lat, local_lng, n_restaurants=number_of_nearby_restaurant_to_be_considered)

# Determining color for ratings cutoff
df_local["ratings_color"] = df_local["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Chopping data frame with respect to popularity cutoff
df_local = df_local[df_local["user_ratings_total"]>popularity_cutoff]

# Making a subheader for local search plot
st.subheader('Distribution of restaurants locally based on rating and user reviews number cutoff')
# Making a map for local data
o = map_instance(zoom=15, initial_location=[local_lat, local_lng],
                        width=width, height=height)

# Making circles around the popularity and color coding it.
o = generating_circles(o, df_local, "ratings_color")

# Estimating centroid bad and centroid good
center_bad, center_good = calc_centers(df_local, rating_cutoff)

# Making a suggestion based on good center and bad center
suggested_lat = (0.9)*center_bad[0] + (0.1)*center_good[0]
suggested_lng = (0.9)*center_bad[1] + (0.1)*center_good[1]

# number of suggestions based on distance
# st.sidebar.markdown("Rating cutoff")
suggestion_number_distance = st.slider('Number of suggestions based on distance',
                            min_value = 1,
                            max_value = 10,
                            step=1,
                            value = 1)

# Dataframe with just latitudes and longitutes. They are to generate suggestions.
df_local_lat_lng = df_local[["lat", "lng", "distance"]]
# st.dataframe(df_local_lat_lng.head())

# Coordinates inside a local box
local_box = generating_circular_coordinates(df = df_local_lat_lng,
                                            lat = local_lat,
                                            lng = local_lng)
# st.write(len(local_box))

best_location_based_on_distance_list = []
for i in range(suggestion_number_distance):
    # st.write(i)
    best_location_based_on_distance = locating_best_place_based_on_distance(box = local_box, df = df_local_lat_lng)
    best_location_based_on_distance_list.append(best_location_based_on_distance)
    to_append = [best_location_based_on_distance[0], best_location_based_on_distance[1], 0]
    df_local_lat_lng.loc[len(df_local_lat_lng.index)] = to_append

# st.write(f"{suggested_lat}, {suggested_lng}")
# st.write(f"{best_location_based_on_distance}")
# with col3:
# folium.Marker([suggested_lat, suggested_lng]).add_to(o)

folium.Marker(location=[center_bad[0], center_bad[1]],
              popup="Rating waited centeroid for less rated restarants",
              icon=folium.Icon(color="red")).add_to(o)


folium.Marker([center_good[0], center_good[1]],
              popup="Rating waited centeroid for high rated restarants",
              icon=folium.Icon(color="darkblue")).add_to(o)

for i in best_location_based_on_distance_list:
    number = 1
    folium.Marker(i,
                popup=f"Optimum location number {number} based on distance from nearest neighbour restaurant",
                icon=folium.Icon(color="darkgreen")).add_to(o)
    number+=1

folium.LayerControl().add_to(o)
folium_static(o)

# Making list of clean cuisine for local choices
cuisine_list_local = df_local["food_type_1_english"].value_counts().index.tolist()
cuisine_list_local = [i for i in cuisine_list_local if i not in cuisine_clean_data_frame_to_remove]

if len(cuisine_list_local) < 10:
    df_top_cuisine_local = df_local.loc[df_local["food_type_1_english"].isin(cuisine_list_local)]
else:
    df_top_cuisine_local = df_local.loc[df_local["food_type_1_english"].isin(cuisine_list_local[0:10])]

fig, ax1 = plt.subplots()
ax1 = sns.countplot(x = "food_type_1_english",
                    data=df_top_cuisine_local,
                    order = df_top_cuisine_local["food_type_1_english"].value_counts().index)

# for p in ax1.patches:
#     ax1.annotate('%{:.1f}'.format(p.get_height()), (p.get_x()+0.1, p.get_height()+50))

st.subheader(f'Popular cusines locally')
# ax.set_title("Food type")
# ax.set_label(False)
ax1.xaxis.label.set_visible(False)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 30)
st.pyplot(fig)

st.header("Global and local area comparision")
