from folium.plugins import HeatMap
from next_restaurant.parameters import zoom, Berlin_center, width, height, radius

import streamlit as st
import math
import pandas as pd
import ast
import folium

"""
In this module we make functions which can be used to transform data frames
"""
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_lat_lng(df: pd.DataFrame):
    """
    This function let us to add a log and lng columns un a DataFrame bease on it's geometry column.
    """
    lat = []
    lng = []
    for i in range(len(df)):
        try:
            lat.append(ast.literal_eval(df.geometry.iloc[i])['location']['lat'])
            lng.append(ast.literal_eval(df.geometry.iloc[i])['location']['lng'])
        except Exception:
            pass
    df['lng'] = lng
    df['lat'] = lat
    return df

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_popularity(pop):
    return pop

# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_map_instance(zoom = zoom, initial_location=Berlin_center, width=width, height=height):
    """making a general map with different folium loayers"""
    # First map, focused on the ratings of the restaurant
    m = folium.Map(width=width, height=height, location=initial_location,
               tiles = "Stamen Toner",
               zoom_start=zoom,
               control_scale=True,
               prefer_canvas=True)

    folium.TileLayer('stamentoner').add_to(m)
    folium.TileLayer('stamenwatercolor').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('openstreetmap').add_to(m)
    folium.LayerControl().add_to(m)
    return m

# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
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

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def adding_heatmap(m, data):
    """making a heatmap of data with lng, lat and data"""
    HeatMap(data=data, radius=10, blur = 0,
            min_opacity = 1, max_val = 0.01,
            gradient={0: "blue", 0.5: "lime",
                        0.7: "red", 0.9: "orange"}).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
    folium.LayerControl().add_to(m)
    return m

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_deg_to_rad(deg):
    """
    Function to convert radians to degree.
    """
    return deg * (math.pi/180)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_distance(lat1 = 40.7128, lng1 = 35.6895,
             lat2 = 74.0060, lng2 = 139.6917):
    """
    This function is based on Haversine formula to estimate distance based
    on 2 sets of latitude and longitude
    a = sin²(ΔlatDifference/2) + cos(lat1).cos(lat2).sin²(ΔlonDifference/2)
    c = 2.atan2(√a, √(1−a))
    d = R.c
    """
    delta_lat = deg_to_rad(lat1-lat2)
    delta_lng = deg_to_rad(lng1-lng2)

    a = ((math.sin(delta_lat/2))*(math.sin(delta_lat/2))) + (math.cos(deg_to_rad(lat1))
                                        *math.cos(deg_to_rad(lat2))
                                        *((math.sin(delta_lng/2))*(math.sin(delta_lng/2))))

    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    R = 6371 # This is in km, and the results are also in Km
    d = R*c
    return d

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def nearby_restaurants(df, lat, lng, range_in_km = 2):
    """
    This function gives the restaurant near a coordinate point and withing the range in km.
    Default range is 2 KM
    """
    df_copy = df.copy()
    df_copy["distance"] = df["lng"]
    #print(df_copy.head())
    for i in range(len(df_copy["distance"])):
        df_copy["distance"][i] = distance(lat1=lat, lng1=lng, lat2 = df_copy["lat"][i], lng2 = df_copy["lng"][i])
    df_copy = df_copy[df_copy["distance"]<range_in_km]
    return df_copy


