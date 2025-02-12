import pandas as pd
import streamlit as st


@st.cache_data
def get_number_of_good_restaurants(df, rating, popularity):
    good_restaurants = df[df["rating"] >= rating]
    number_of_good_restaurants = len(
        good_restaurants[good_restaurants["user_ratings_total"] >= popularity]
    )
    return number_of_good_restaurants


@st.cache_data
def get_percent_of_good_restaurants(df, rating, popularity):
    total_num_of_restaurants = len(df)
    good_restaurants = df[df["rating"] >= rating]
    number_of_good_restaurants = len(
        good_restaurants[good_restaurants["user_ratings_total"] >= popularity]
    )
    percentage_of_good_restaurants = (
        number_of_good_restaurants / total_num_of_restaurants
    )
    return percentage_of_good_restaurants


@st.cache_data
def update_stats_per_cuisine(df, cuisine, rating, popularity):
    lst_ = []
    if cuisine == "All":
        for cuisine, cuisine_df in df.groupby("food_type"):
            good_cuisine_type = cuisine_df[cuisine_df.rating >= rating]
            good_cuisine_type_df = good_cuisine_type[
                good_cuisine_type.user_ratings_total >= popularity
            ]

            lst_.append(cuisine)
            lst_.append(cuisine_df["names_clean"].count())
            lst_.append(
                round(
                    cuisine_df["names_clean"].count() / df["names_clean"].count(), 2
                )
            )
            lst_.append(
                round(
                    good_cuisine_type_df["names_clean"].count()
                    / cuisine_df["names_clean"].count(),
                    2,
                )
            )

            # Make it a df

            splitted = [lst_[i : i + 4] for i in range(0, len(lst_), 4)]
            cuisines_df = pd.DataFrame(splitted)
            cuisines_df.columns = [
                "cuisine",
                "number_restaurants_in_Berlin",
                "%_all_restaurants_in_Berlin",
                "%_considered_good",
            ]
            cuisines_df = cuisines_df.sort_values(
                by=["%_all_restaurants_in_Berlin"], ascending=False
            )

        return cuisines_df

    else:
        cuisine_type = df[df.food_type == cuisine.lower()]
        good_cuisine_type = cuisine_type[cuisine_type.rating >= rating]
        good_cuisine_type_df = good_cuisine_type[
            good_cuisine_type.user_ratings_total >= popularity
        ]

        lst_.append(cuisine)
        lst_.append(cuisine_type["names_clean"].count())
        lst_.append(
            round(cuisine_type["names_clean"].count() / df["names_clean"].count(), 2)
        )
        lst_.append(
            round(
                good_cuisine_type_df["names_clean"].count()
                / cuisine_type["names_clean"].count(),
                2,
            )
        )

        # Make it a df
        splitted = [lst_[i : i + 4] for i in range(0, len(lst_), 4)]
        cuisines_df = pd.DataFrame(splitted)
        cuisines_df.columns = [
            "cuisine",
            "number_restaurants_in_Berlin",
            "%_all_restaurants_in_Berlin",
            "%_considered_good",
        ]
        cuisines_df = cuisines_df.sort_values(
            by=["%_all_restaurants_in_Berlin"], ascending=False
        )

        return cuisines_df


@st.cache_data
def update_stats_per_hood(df, rating, popularity):
    lst_2 = []
    for hood, hood_df in df.groupby("district"):
        good_in_hood = hood_df[hood_df.rating >= rating]
        good_in_hood_df = good_in_hood[good_in_hood.user_ratings_total >= popularity]

        good_restaurants = df[df.rating >= rating]
        good_restaurants_df = good_restaurants[
            good_restaurants.user_ratings_total >= popularity
        ]

        lst_2.append(hood)
        lst_2.append(hood_df["names_clean"].count())
        lst_2.append(
            round(hood_df["names_clean"].count() / df["names_clean"].count(), 2)
        )
        lst_2.append(round(good_in_hood_df["names_clean"].count()))
        lst_2.append(
            good_in_hood_df["names_clean"].count()
            / good_restaurants_df["names_clean"].count()
        )

        # Make it a df
        splitted_ = [lst_2[i : i + 5] for i in range(0, len(lst_2), 5)]
        hoods_df_ = pd.DataFrame(splitted_)
        hoods_df_.columns = [
            "district",
            "number_of_restaurants",
            "%_all_berlin_restaurants",
            "number_good_restaurants",
            "%_all_good_restaurants",
        ]
        hoods_df_ = hoods_df_.sort_values(by=["number_of_restaurants"], ascending=False)

    return hoods_df_


