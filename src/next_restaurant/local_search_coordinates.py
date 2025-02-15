from next_restaurant.functions_for_df import get_distance

import numpy as np
import streamlit as st
import pandas as pd
from typing import List


@st.cache_data  # type: ignore
def get_coordinates_inside_box(
    box_coordinates: List[List[float]], lat_divisions: int, lng_divisions: int
) -> List[List[float]]:
    box_coordinates_inside: List[List[float]] = []

    for coordinate_lat in np.linspace(
        box_coordinates[0][0], box_coordinates[2][0], lat_divisions
    ):
        for coordinate_lng in np.linspace(
            box_coordinates[0][1], box_coordinates[3][1], lng_divisions
        ):
            box_coordinates_inside.append([coordinate_lat, coordinate_lng])
    return box_coordinates_inside


@st.cache_data  # type: ignore
def generating_circular_coordinates(
    df: pd.DataFrame,
    lat: float = 52.5607405,
    lng: float = 13.3808273,
    radius: int = 100,
) -> List[List[float]]:
    """
    This function generates coordinates to search for best location
    based on being far from the restaurants.
    """

    # Selecting inly latitudes and longitudes
    df = df[df["distance"] == df["distance"].max()][["lat", "lng"]]

    lat_max = df.iloc[0]["lat"]
    lng_max = df.iloc[0]["lng"]
    box_coordinates = []
    box_coordinates.append([lat_max, lng_max])  # first extreme
    box_coordinates.append(
        [lat + (lat - lat_max), lng + lng - lng_max]
    )  # opposite to first
    box_coordinates.append([lat + (lat - lat_max), lng_max])  # opposite to first
    box_coordinates.append([lat_max, lng + lng - lng_max])  # opposite to second

    lat_distance = get_distance(
        lat1=box_coordinates[0][0],
        lat2=box_coordinates[2][0],
        lng1=box_coordinates[0][1],
        lng2=box_coordinates[2][1],
    )

    lng_distance = get_distance(
        lat1=box_coordinates[0][0],
        lat2=box_coordinates[3][0],
        lng1=box_coordinates[0][1],
        lng2=box_coordinates[3][1],
    )

    lat_divisions = int(lat_distance * 1000 / radius) + 1
    lng_divisions = int(lng_distance * 1000 / radius) + 1

    box_coordinates_inside = get_coordinates_inside_box(
        box_coordinates=box_coordinates,
        lat_divisions=lat_divisions,
        lng_divisions=lng_divisions,
    )

    distance_max = get_distance(lat1=lat_max, lat2=lat, lng1=lng_max, lng2=lng)

    box_sorted: List[List[float]] = [
        box_coordinates
        for box_coordinates in box_coordinates_inside
        if get_distance(
            lat1=lat, lat2=box_coordinates[0], lng1=lng, lng2=box_coordinates[1]
        )
        < 2 * distance_max / 3
    ]
    return box_sorted


@st.cache_data  # type: ignore
def get_locating_best_place_based_on_distance(
    df: pd.DataFrame, boxes: List[List[float]]
) -> List[float]:
    """
    This function looks for the farthest possible place with respect to
    the nearest neighbouring restaurant.
    """
    df_list = []
    for coordinate in boxes:
        lat_box, lng_box = coordinate
        # Calculate the distance between each point in df and the coordinate in box using NumPy
        distances = np.sqrt((df["lat"] - lat_box) ** 2 + (df["lng"] - lng_box) ** 2)
        # Append the minimum distance to the result list
        df_list.append(distances.min())
    return boxes[df_list.index(max(df_list))]
