import pandas as pd
import math
import streamlit as st

# HOW TO USE#
""" 1. run the k_neighbours_df function with the data_df, the lat, lng of the choosen location and the number of restaurants to return
2. with the resulting df of the k_neighbours_df function run the calc_centers function to get the center of the bad and good centers
"""

# user_input = geocoder.osm('sonnenallee30')
# lat = user_input.latlng[0]
# lng = user_input.latlng[1]


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def deg_to_rad(deg):
    """
    Function to convert radians to degree.
    """
    return deg * (math.pi / 180)


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def distance(lat1, lng1, lat2, lng2):
    """
    This function is based on Haversine formula to estimate distance based
    on 2 sets of latitude and longitude
    a = sin²(ΔlatDifference/2) + cos(lat1).cos(lat2).sin²(ΔlonDifference/2)
    c = 2.atan2(√a, √(1−a))
    d = R.c
    """
    delta_lat = deg_to_rad(lat1 - lat2)
    delta_lng = deg_to_rad(lng1 - lng2)
    a = ((math.sin(delta_lat / 2)) * (math.sin(delta_lat / 2))) + (
        math.cos(deg_to_rad(lat1))
        * math.cos(deg_to_rad(lat2))
        * ((math.sin(delta_lng / 2)) * (math.sin(delta_lng / 2)))
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # This is in km, and the results are also in Km
    d = R * c
    return d


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def k_neighbours_df(df, lat, lng, n_restaurants=20):
    """takes the df of restaurants and the lat,lng for the prefered user location and outputs a df of k nearest restaurants"""
    df["distance"] = ""
    for i in range(len(df)):
        df["distance"][i] = distance(lat, lng, df["lat"][i], df["lng"][i])
    return df.sort_values(by="distance")[:n_restaurants]


# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
def calc_centers(df, rating):
    """calculate the center of 'good' and 'bad' restaurants of the choosing location.
    Good and bad restaurants are decided based on the rating"""

    bad_rest = df[df["rating"] < rating]

    good_rest = df[df["rating"] >= rating]

    if len(bad_rest) == 0 and len(good_rest) == 0:
        return None
    elif len(bad_rest) == 0 and len(good_rest) != 0:
        center_good = (
            (good_rest["rating"] * good_rest["lat"]).sum() / good_rest["rating"].sum(),
            (good_rest["rating"] * good_rest["lng"]).sum() / good_rest["rating"].sum(),
        )
        return {"center_good": center_good}
    elif len(bad_rest) != 0 and len(good_rest) == 0:
        center_bad = (
            (bad_rest["rating"] * bad_rest["lat"]).sum() / bad_rest["rating"].sum(),
            (bad_rest["rating"] * bad_rest["lng"]).sum() / bad_rest["rating"].sum(),
        )
        return {"center_bad": center_bad}
    else:
        center_bad = (
            (bad_rest["rating"] * bad_rest["lat"]).sum() / bad_rest["rating"].sum(),
            (bad_rest["rating"] * bad_rest["lng"]).sum() / bad_rest["rating"].sum(),
        )
        center_good = (
            (good_rest["rating"] * good_rest["lat"]).sum() / good_rest["rating"].sum(),
            (good_rest["rating"] * good_rest["lng"]).sum() / good_rest["rating"].sum(),
        )
    return center_bad, center_good


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def neighbours_stats(df):
    """takes the k_neighbours_df and returns the most_frequent_price_leve, avg_rating , best_competitor(= rating * total No. of ratings) and the count of each cuisine in a dict"""
    price_dict = {
        "€": 1.0,
        "€€": 2.0,
        "€€€": 3.0,
        "€€€€": 4.0,
        "1.0": 1.0,
        "2.0": 2.0,
        "3.0": 3.0,
        "4.0": 4.0,
    }
    df.replace({"price_level": price_dict}, inplace=True)
    most_frq_price_level = df["price_level"].mode()
    most_frq_price_level = int(most_frq_price_level) * "€"
    avg_rating = df["rating"].mean()
    df["rating_total"] = df["rating"] * df["user_ratings_total"]

    # Making best competitor
    best_competitor_df = df[df["rating_total"] == df["rating_total"].max()]
    df_1 = pd.DataFrame.from_dict(best_competitor_df)
    df_1 = df_1.reset_index()
    best_competitor = df_1["names_clean"][0]
    # best_competitor = best_competitor.capitalise()
    cuisine_distribution = {}
    for i in df["food_type"].unique():
        cuisine_distribution[i] = df[df["food_type"] == i]["food_type"].count()

    percent_of_good_restaurants = round(
        len(df[df["ratings_color"] == "blue"]) * 100 / len(df)
    )
    percent_of_bad_restaurants = round(
        len(df[df["ratings_color"] == "orange"]) * 100 / len(df)
    )

    return (
        most_frq_price_level,
        avg_rating,
        best_competitor,
        cuisine_distribution,
        percent_of_good_restaurants,
        percent_of_bad_restaurants,
    )
