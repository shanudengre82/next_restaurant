
from streamlit_folium import folium_static
import streamlit as st
import folium

# import openrouteservice
# import json
# import datetime
# import geocoder
# import requests

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


# The title
st.title("Next Restaurant")

# Basic info about the website
st.markdown('''I will help you to find best place in Berlin to open a restaurant.
Thank you
''')

# Making sure if the inputs are coordinates or proper address
input_type = st.radio("Select a type of a restaurant", ('Italian', 'Indian', 'Turkish', 'French'))

#initial_address = st.text_input("Starting point", "New York")
if input_type == "Italian":
    st.write("The intitial choice is Italian")

# Defining number of people for the ride.
number_of_people = st.slider('How many people will come to the restaurant', 1, 10, 3)

Berlin_center = {'lat': 52.52000659999999, 'lng': 13.404954}
# Starting point
m = folium.Map(location=[52.52000659999999, 13.404954], zoom_start=12)

# add marker to intial address
tooltip = "Liberty Bell"
folium.Marker(
    [52.52000659999999, 13.404954], color='blue', popup="City center", tooltip=tooltip
).add_to(m)

folium_static(m)
