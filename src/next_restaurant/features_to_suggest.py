import pandas as pd
import streamlit as st
from typing import Tuple, Optional, Any

from next_restaurant.functions_for_df import get_distance

# HOW TO USE#
""" 1. run the k_neighbours_df function with the data_df, the lat, lng of the choosen location and the number of restaurants to return
2. with the resulting df of the k_neighbours_df function run the calc_centers function to get the center of the bad and good centers
"""

# user_input = geocoder.osm('sonnenallee30')
# lat = user_input.latlng[0]
# lng = user_input.latlng[1]


@st.cache_data  # type: ignore
def k_neighbours_df(
    df: pd.DataFrame, lat: float, lng: float, n_restaurants: int = 20
) -> pd.DataFrame:
    """takes the df of restaurants and the lat,lng for the prefered user location and outputs a df of k nearest restaurants"""
    df["distance"] = df.apply(
        lambda row: get_distance(lat1=row["lat"], lat2=lat, lng1=row["lng"], lng2=lng),
        axis=1,
    )
    return df.sort_values(by="distance")[:n_restaurants]


# TODO: To optimise function for proper mypy return type, perhaps split the function
@st.cache_data  # type: ignore
def calc_centers(df: pd.DataFrame, rating: float) -> Any:
    """calculate the center of 'good' and 'bad' restaurants of the choosing location.
    Good and bad restaurants are decided based on the rating"""

    bad_rest = df[df["rating"] < rating]

    good_rest = df[df["rating"] >= rating]

    def calculate_center(restaurants: pd.DataFrame) -> Optional[Tuple[float, float]]:
        if len(restaurants) == 0:
            return None
        weighted_lat = (restaurants["rating"] * restaurants["lat"]).sum() / restaurants[
            "rating"
        ].sum()
        weighted_lng = (restaurants["rating"] * restaurants["lng"]).sum() / restaurants[
            "rating"
        ].sum()
        return weighted_lat, weighted_lng

    # Calculate centers for good and bad restaurants
    center_good = calculate_center(good_rest)
    center_bad = calculate_center(bad_rest)

    if center_good is None and center_bad is None:
        return None

    result = {}
    if center_good is not None:
        result["center_good"] = center_good
    if center_bad is not None:
        result["center_bad"] = center_bad

    return result


@st.cache_data  # type: ignore
def neighbours_stats(
    df: pd.DataFrame,
) -> Tuple[str, Any, Any, dict[Any, Any], int, int]:
    """takes the k_neighbours_df and returns the most_frequent_price_leve, avg_rating , best_competitor(= rating * total No. of ratings) and the count of each cuisine in a dict"""
    price_dict = {
        1.0: "€",
        2.0: "€€",
        3.0: "€€€",
        4.0: "€€€€",
    }
    df.replace({"price_level": price_dict}, inplace=True)
    most_frq_price_level = df["price_level"].dropna().mode()[0]

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
