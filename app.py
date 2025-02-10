import streamlit as st
import folium
import pandas as pd
from geopy.geocoders import Nominatim

from streamlit_folium import folium_static
from next_restaurant.cuisine_info import change_main_food_types
from next_restaurant.functions_for_df import (
    get_map_instance,
    generating_circles,
    get_popularity,
)
from next_restaurant.stats import (
    get_stats_per_cuisine,
    get_stats_per_hood,
    get_stats_per_hood_and_cuisine,
    get_stats_per_cuisine_and_hood,
    get_percent_of_good_restaurants,
    get_number_of_good_restaurants,
)
from next_restaurant.features_to_suggest import (
    calc_centers,
    k_neighbours_df,
    neighbours_stats,
)
from next_restaurant.cuisine_info import (
    CUSINE_ORDERED_DATA_FRAME_CAPITALISE,
    CUISINE_CLEAN_DATA_FRAME_TO_REMOVE,
    CUISINE_TO_REMOVE,
)
from next_restaurant.district import BERLIN_DISTRICTS
from next_restaurant.local_search_coordinates import generating_circular_coordinates
from next_restaurant.parameters import BERLIN_CENTER, WIDTH, HEIGHT, INITIAL_ZOOM
from next_restaurant.local_search_coordinates import (
    get_locating_best_place_based_on_distance,
)

# SET LAYOUT
st.set_page_config(
    page_title="NEXT RESTAURANT", initial_sidebar_state="expanded", layout="wide"
)

# LOAD THE DATAFRAME
df = pd.read_csv("raw_data//clean_dataframe_1.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(get_popularity)

# Capitalize food_types for the selection dropdown
df = change_main_food_types(df)

df["food_type_1_english"] = df["food_type"].str.capitalize()

# makes copies of the df for the second plot and the stats
df_copy = df.copy()
df_copy_for_stats = df.copy()

# MAIN PAGE
# Title and subheader
st.title("Next Restaurant")
st.header("Browse through the restaurants in Berlin")

st.markdown("###### ")
st.markdown(
    '#### <span style="color:blue">**Blue circles**</span>: High rated restaurants',
    unsafe_allow_html=True,
)
st.markdown(
    '#### <span style="color:orange">**Orange circles**</span>: Low rated restaurants',
    unsafe_allow_html=True,
)
st.markdown("###### ")

# Title
st.sidebar.markdown("""# Find the best place to open your restaurant""")

# Cuisine selection

st.sidebar.subheader("Do you already have a type of cuisine in mind?")

selected_cuisine = [
    cuisine
    for cuisine in CUSINE_ORDERED_DATA_FRAME_CAPITALISE
    if cuisine not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]

options_cuisine = st.sidebar.selectbox("Select a type of cuisine", selected_cuisine)

if options_cuisine != "All":
    df = df[df["food_type_1_english"] == options_cuisine]

# District selection
st.sidebar.subheader("Do you already have a district in mind?")

options_district = st.sidebar.selectbox("Select a district", BERLIN_DISTRICTS)

if options_district != "All":
    df = df[df["district"] == options_district]

# input popularity and ratings
st.sidebar.subheader(
    "What would you consider a good restaurant based on customers ratings?"
)

rating_cutoff = st.sidebar.slider(
    "Please select a rating", min_value=2.0, max_value=5.0, step=0.1, value=4.5
)

# user popularity cutoff
popularity_cutoff = st.sidebar.slider(
    "Please select a number of rating", min_value=0, max_value=2000, step=1, value=40
)

# Conditions for generating maps
blue_ratings = st.sidebar.checkbox("Only show me good restaurants")
red_ratings = st.sidebar.checkbox("Only show me bad restaurants")

# POPULARITY AND RATINGS CUTOFFS
# Conditions for generating maps
blue_popular = st.sidebar.checkbox("Only show me popular restaurants")
red_popular = st.sidebar.checkbox("Only show me unpopular restaurants")

# Input an address
st.sidebar.subheader("Do you already have an address in mind?")

user_input = st.sidebar.text_input("Enter an address", "Mitte, Berlin")

geolocator = Nominatim(user_agent="MyApp")

location = geolocator.geocode(user_input)

# TODO: Uopdate defination properly there is a mismatch somehwere between latitude and longitude
local_lat = location.latitude
local_lng = location.longitude

district = geolocator.geocode(f"{options_district}, Berlin")
local_lng_district = district.latitude
local_lat_district = district.longitude

# Number of restaurants to be considered locally
number_of_nearby_restaurant_to_be_considered = st.sidebar.slider(
    "How many nearest restaurants would you like to see?",
    min_value=5,
    max_value=100,
    step=5,
    value=20,
)

# Determining color for ratings cutoff
df["ratings_color"] = df["rating"].apply(
    lambda x: "orange" if x < rating_cutoff else "blue"
)

# Chopping data frame with respect to popularity cutoff
df = df[df["user_ratings_total"] > popularity_cutoff]

# FIRST MAP
# Display the map
if options_district == "All":
    m = get_map_instance(
        zoom=INITIAL_ZOOM, initial_location=BERLIN_CENTER, width=WIDTH, height=HEIGHT
    )
else:
    m = get_map_instance(
        zoom=14,
        initial_location=[local_lat_district, local_lng_district],
        width=WIDTH,
        height=HEIGHT,
    )

if red_ratings and blue_ratings:
    m = generating_circles(m, df, "ratings_color")

elif red_ratings and not blue_ratings:
    df_red = df[df["ratings_color"] == "orange"]
    heatmap_red_ratings = df_red[["lat", "lng", "rating"]]
    m = generating_circles(m, df_red, "ratings_color")

elif blue_ratings and not red_ratings:
    df_blue = df[df["ratings_color"] == "blue"]
    heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]
    m = generating_circles(m, df_blue, "ratings_color")
