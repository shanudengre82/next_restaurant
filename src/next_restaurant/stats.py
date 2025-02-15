import pandas as pd
import streamlit as st


@st.cache_data  # type: ignore
def get_number_of_good_restaurants(
    df: pd.DataFrame, rating: float, popularity: float
) -> int:
    good_restaurants = df[df["rating"] >= rating]
    number_of_good_restaurants = len(
        good_restaurants[good_restaurants["user_ratings_total"] >= popularity]
    )
    return number_of_good_restaurants


@st.cache_data  # type: ignore
def get_percent_of_good_restaurants(
    df: pd.DataFrame, rating: float, popularity: float
) -> float:
    total_num_of_restaurants = len(df)
    good_restaurants = df[df["rating"] >= rating]
    number_of_good_restaurants = len(
        good_restaurants[good_restaurants["user_ratings_total"] >= popularity]
    )
    percentage_of_good_restaurants = (
        number_of_good_restaurants / total_num_of_restaurants
    )
    return percentage_of_good_restaurants


@st.cache_data  # type: ignore
def update_stats_per_cuisine(
    df: pd.DataFrame, cuisine: str, rating: float, popularity: int
) -> pd.DataFrame:
    """
    Computes cuisine statistics across Berlin based on rating and popularity criteria.

    Args:
        df (pd.DataFrame): The input DataFrame containing restaurant data.
        cuisine (str): The specific cuisine type to filter by ("All" for all cuisines).
        rating (float): The minimum rating threshold.
        popularity (int): The minimum number of user ratings.

    Returns:
        pd.DataFrame: A DataFrame with cuisine statistics.
    """
    results = []

    # Total number of restaurants for calculating percentages
    total_restaurants = df["names_clean"].count()

    if cuisine == "All":
        # Group by cuisine type
        for cuisine_name, cuisine_df in df.groupby("food_type"):
            total_cuisine_restaurants = cuisine_df["names_clean"].count()

            # Filter for good restaurants
            good_cuisine_df = cuisine_df[
                (cuisine_df["rating"] >= rating)
                & (cuisine_df["user_ratings_total"] >= popularity)
            ]
            good_cuisine_count = good_cuisine_df["names_clean"].count()

            # Compute percentages
            percent_all = (
                round(total_cuisine_restaurants / total_restaurants, 2)
                if total_restaurants
                else 0
            )
            percent_good = (
                round(good_cuisine_count / total_cuisine_restaurants, 2)
                if total_cuisine_restaurants
                else 0
            )

            # Append row to results
            results.append(
                [cuisine_name, total_cuisine_restaurants, percent_all, percent_good]
            )

    else:
        # Filter for a specific cuisine
        cuisine_df = df[df["food_type"] == cuisine.lower()]
        total_cuisine_restaurants = cuisine_df["names_clean"].count()

        # Filter for good restaurants
        good_cuisine_df = cuisine_df[
            (cuisine_df["rating"] >= rating)
            & (cuisine_df["user_ratings_total"] >= popularity)
        ]
        good_cuisine_count = good_cuisine_df["names_clean"].count()

        # Compute percentages
        percent_all = (
            round(total_cuisine_restaurants / total_restaurants, 2)
            if total_restaurants
            else 0
        )
        percent_good = (
            round(good_cuisine_count / total_cuisine_restaurants, 2)
            if total_cuisine_restaurants
            else 0
        )

        # Append row to results
        results.append([cuisine, total_cuisine_restaurants, percent_all, percent_good])

    # Create DataFrame outside loop
    cuisines_df = pd.DataFrame(
        results,
        columns=[
            "cuisine",
            "number_restaurants_in_Berlin",
            "%_all_restaurants_in_Berlin",
            "%_considered_good",
        ],
    )

    return cuisines_df.sort_values(by="%_all_restaurants_in_Berlin", ascending=False)


@st.cache_data  # type: ignore
def update_stats_per_hood(
    df: pd.DataFrame, rating: float, popularity: float
) -> pd.DataFrame:
    # Pre-filter the good restaurants based on rating and popularity
    good_restaurants = df[
        (df["rating"] >= rating) & (df["user_ratings_total"] >= popularity)
    ]

    # List to store the results
    result_lst = []

    # Get total number of restaurants
    total_restaurants_count = df["names_clean"].count()

    # Iterate over each district (hood)
    for hood, hood_df in df.groupby("district"):
        # Filter good restaurants in the current hood
        good_in_hood_df = good_restaurants[good_restaurants["district"] == hood]

        # Calculate the number of restaurants in the hood and other metrics
        count_hood = hood_df["names_clean"].count()
        percent_hood = (
            round(count_hood / total_restaurants_count, 2)
            if total_restaurants_count > 0
            else 0
        )
        count_good_hood = good_in_hood_df["names_clean"].count()

        # Calculate percentage of good restaurants in the hood out of all good restaurants
        good_restaurants_count = good_restaurants["names_clean"].count()
        percent_good_hood = (
            round(count_good_hood / good_restaurants_count, 2)
            if good_restaurants_count > 0
            else 0
        )

        # Append the results for the current hood
        result_lst.append(
            [hood, count_hood, percent_hood, count_good_hood, percent_good_hood]
        )

    # Convert the result list to a DataFrame
    hoods_df = pd.DataFrame(
        result_lst,
        columns=[
            "district",
            "number_of_restaurants",
            "%_all_berlin_restaurants",
            "number_good_restaurants",
            "%_all_good_restaurants",
        ],
    )

    # Sort the DataFrame by number of restaurants in descending order
    hoods_df = hoods_df.sort_values(by="number_of_restaurants", ascending=False)

    return hoods_df


