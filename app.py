import streamlit as st
import folium
import pandas as pd
from geopy.geocoders import Nominatim

from streamlit_folium import folium_static
from next_restaurant.cuisine_info import change_main_foodTypes
from next_restaurant.functions_for_df import (
    get_map_instance,
    generating_circles,
    update_df_based_on_selected_cusine_and_district,
)
from next_restaurant.stats import (
    update_stats_per_cuisine,
    update_stats_per_hood,
    update_stats_per_hood_and_cuisine,
    update_stats_per_cuisine_and_hood,
    get_percent_of_good_restaurants,
    get_number_of_good_restaurants,
)
from next_restaurant.features_to_suggest import (
    calc_centers,
    k_neighbours_df,
    neighbours_stats,
)
from next_restaurant.cuisine_info import (
    CUISINE_OPTIONS,
    CUISINE_CLEAN_DATA_FRAME_TO_REMOVE,
    # CUISINE_TO_REMOVE,
)
from next_restaurant.district import BERLIN_DISTRICTS
from next_restaurant.local_search_coordinates import generating_circular_coordinates
from next_restaurant.parameters import BERLIN_CENTER, WIDTH, HEIGHT, INITIAL_ZOOM
from next_restaurant.local_search_coordinates import (
    get_locating_best_place_based_on_distance,
)

from next_restaurant.cuisine_stats_display import (
    all_district_all_cuisines,
    # all_district_selected_cuisine,
    # selected_district_all_cuisine,
    # selected_district_selected_cuisine,
    display_additional_stats,
)

from typing import List

import requests  # type: ignore

from next_restaurant.german_to_english import german_to_english

# SET LAYOUT
st.set_page_config(
    page_title="NEXT RESTAURANT", initial_sidebar_state="expanded", layout="wide"
)

