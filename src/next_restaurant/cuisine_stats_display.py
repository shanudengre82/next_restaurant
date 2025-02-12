import streamlit as st
import pandas as pd


def display_additional_stats(
    most_frq_price_level: str,
    avg_rating: float,
    good_restaurants_per: int,
    best_competitor: str,
):
    # Printing local stats
    st.markdown(f"Most of them have price level **{most_frq_price_level}**.")
    st.markdown(
        f"Their average rating is **{round(avg_rating, 2)}**, and **{good_restaurants_per}%** of restaurants are considered as good."
    )
    st.markdown(
        f"Based on the address you provided, your top potential competitor would be: **{best_competitor}**."
    )

    # Making heading for the suggestion part
    st.header("Our suggestions in the area")

    # Adding description for the marker.
    st.markdown(
        '#### <span style="color:orange">*Orange marker*</span>: center of low rated resaturants of the area',
        unsafe_allow_html=True,
    )
    st.markdown(
        '#### <span style="color:blue">*Blue marker*</span>: center of high rated resaturants of the area',
        unsafe_allow_html=True,
    )
    st.markdown(
        '#### <span style="color:lightgreen">*Lightreen marker*</span>: furthest locations from all restaurants in the area',
        unsafe_allow_html=True,
    )
    st.markdown("###### ")


def all_district_all_cuisines(
    total_number_of_restaurants: int,
    number_of_good_restaurants: int,
    five_most_common_cuisines: list,
    five_most_common_percent: list,
):
    st.write(
        f"\
    - There are {total_number_of_restaurants} restaurants in Berlin, \
    {number_of_good_restaurants} of them are good restaurants "
    )
    st.write(
        f"\
    - The three most common type of cuisines are\
    {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}% of all restaurants),\
    {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}% of all restaurants),\
    {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}% of all restaurants)."
    )

    st.write("For more information, select a district and a cuisine type.")


def all_district_selected_cuisine(
    stats_hoods_cuisine: pd.DataFrame,
    stats_cuisine_hoods: pd.DataFrame,
    options_cuisine: str,
    number_cuisine: int,
    percent_good_cuisine: int,
    percent_of_all: int,
    best_rated_3_cuisines: list,
    best_rated_3_perc: list,
):
    main_hood_per_cuisine = list(
        stats_cuisine_hoods[stats_hoods_cuisine["cuisine"] == options_cuisine.lower()][
            "district"
        ][0:5]
    )
    p = list(
        stats_cuisine_hoods[stats_cuisine_hoods["cuisine"] == options_cuisine.lower()][
            "percent_all_restaurants_of_berlin"
        ][0:5]
        * 100
    )

    st.write(
        f"\
        - There are {number_cuisine} {options_cuisine} restaurants in Berlin,\
        {percent_good_cuisine}% are good restaurants"
    )
    st.write(
        f"\
        - {options_cuisine} restaurants represents {round(percent_of_all)}% \
            of all Berlin restaurants"
    )
    st.write(
        f"\
        - {options_cuisine} restaurants are mostly located in \
    {main_hood_per_cuisine[0]} ({round(p[0])}%), {main_hood_per_cuisine[1]} ({round(p[1])}%) and \
    {main_hood_per_cuisine[2]} ({round(p[2])}%)"
    )

    st.write(
        f"In Berlin, the type of restaurants which have the best ratings are:\
    {best_rated_3_cuisines[0]} ({round(best_rated_3_perc[0])}%),\
    {best_rated_3_cuisines[1]} ({round(best_rated_3_perc[1])}%) and \
    {best_rated_3_cuisines[2]} ({round(best_rated_3_perc[1])}%)"
    )