@st.cache_data  # type: ignore
def update_stats_per_hood_and_cuisine(
    df: pd.DataFrame, rating: float, popularity: int
) -> pd.DataFrame:
    """
    Computes restaurant statistics per district and cuisine based on rating and popularity criteria.

    Args:
        df (pd.DataFrame): The input DataFrame containing restaurant data.
        rating (float): The minimum rating threshold.
        popularity (int): The minimum number of user ratings.

    Returns:
        pd.DataFrame: A DataFrame with statistics per district and cuisine.
    """
    results = []

    # Precompute "good" restaurants (satisfying rating & popularity criteria)
    good_df = df[(df["rating"] >= rating) & (df["user_ratings_total"] >= popularity)]
    good_cuisine_counts = good_df.groupby("food_type")["names_clean"].count().to_dict()

    # Group by district once instead of repeatedly filtering
    for hood, hood_df in df.groupby("district"):
        total_hood_restaurants = hood_df["food_type"].count()

        # Iterate over cuisines within the current district
        for cuisine, cuisine_df in hood_df.groupby("food_type"):
            total_cuisine_count = cuisine_df["food_type"].count()

            # Filter for good restaurants in this district and cuisine
            good_cuisine_df = cuisine_df[
                (cuisine_df["rating"] >= rating)
                & (cuisine_df["user_ratings_total"] >= popularity)
            ]
            good_cuisine_count = good_cuisine_df["names_clean"].count()

            # Compute statistics
            percent_in_district = (
                round(total_cuisine_count / total_hood_restaurants, 2)
                if total_hood_restaurants
                else "No restaurants in this district"
            )

            percent_good = (
                round(good_cuisine_count / total_cuisine_count, 2)
                if total_cuisine_count
                else "No restaurants of this cuisine in this district"
            )

            percent_all_good_cuisines = (
                round(good_cuisine_count / good_cuisine_counts.get(cuisine, 1), 2)
                if good_cuisine_counts.get(cuisine, 0) > 0
                else "No restaurants of this cuisine in Berlin"
            )

            # Append row to results
            results.append(
                [
                    hood,
                    cuisine,
                    total_cuisine_count,
                    percent_in_district,
                    percent_good,
                    percent_all_good_cuisines,
                ]
            )

    # Convert collected data into a DataFrame outside the loop
    hoods_cuisine_df = pd.DataFrame(
        results,
        columns=[
            "district",
            "cuisine",
            "count",
            "%_restaurants_in_district",
            "%_considered_good",
            "%_all_good_restaurants_for_this_cuisine_in_berlin",
        ],
    )

    return hoods_cuisine_df.sort_values(by=["district", "count"], ascending=False)


@st.cache_data  # type: ignore
def update_stats_per_cuisine_and_hood(
    df: pd.DataFrame, rating: float, popularity: float
) -> pd.DataFrame:
    # Filter data where rating and user_ratings_total meet the criteria
    df_good = df[(df["rating"] >= rating) & (df["user_ratings_total"] >= popularity)]

    # Initialize a list to store results
    result_lst = []

    # Iterate over each group by district and food type (combined in one loop)
    for (hood, cuisine), group in df.groupby(["district", "food_type"]):
        # Filter hood and cuisine specific data
        hood_df = group
        good_df = df_good[
            (df_good["district"] == hood) & (df_good["food_type"] == cuisine)
        ]

        # All restaurants for the given cuisine
        all_cuisines_df = df[df["food_type"] == cuisine]
        all_good_cuisines_df = df_good[df_good["food_type"] == cuisine]

        # Calculate the metrics
        count_hood = hood_df["names_clean"].count()
        count_all_cuisine = all_cuisines_df["names_clean"].count()
        count_good_hood = good_df["names_clean"].count()
        count_good_all_cuisine = all_good_cuisines_df["names_clean"].count()

        # Append the results
        result_lst.append(
            [
                cuisine,
                hood,
                count_hood,
                (
                    round(count_hood / count_all_cuisine, 2)
                    if count_all_cuisine > 0
                    else 0
                ),
                round(count_good_hood / count_hood, 2) if count_hood > 0 else 0,
                (
                    round(count_good_hood / count_good_all_cuisine, 2)
                    if count_good_all_cuisine > 0
                    else 0
                ),
            ]
        )

    # Convert the result list to a DataFrame
    result_df = pd.DataFrame(
        result_lst,
        columns=[
            "cuisine",
            "district",
            "count",
            "percent_all_restaurants_of_berlin",
            "%_considered_good",
            "%_all_good_restaurants_for_this_cuisine_in_berlin",
        ],
    )

    # Sort the DataFrame by count in descending order
    result_df = result_df.sort_values(by="count", ascending=False)

    return result_df
