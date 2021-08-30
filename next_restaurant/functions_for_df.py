
from folium.plugins import HeatMap
from next_restaurant.parameters import *

import pandas as pd
import ast
import folium

"""
In this module we make functions which can be used to transform data frames
"""

def getting_lat_lng(df: pd.DataFrame):
    """
    This function let us to add a log and lng columns un a DataFrame bease on it's geometry column.
    """
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
    return df

def popularity(pop):
    return pop


def map_instance():
    """making a general map with different folium loayers"""
    # First map, focused on the ratings of the restaurant
    m = folium.Map(width=width, height=height, location=Berlin_center,
               tiles = "Stamen Toner",
               zoom_start=zoom,
               control_scale=True,
               prefer_canvas=True)

    folium.TileLayer('stamentoner').add_to(m)
    folium.TileLayer('stamenwatercolor').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('openstreetmap').add_to(m)

    return m

def generating_circles(m, df, color: str):
    for i in range(len(df)):
            # address = df.iloc[i]["full_address"]
            folium.Circle(
                location=[df.iloc[i]["lat"], df.iloc[i]["lng"]],
                #popup=data.iloc[i]['name'],
                radius=radius,
                color=df.iloc[i][color],
                popup=df.iloc[i]["full_address"],
                tooltip="Click for name and address info",
                fill=True,
                fill_color=df.iloc[i][color]
                ).add_to(m)
    return m

def adding_heatmap(m, data):
    """making a heatmap of data with lng, lat and data"""
    HeatMap(data=data, radius=10, blur = 0,
            min_opacity = 1, max_val = 0.01,
            gradient={0: "blue", 0.5: "lime",
                        0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    folium.LayerControl().add_to(m)
    return m


def background():
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

    # if col2.checkbox('Inject CSS'):
#     st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)