def selected_district_all_cuisine(
    stats_hoods: pd.DataFrame,
    options_district: str,
    main_cuisine_per_hood: str,
    percent_main_cuisine: str,
    total_num_of_restaurants: int,
    number_of_good_restaurants: int,
    most_restaurants: str,
    most_restaurants_perc: int,
    best_district: str,
    best_district_per: int,
    five_most_common_cuisines: list,
    five_most_common_percent: list,
):
    stats_hoods_hood = stats_hoods[stats_hoods["district"] == options_district]

    num_restaurants = stats_hoods_hood.iloc[0]["number_of_restaurants"]
    num_good_restaurants = stats_hoods_hood.iloc[0]["number_good_restaurants"]
    percentage_good_restaurants_hood = round(
        stats_hoods_hood.iloc[0]["%_all_good_restaurants"] * 100
    )

    st.write(
        f"\
    - There are {num_restaurants} restaurants in {options_district}, \
    {round((num_good_restaurants / num_restaurants) * 100)}% of them are good "
    )
    st.write(
        f"\
        - {options_district} has {percentage_good_restaurants_hood} % of the best restaurants in Berlin"
    )
    st.write(
        f"\
    - Most common type of cuisine in {options_district}:\
    {main_cuisine_per_hood[0].capitalize()}, ({round(percent_main_cuisine[0])}%) \
    {main_cuisine_per_hood[1].capitalize()} ({round(percent_main_cuisine[1])}%) \
    and {main_cuisine_per_hood[2].capitalize()} ({round(percent_main_cuisine[2])}%)."
    )

    st.write(
        f"In Berlin overall, there are: {total_num_of_restaurants} restaurants \
    {number_of_good_restaurants} of them are good"
    )
    st.write(
        f"- {most_restaurants} has most restaurants in Berlin ({most_restaurants_perc}%) \
    and {best_district} has most of the good restaurants ({best_district_per}%)"
    )
    st.write(
        f"The most common types of cuisines in Berlin are:\
     {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}%), \
     {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}%) and \
     {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}%)"
    )


def selected_district_selected_cuisine(
    stats_hoods_cuisine: pd.DataFrame,
    stats_cuisine_hoods: pd.DataFrame,
    options_district: str,
    options_cuisine: str,
    berlin_cuisine: int,
    berlin_good_cuisine: int,
):
    stats_hoods_cuisine_hood = stats_hoods_cuisine[
        stats_hoods_cuisine["district"] == options_district
    ]
    stats_hoods_cuisine_cuisine = stats_hoods_cuisine_hood[
        stats_hoods_cuisine_hood["cuisine"] == options_cuisine.lower()
    ]
    num = stats_hoods_cuisine_cuisine.iloc[0]["count"]
    good = round(stats_hoods_cuisine_cuisine.iloc[0]["%_considered_good"] * 100)
    percent_of_all = round(
        stats_hoods_cuisine_cuisine.iloc[0][
            "%_all_good_restaurants_for_this_cuisine_in_berlin"
        ]
        * 100
    )

    stats_hoods_good = stats_cuisine_hoods[
        stats_cuisine_hoods["cuisine"] == options_cuisine.lower()
    ].sort_values(by=["percent_all_restaurants_of_berlin"], ascending=False)
    name = stats_hoods_good.iloc[0]["district"]
    perce = round(stats_hoods_good.iloc[0]["percent_all_restaurants_of_berlin"] * 100)
    stats_hoods_2 = stats_cuisine_hoods[
        stats_cuisine_hoods["cuisine"] == options_cuisine.lower()
    ].sort_values(
        by=["%_all_good_restaurants_for_this_cuisine_in_berlin"], ascending=False
    )
    name_2 = stats_hoods_2.iloc[0]["district"]
    perce_2 = round(
        stats_hoods_2.iloc[0]["%_all_good_restaurants_for_this_cuisine_in_berlin"] * 100
    )

    st.write(
        f" - There are {num} {options_cuisine.capitalize()} restaurants in {options_district}, \
        {good}% of them are good restaurants"
    )
    st.write(
        f" - {percent_of_all}% of the all the {options_cuisine.capitalize()} restaurants of Berlin \
    are located in {options_district} "
    )

    st.write(
        f" - In Berlin overall, there are {berlin_cuisine} {options_cuisine.capitalize()} restaurants,\
 {round(berlin_good_cuisine * 100)}% of them are good "
    )
    st.write(
        f" - {name} has most {options_cuisine.capitalize()} restaurants in Berlin ({perce}%)"
    )
    st.write(
        f" - {name_2}  has most of the good {options_cuisine.capitalize()} restaurants ({perce_2}%)"
    )