@st.cache_data
def update_stats_per_hood_and_cuisine(df, rating, popularity):
    lst_3 = []
    for hood, hood_df in df.groupby("district"):
        for cuisine, cuisine_df in df.groupby("food_type"):
            hood_df = df[df.district == hood]
            cuisine_df = hood_df[hood_df.food_type == cuisine.lower()]
            good = cuisine_df[cuisine_df.rating >= rating]
            good_df = good[good.user_ratings_total >= popularity]
            all_cuisines = df[df.food_type == cuisine]
            all_good_cuisines = all_cuisines[all_cuisines.rating >= rating]
            all_good_cuisines_df = all_good_cuisines[
                all_good_cuisines.user_ratings_total >= popularity
            ]

            lst_3.append(hood)
            lst_3.append(cuisine)
            lst_3.append(cuisine_df["food_type"].count())
            lst_3.append(
                round(cuisine_df["food_type"].count() / hood_df["food_type"].count(), 2)
            )
            lst_3.append(
                round(
                    good_df["names_clean"].count() / cuisine_df["food_type"].count(), 2
                )
            )
            lst_3.append(
                round(
                    good_df["names_clean"].count()
                    / all_good_cuisines_df["names_clean"].count(),
                    2,
                )
            )

            # make the list a dataframe

            list_splitted = [lst_3[i : i + 6] for i in range(0, len(lst_3), 6)]

            hoods_cuisine = pd.DataFrame(list_splitted)
            hoods_cuisine.columns = [
                "district",
                "cuisine",
                "count",
                "%_restaurants_in_district",
                "%_considered_good",
                "%_all_good_restaurants_for_this_cuisine_in_berlin",
            ]
            hoods_cuisine = hoods_cuisine.sort_values(
                by=["district", "count"], ascending=False
            )

    return hoods_cuisine


@st.cache_data
def update_stats_per_cuisine_and_hood(df, rating, popularity):
    lst_4 = []
    for hood, hood_df in df.groupby("district"):
        for cuisine, cuisine_df in df.groupby("food_type"):
            cuisine_df = df[df.food_type == cuisine]
            hood_df = cuisine_df[cuisine_df.district == hood]

            good = hood_df[hood_df.rating >= rating]
            good_df = good[good.user_ratings_total >= popularity]

            all_cuisines = df[df.food_type == cuisine]
            all_good_cuisines = all_cuisines[all_cuisines.rating >= rating]
            all_good_cuisines_df = all_good_cuisines[
                all_good_cuisines.user_ratings_total >= popularity
            ]

            lst_4.append(cuisine)
            lst_4.append(hood)
            lst_4.append(hood_df["names_clean"].count())
            lst_4.append(
                round(
                    hood_df["names_clean"].count()
                    / all_cuisines["names_clean"].count(),
                    2,
                )
            )
            lst_4.append(
                round(
                    good_df["names_clean"].count() / hood_df["names_clean"].count(), 2
                )
            )
            lst_4.append(
                round(
                    good_df["names_clean"].count()
                    / all_good_cuisines_df["names_clean"].count(),
                    2,
                )
            )

    # make the list a dataframe
    list_splitted = [lst_4[i : i + 6] for i in range(0, len(lst_4), 6)]
    cuisine_hoods = pd.DataFrame(list_splitted)
    cuisine_hoods.columns = [
        "cuisine",
        "district",
        "count",
        "percent_all_restaurants_of_berlin",
        "%_considered_good",
        "%_all_good_restaurants_for_this_cuisine_in_berlin",
    ]
    cuisine_hoods = cuisine_hoods.sort_values(by=["count"], ascending=False)
    return cuisine_hoods