try:
    response = requests.get(
        st.secrets["URL_TO_DATA"], auth=(st.secrets["USERNAME"], st.secrets["PASSWORD"])
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        print("Unable to load file from web, looking file locally")
    else:
        data = response.json()["sheet1"]
        df = pd.DataFrame(data, index=False)
except Exception:
    try:
        df = pd.read_csv("raw_data//clean_dataframe.csv")
    except Exception:
        raise FileNotFoundError("Unable to find file raw_data/clean_dataframe.csv")

columns_required: List[str] = [
    "priceLevel",
    "rating",
    "userRatingsTotal",
    "lat",
    "lng",
    "namesClean",
    "fullAddress",
    "district",
    "foodType",
    "foodType_2",
]

# Updating dataframe
df = df[columns_required]
df = german_to_english(df)

# Capitalize foodTypes for the selection dropdown
df = change_main_foodTypes(df)

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
selected_cuisine = st.sidebar.selectbox("Select a type of cuisine", CUISINE_OPTIONS)

# District selection
st.sidebar.subheader("Do you already have a district in mind?")
selected_district = st.sidebar.selectbox("Select a district", BERLIN_DISTRICTS)


df_cusine_district = update_df_based_on_selected_cusine_and_district(
    df=df, cuisine=selected_cuisine, district=selected_district
)

# input popularity and ratings
st.sidebar.subheader(
    "What would you consider a good restaurant based on customers ratings?"
)

rating_cutoff = st.sidebar.slider(
    "Please select a rating", min_value=2.0, max_value=5.0, step=0.1, value=4.5
)

# user popularity cutoff
popularity_cutoff = st.sidebar.slider(
    "Minimim number of reviews", min_value=0, max_value=2000, step=1, value=40
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

# TODO: UPdates since geolocatiopn sometimes does not work
district = geolocator.geocode(f"{selected_district}, Berlin")
local_lat_district = district.latitude
local_lng_district = district.longitude

# Number of restaurants to be considered locally
number_of_nearby_restaurant_to_be_considered = st.sidebar.slider(
    "How many nearest restaurants would you like to see?",
    min_value=5,
    max_value=100,
    step=5,
    value=20,
)

# Determining color for ratings cutoff
df_cusine_district["ratings_color"] = df_cusine_district["rating"].apply(
    lambda x: "orange" if x < rating_cutoff else "blue"
)

# Chopping data frame with respect to popularity cutoff
df_cusine_district = df_cusine_district[
    df_cusine_district["userRatingsTotal"] > popularity_cutoff
]

# FIRST MAP
# Display the map
if selected_district == "All":
    map = get_map_instance(
        zoom=INITIAL_ZOOM, initial_location=BERLIN_CENTER, width=WIDTH, height=HEIGHT
    )
else:
    map = get_map_instance(
        zoom=14,
        initial_location=[local_lat_district, local_lng_district],
        height=HEIGHT,
        width=WIDTH,
    )


# TODO: Make a separatre funtion to update map
if red_ratings and blue_ratings:
    map = generating_circles(map=map, df=df_cusine_district, color="ratings_color")

elif red_ratings and not blue_ratings:
    df_red = df_cusine_district[df_cusine_district["ratings_color"] == "orange"]
    heatmap_red_ratings = df_red[["lat", "lng", "rating"]]
    map = generating_circles(map=map, df=df_red, color="ratings_color")

elif blue_ratings and not red_ratings:
    df_blue = df_cusine_district[df_cusine_district["ratings_color"] == "blue"]
    heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]
    map = generating_circles(map=map, df=df_blue, color="ratings_color")
else:
    map = generating_circles(map=map, df=df_cusine_district, color="ratings_color")

folium.LayerControl().add_to(map)
folium_static(map)

# Getting information from global dataframe

# Making list of clean cuisine for global choices
cuisine_list = df["foodType"].value_counts().index.tolist()
cuisine_list = [
    cuisine
    for cuisine in cuisine_list
    if cuisine not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]

df_top_cuisine = df.loc[df["foodType"].isin(cuisine_list[0:10])]
if len(cuisine_list) < 10:
    df_top_cuisine = df_top_cuisine.loc[df_top_cuisine["foodType"].isin(cuisine_list)]
else:
    df_top_cuisine = df_top_cuisine.loc[
        df_top_cuisine["foodType"].isin(cuisine_list[0:10])
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
stats_cuisine = update_stats_per_cuisine(
    df_copy_for_stats, selected_cuisine, rating_cutoff, popularity_cutoff
)
five_most_common_cuisines = list(stats_cuisine["cuisine"][0:5])
five_most_common_percent = list(stats_cuisine["%_all_restaurants_in_Berlin"] * 100)[0:5]
number_cuisine = round(list(stats_cuisine["number_restaurants_in_Berlin"])[0])
percent_good_cuisine = list(stats_cuisine["%_considered_good"] * 100)[0]
percent_of_all = list(stats_cuisine["%_all_restaurants_in_Berlin"] * 100)[0]

best_rated_cuisines = update_stats_per_cuisine(
    df_copy_for_stats, "All", rating_cutoff, popularity_cutoff
)

best_rated_cuisines_df = best_rated_cuisines.sort_values(
    by=["%_considered_good"], ascending=False
)
best_rated = best_rated_cuisines_df[
    ~best_rated_cuisines_df["cuisine"].isin(CUISINE_OPTIONS)
]
best_rated_3_cuisines = list(best_rated["cuisine"])[0:3]
best_rated_3_perc = list(best_rated["%_considered_good"] * 100)[0:3]

berlin_cuisine = stats_cuisine.iloc[0]["number_restaurants_in_Berlin"]
berlin_good_cuisine = stats_cuisine.iloc[0]["%_considered_good"]

# hoods stats
stats_hoods = update_stats_per_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)
most_restaurants = stats_hoods.iloc[0]["district"]
most_restaurants_perc = round(stats_hoods.iloc[0]["%_all_berlin_restaurants"] * 100)
best_hood = stats_hoods.sort_values(by=["%_all_good_restaurants"], ascending=False)
best_district = best_hood.iloc[0]["district"]
best_district_per = round(best_hood.iloc[0]["%_all_good_restaurants"] * 100)

# hoods and cuisine stats
stats_hoods_cuisine = update_stats_per_hood_and_cuisine(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)
main_cuisine_per_hood = list(
    stats_hoods_cuisine[stats_hoods_cuisine["district"] == selected_cuisine]["cuisine"][
        0:5
    ]
)
percent_main_cuisine = list(
    stats_hoods_cuisine[stats_hoods_cuisine["district"] == selected_district][
        "%_restaurants_in_district"
    ][0:5]
    * 100
)
num_cuisine_per_hood = stats_hoods_cuisine


stats_cuisine_hoods = update_stats_per_cuisine_and_hood(
    df_copy_for_stats, rating_cutoff, popularity_cutoff
)

if selected_district == "All" and selected_cuisine == "All":
    all_district_all_cuisines(
        total_number_of_restaurants=total_num_of_restaurants,
        number_of_good_restaurants=number_of_good_restaurants,
        five_most_common_cuisines=five_most_common_cuisines,
        five_most_common_percent=five_most_common_percent,
    )

# TODO: Update all cases properly
# elif selected_district == "All" and selected_cuisine != "All":
#     all_district_selected_cuisine(
#         stats_hoods_cuisine=stats_hoods_cuisine,
#         stats_cuisine_hoods=stats_cuisine_hoods,
#         options_cuisine=selected_cuisine,
#         number_cuisine=number_cuisine,
#         percent_good_cuisine=percent_good_cuisine,
#         percent_of_all=percent_of_all,
#         best_rated_3_cuisines=best_rated_3_cuisines,
#         best_rated_3_perc=best_rated_3_perc,
#     )
# elif selected_district != "All" and selected_cuisine == "All":
#     selected_district_all_cuisine(
#         stats_hoods=stats_hoods,
#         options_district=selected_district,
#         main_cuisine_per_hood=main_cuisine_per_hood,
#         percent_main_cuisine=percent_main_cuisine,
#         total_num_of_restaurants=total_num_of_restaurants,
#         number_of_good_restaurants=number_of_good_restaurants,
#         most_restaurants=most_restaurants,
#         most_restaurants_perc=most_restaurants_perc,
#         best_district=best_district,
#         best_district_per=best_district_per,
#         five_most_common_cuisines=five_most_common_cuisines,
#         five_most_common_percent=five_most_common_percent,
#     )
# else:
#     selected_district_selected_cuisine(
#         stats_hoods_cuisine=stats_hoods_cuisine,
#         stats_cuisine_hoods=stats_cuisine_hoods,
#         options_district=selected_district,
#         options_cuisine=selected_cuisine,
#         berlin_cuisine=berlin_cuisine,
#         berlin_good_cuisine=berlin_good_cuisine,
#     )

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
df_local = df_local[df_local["userRatingsTotal"] > popularity_cutoff]

# In case of address input
st.header("Your closest competitors")

(
    most_frq_priceLevel,
    avg_rating,
    best_competitor,
    cuisine_distribution,
    good_restaurants_per,
    bad_restaurants_per,
) = neighbours_stats(df_cusine_district)

# Capitalising names
best_competitor_capitalise = []
for competitor in best_competitor.split():
    try:
        best_competitor_capitalise.append(competitor.capitalize())
    except Exception:
        best_competitor_capitalise.append(competitor)
best_competitor = " ".join(best_competitor_capitalise)

display_additional_stats(
    most_frq_priceLevel=most_frq_priceLevel,
    avg_rating=avg_rating,
    good_restaurants_per=good_restaurants_per,
    best_competitor=best_competitor,
)

# Starting with second map, finding best places to open a restaurant
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
        boxes=local_box, df=df_local_lat_lng
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
cuisine_list_local = df_local["foodType"].value_counts().index.tolist()
cuisine_list_local = [
    cuisine
    for cuisine in cuisine_list_local
    if cuisine not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]

if len(cuisine_list_local) < 10:
    df_top_cuisine_local = df_local.loc[df_local["foodType"].isin(cuisine_list_local)]
else:
    df_top_cuisine_local = df_local.loc[
        df_local["foodType"].isin(cuisine_list_local[0:10])
    ]
