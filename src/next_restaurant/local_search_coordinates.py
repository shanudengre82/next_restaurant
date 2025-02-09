from next_restaurant.functions_for_df import get_distance

import numpy as np
import streamlit as st


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def generating_circular_coordinates(df, lat=52.5607405, lng=13.3808273, radius=100):
    """
    This function generates coordinates to search for best location
    based on being far from the restaurants.
    """
    # # Making a distance column in the df
    # df["distance"] = df["lat"]
    # for i in range(len(df["distance"])):
    #     df["distance"][i] = distance(lat1=lat, lng1=lng, lat2 = df["lat"][i], lng2 = df["lng"][i])

    # Selecting inly latitudes and longitudes
    df = df[df["distance"] == df["distance"].max()][["lat", "lng"]]

    lat_max = df.iloc[0]["lat"]
    lng_max = df.iloc[0]["lng"]
    # print(lat_max, lng_max)
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

    # print(lat_distance, lng_distance)

    box_coordinates_inside = []

    for i in np.linspace(box_coordinates[0][0], box_coordinates[2][0], lat_divisions):
        for j in np.linspace(
            box_coordinates[0][1], box_coordinates[3][1], lng_divisions
        ):
            box_coordinates_inside.append([i, j])

    box_sorted = []

    distance_max = get_distance(lat1=lat_max, lat2=lat, lng1=lng_max, lng2=lng)
    for i in box_coordinates_inside:
        distance = get_distance(lat1=lat, lat2=i[0], lng1=lng, lng2=i[1])
        if distance < 2 * distance_max / 3:
            box_sorted.append(i)
    return box_sorted


@st.cache(suppress_st_warning=True, allow_output_mutation=False)
def get_locating_best_place_based_on_distance(df, box: list):
    """
    This function looks for the farthest possible place with respect to
    the nearest neighbouring restaurant.
    """
    df_list = []
    for i in box:
        count = []
        for j in range(len(df)):
            distance = get_distance(
                lat1=df.iloc[j]["lat"], lat2=i[0], lng1=df.iloc[j]["lng"], lng2=i[1]
            )
            count.append(distance)
        df_list.append(min(count))
    return box[df_list.index(max(df_list))]
