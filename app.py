from streamlit_folium import folium_static
from folium.plugins import HeatMap
from folium.plugins import HeatMapWithTime

import streamlit as st
import folium
import pandas as pd
import ast

# The title
st.title("Next Restaurant")

# Basic info about the website
st.markdown('''I will help you to find best place in Berlin to open a restaurant.
Thank you
''')

df = pd.read_csv("raw_data//Berlin_30500coor.csv")
# df = df.drop_duplicates(subset="name")
# import openrouteservice
# import json
# import datetime
# import geocoder
# import requests

lat = []
lng = []

for i in range(len(df)):
    try:
        lat.append(ast.literal_eval(df.geometry.iloc[i])['location']['lat'])
        lng.append(ast.literal_eval(df.geometry.iloc[i])['location']['lng'])
    except:
        pass

df['lng'] = lng
df['lat'] = lat

# df["lat"] = df["geometry"]
# df["lng"] = df["geometry"]
st.write(df.head())
st.write(df.tail())
#st.write(df.info())

# def lat(geometry: dict):
#     lat = geometry["location"]["lat"]
#     return float(lat)

# def lng(geometry: dict):
#     lng = geometry["location"]["lng"]
#     return float(lng)

# df["lat"] = df["geometry"].apply(lat)
# df["lng"] = df["geometry"].apply(lng)

heatmap_ratings_data = df[["lat", "lng", "rating"]]


CSS = """
h1 {
    color: red;
}
.stApp {
    background-image: url(https://avatars1.githubusercontent.com/u/9978111?v=4);
    background-size: cover;
}
"""

if st.checkbox('Inject CSS'):
    st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

# Making sure if the inputs are coordinates or proper address
input_type = st.radio("Select a type of a restaurant", ('Italian', 'Indian', 'Turkish', 'French'))

#initial_address = st.text_input("Starting point", "New York")
if input_type == "Italian":
    st.write("The intitial choice is Italian")

# Defining number of people for the ride.
number_of_people = st.slider('How many people will come to the restaurant', 1, 10, 3)

Berlin_center = {'lat': 52.52000659999999, 'lng': 13.404954}
# Starting point
m = folium.Map(location=[52.5200066, 13.404954],
                tiles = "Stamen Toner",
                zoom_start=14)

# add marker to intial address
tooltip = "Liberty Bell"
folium.Marker(
    [52.52000659999999, 13.404954], color='blue', popup="City center", tooltip=tooltip
).add_to(m)

folium.Circle(
    location=[52.52000659999999, 13.404954],
    #popup=data.iloc[i]['name'],
    radius=10000,
    color='black',
    fill=True,
    fill_color='blue'
    ).add_to(m)

gradient = {1: 'purple',
            2: 'purple',
            3: 'purple',
            4: 'red',
            5: 'red'}

HeatMap(data=heatmap_ratings_data, radious=12, max_zoom=12).add_to(m)

<<<<<<< HEAD
st.markdown('''## The next restaurant project''')
=======
folium_static(m)
>>>>>>> 4b43bb9b331c4ef67240f42c1d88e84b5f8e4808
