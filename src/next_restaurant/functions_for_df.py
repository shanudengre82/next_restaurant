import ast
import math
from typing import List, Tuple

import folium
import pandas as pd
import streamlit as st
from folium.plugins import HeatMap

from next_restaurant.cuisine_info import CUISINE_OPTIONS, change_main_foodTypes
from next_restaurant.district import BERLIN_DISTRICTS
from next_restaurant.german_to_english import german_to_english
from next_restaurant.parameters import BERLIN_CENTER, INITIAL_RADIUS, WIDTH

"""
In this module we make functions which can be used to transform DataFrames
"""

COLUMNS_REQUIRED: List[str] = [
    "priceLevel",
    "rating",
    "userRatingsTotal",
    "lat",
    "lng",
    "namesClean",
    "fullAddress",
    "district",
    "foodType",
    "foodType2",
]


def preprocessing_df(df: pd.DataFrame) -> pd.DataFrame:
    # Updating dataframe
    df = df[COLUMNS_REQUIRED]
    df = german_to_english(df)

    # Capitalize foodTypes for the selection dropdown
    df = change_main_foodTypes(df)

    # selecting required cuisines
    df = df[df["foodType"].isin(CUISINE_OPTIONS)]
    return df


def update_df_based_on_selected_cusine_and_district(
    df: pd.DataFrame, cuisine: str, district: str
) -> pd.DataFrame:
    cuisine_list = [cuisine]
    if cuisine == "All":
        cuisine_list = CUISINE_OPTIONS

    district_list = [district]
    if district == "All":
        district_list = BERLIN_DISTRICTS

    df_cuisine_district = df[
        (df["foodType"].isin(cuisine_list)) & (df["district"].isin(district_list))
    ]
    return df_cuisine_district


@st.cache_data  # type: ignore
def get_lat_lng(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function let us to add a log and lng columns un a DataFrame bease on it's geometry column.
    """
    lat = []
    lng = []
    for i in range(len(df)):
        try:
            lat.append(ast.literal_eval(df.geometry.iloc[i])["location"]["lat"])
            lng.append(ast.literal_eval(df.geometry.iloc[i])["location"]["lng"])
        except Exception:
            pass
    df["lng"] = lng
    df["lat"] = lat
    return df


@st.cache_data  # type: ignore
def get_map_instance(
    zoom: int = INITIAL_RADIUS,
    initial_location: Tuple[float, float] = BERLIN_CENTER,
    width: int = WIDTH,
    height: int = WIDTH,
) -> folium.Map:
    """making a general map with different folium loayers"""
    # First map, focused on the ratings of the restaurant
    map_instance = folium.Map(
        width=width,
        height=height,
        location=tuple(initial_location),
        zoom_start=zoom,
        control_scale=True,
        prefer_canvas=True,
    )
    return map_instance


# @st.cache_data  # type: ignore
def generating_circles(map: folium.Map, df: pd.DataFrame, color: str) -> folium.Map:
    for _, row in df.iterrows():  # More efficient row iteration
        folium.Circle(
            location=[row["lat"], row["lng"]],  # Direct access
            radius=INITIAL_RADIUS,
            color=row[color],
            popup=row["fullAddress"],
            tooltip="Click for name and address info",
            fill=True,
            fill_color=row[color],
        ).add_to(map)
    return map


@st.cache_data  # type: ignore
def adding_heatmap(map: folium.Map, data: pd.DataFrame) -> folium.Map:
    """making a heatmap of data with lng, lat and data"""
    HeatMap(
        data=data,
        radius=10,
        blur=0,
        min_opacity=1,
        max_val=0.01,
        gradient={0: "blue", 0.5: "lime", 0.7: "red", 0.9: "orange"},
    ).add_to(folium.FeatureGroup(name="Heat Map").add_to(map))
    folium.LayerControl().add_to(map)
    return map


@st.cache_data  # type: ignore
def get_deg_to_rad(deg: float) -> float:
    """
    Function to convert radians to degree.
    """
    return deg * (math.pi / 180)


@st.cache_data  # type: ignore
def get_distance(
    lat1: float = 40.7128,
    lng1: float = 35.6895,
    lat2: float = 74.0060,
    lng2: float = 139.6917,
) -> float:
    """
    This function is based on Haversine formula to estimate distance based
    on 2 sets of latitude and longitude
    a = sin²(ΔlatDifference/2) + cos(lat1).cos(lat2).sin²(ΔlonDifference/2)
    c = 2.atan2(√a, √(1−a))
    d = R.c
    """
    delta_lat = get_deg_to_rad(lat1 - lat2)
    delta_lng = get_deg_to_rad(lng1 - lng2)

    a = ((math.sin(delta_lat / 2)) * (math.sin(delta_lat / 2))) + (
        math.cos(get_deg_to_rad(lat1))
        * math.cos(get_deg_to_rad(lat2))
        * ((math.sin(delta_lng / 2)) * (math.sin(delta_lng / 2)))
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    earth_radius = 6371  # This is in km, and the results are also in Km
    distance = earth_radius * c
    return distance


@st.cache_data  # type: ignore
def nearby_restaurants(
    df: pd.DataFrame, lat: float, lng: float, range_in_km: int = 2
) -> pd.DataFrame:
    """
    This function gives the restaurant near a coordinate point and withing the range in km.
    Default range is 2 KM
    """
    df_copy = df.copy()

    # Use vectorized operations to calculate the distance for each row
    df_copy["distance"] = df_copy.apply(
        lambda row: get_distance(lat1=lat, lng1=lng, lat2=row["lat"], lng2=row["lng"]),
        axis=1,
    )
    df_copy = df_copy[df_copy["distance"] < range_in_km]
    return df_copy