else:
    m = generating_circles(m, df, "ratings_color")

folium.LayerControl().add_to(m)
folium_static(m)

# Making list of clean cuisine for global choices
cuisine_list = df["food_type_1_english"].value_counts().index.tolist()
cuisine_list = [i for i in cuisine_list if i not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE]

df_top_cuisine = df.loc[df["food_type_1_english"].isin(cuisine_list[0:10])]
if len(cuisine_list) < 10:
    df_top_cuisine = df_top_cuisine.loc[
        df_top_cuisine["food_type_1_english"].isin(cuisine_list)
    ]
else:
    df_top_cuisine = df_top_cuisine.loc[
        df_top_cuisine["food_type_1_english"].isin(cuisine_list[0:10])
    ]

st.header("Key points")
st.subheader("Consider this information when chosing a location for your restaurant:")

# general stats about Berlin
percent_good_restaurants = get_percent_of_good_restaurants(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)
total_num_of_restaurants = len(df_copy_for_stats)
number_of_good_restaurants = get_number_of_good_restaurants(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)

# cuisine stats
stats_cuisine = get_stats_per_cuisine(
    df_copy_for_stats, options_cuisine, rating_cutoff, popularity_cutoff
)
five_most_common_cuisines = list(stats_cuisine["cuisine"][0:5])
five_most_common_percent = list(stats_cuisine["%_all_restaurants_in_Berlin"] * 100)[0:5]
number_cuisine = round(list(stats_cuisine["number_restaurants_in_Berlin"])[0])
percent_good_cuisine = list(stats_cuisine["%_considered_good"] * 100)[0]
percent_of_all = list(stats_cuisine["%_all_restaurants_in_Berlin"] * 100)[0]

best_rated_cuisines = get_stats_per_cuisine(
    df_copy_for_stats, "All", rating_cutoff, popularity_cutoff
)

best_rated_cuisines_df = best_rated_cuisines.sort_values(
    by=["%_considered_good"], ascending=False
)
best_rated = best_rated_cuisines_df[
    ~best_rated_cuisines_df["cuisine"].isin(CUISINE_TO_REMOVE)
]
best_rated_3_cuisines = list(best_rated["cuisine"])[0:3]
best_rated_3_perc = list(best_rated["%_considered_good"] * 100)[0:3]

berlin_cuisine = stats_cuisine.iloc[0]["number_restaurants_in_Berlin"]
berlin_good_cuisine = stats_cuisine.iloc[0]["%_considered_good"]

# hoods stats
stats_hoods = get_stats_per_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)
most_restaurants = stats_hoods.iloc[0]["district"]
most_restaurants_perc = round(stats_hoods.iloc[0]["%_all_berlin_restaurants"] * 100)
best_hood = stats_hoods.sort_values(by=["%_all_good_restaurants"], ascending=False)
best_district = best_hood.iloc[0]["district"]
best_district_per = round(best_hood.iloc[0]["%_all_good_restaurants"] * 100)

# hoods and cuisine stats
stats_hoods_cuisine = get_stats_per_hood_and_cuisine(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)
main_cuisine_per_hood = list(
    stats_hoods_cuisine[stats_hoods_cuisine["district"] == options_district]["cuisine"][
        0:5
    ]
)
percent_main_cuisine = list(
    stats_hoods_cuisine[stats_hoods_cuisine["district"] == options_district][
        "%_restaurants_in_district"
    ][0:5]
    * 100
)
num_cuisine_per_hood = stats_hoods_cuisine


stats_cuisine_hoods = get_stats_per_cuisine_and_hood(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)

# text to be displayed:

if options_district == "All" and options_cuisine == "All":
    st.write(
        f"\
    - There are {total_num_of_restaurants} restaurants in Berlin, \
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

elif options_district == "All" and options_cuisine != "All":
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

elif options_district != "All" and options_cuisine == "All":
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

else:
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

# MAP ZOOMED IN
df_local = k_neighbours_df(
    df_copy,
    local_lat,
    local_lng,
    n_restaurants=number_of_nearby_restaurant_to_be_considered,
)

# Determining color for ratings cutoff
df_local["ratings_color"] = df_local["rating"].apply(
    lambda x: "orange" if x < rating_cutoff else "blue"
)

# Chopping data frame with respect to popularity cutoff
df_local = df_local[df_local["user_ratings_total"] > popularity_cutoff]

# In case of address input
st.header("Your closest competitors")

(
    most_frq_price_level,
    avg_rating,
    best_competitor,
    cuisine_distribution,
    good_restaurants_per,
    bad_restaurants_per,
) = neighbours_stats(df)

# Capitalising names
best_competitor_capitalise = []
for competitor in best_competitor.split():
    try:
        best_competitor_capitalise.append(competitor.capitalize())
    except Exception:
        best_competitor_capitalise.append(competitor)
best_competitor = " ".join(best_competitor_capitalise)

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

# Estimating centroid bad and centroid good
center_bad_center_good = calc_centers(df_local, rating_cutoff)

if isinstance(center_bad_center_good, dict):
    first_key = next(iter(center_bad_center_good))
    o = get_map_instance(
        zoom=15,
        initial_location=[
            center_bad_center_good[first_key][0],
            center_bad_center_good[first_key][1],
        ],
        width=WIDTH,
        height=HEIGHT,
    )
else:
    o = get_map_instance(
        zoom=15,
        initial_location=[center_bad_center_good[1][0], center_bad_center_good[1][1]],
        width=WIDTH,
        height=HEIGHT,
    )

# Making circles around the popularity and color coding it.
o = generating_circles(o, df_local, "ratings_color")

suggestion_number_distance = st.slider(
    "Number of lightgreen markers", min_value=1, max_value=10, step=1, value=2
)

# Dataframe with just latitudes and longitutes. They are to generate suggestions.
df_local_lat_lng = df_local[["lat", "lng", "distance"]]

# Coordinates inside a local box
local_box = generating_circular_coordinates(
    df=df_local_lat_lng, lat=local_lat, lng=local_lng
)
# Creating best location lists
best_location_based_on_distance_list = []
for _ in range(suggestion_number_distance):
    best_location_based_on_distance = get_locating_best_place_based_on_distance(
        box=local_box, df=df_local_lat_lng
    )
    best_location_based_on_distance_list.append(best_location_based_on_distance)
    to_append = [
        best_location_based_on_distance[0],
        best_location_based_on_distance[1],
        0,
    ]
    df_local_lat_lng.loc[len(df_local_lat_lng.index)] = to_append


if isinstance(center_bad_center_good, dict):
    if first_key == "center_bad":
        color = "orange"
    else:
        color = "darkblue"
    folium.Marker(
        location=[
            center_bad_center_good[first_key][0],
            center_bad_center_good[first_key][1],
        ],
        popup="Center of low rated restarants",
        icon=folium.Icon(color=color),
    ).add_to(o)
else:
    folium.Marker(
        [center_bad_center_good[1][0], center_bad_center_good[1][1]],
        popup="Center of high rated restarants",
        icon=folium.Icon(color="darkblue"),
    ).add_to(o)
    folium.Marker(
        [center_bad_center_good[0][0], center_bad_center_good[0][1]],
        popup="Center of low rated restarants",
        icon=folium.Icon(color="orange"),
    ).add_to(o)

number = 1
for i in best_location_based_on_distance_list:
    folium.Marker(
        i,
        popup=f"Optimum location number {number} based on distance from nearest neighbour restaurant",
        icon=folium.Icon(color="lightgreen"),
    ).add_to(o)
    number += 1

folium_static(o)

# Making list of clean cuisine for local choices
cuisine_list_local = df_local["food_type_1_english"].value_counts().index.tolist()
cuisine_list_local = [
    cuisine
    for cuisine in cuisine_list_local
    if cuisine not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]

if len(cuisine_list_local) < 10:
    df_top_cuisine_local = df_local.loc[
        df_local["food_type_1_english"].isin(cuisine_list_local)
    ]
else:
    df_top_cuisine_local = df_local.loc[
        df_local["food_type_1_english"].isin(cuisine_list_local[0:10])
    ]
