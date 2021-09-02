from streamlit_folium import folium_static
from next_restaurant.german_to_english import *
from next_restaurant.cuisine_info import *
from next_restaurant.parameters import *
from next_restaurant.functions_for_df import *
from next_restaurant.district import *
from next_restaurant.stats import *
from next_restaurant.suggestion_feature import *
from next_restaurant.local_search_coordinates import *

import streamlit as st
import folium
import pandas as pd
import geocoder
import seaborn as sns
import matplotlib.pyplot as plt


# import ast
# import time
# import openrouteservice
# import json
# import datetime
# import geocoder
# import requests

## SET LAYOUT
st.set_page_config(page_title="NEXT RESTAURANT",
                   initial_sidebar_state='expanded')

# Trying to make it colorfull
# st.markdown(f'<p style="background-color:#0066cc;color:#33ff33;font-size:24px;border-radius:2%;">Hello My name is Shanu Dengre</p>', unsafe_allow_html=True)

# colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

# for color in colors:
#     st.markdown(f"<{color}>{color}</{color}>", unsafe_allow_html=True)

## LOAD THE DATAFRAME
df = pd.read_csv("raw_data//clean_dataframe_1.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Capitalize food_types for the selection dropdown
df = change_main_food_types(df)

df["food_type_1_english"] = df["food_type"].str.capitalize()

# makes copies of the df for the second plot and the stats
df_copy = df.copy()
df_copy_for_stats = df.copy()

## MAIN PAGE
# Title and subheader
st.title("Next Restaurant")
st.header('Browse through the restaurants in Berlin')

st.markdown('#### <span style="color:blue">**Blue circles**</span>: High rated restaurants', unsafe_allow_html=True)
st.markdown('#### <span style="color:red">**Red circles**</span>: Low rated restaurants', unsafe_allow_html=True)
st.markdown('###### ')
## SIDEBAR

# Title
st.sidebar.markdown('''# Find the best place to open your restaurant''')

# Cuisine selection

st.sidebar.subheader("Do you already have a type of cuisine in mind?")

selected_cuisine = [i for i in cuisine_num_wise_clean_data_frame_capitalise
 if i not in cuisine_clean_data_frame_to_remove]

options_cuisine = st.sidebar.selectbox('Select a type of cuisine',
                                       selected_cuisine)

if options_cuisine != "All":
    df = df[df["food_type_1_english"] == options_cuisine]

# District selection
st.sidebar.subheader("Do you already have a district in mind?")

options_district = st.sidebar.selectbox(
    'Select a district', list_districts)

if options_district != "All":
    df = df[df["district"] == options_district]

# input popularity and ratings
st.sidebar.subheader("What would you consider a \"good\" restaurant\
                     based on customers ratings?"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     )

rating_cutoff = st.sidebar.slider('Please select a rating',
                                  min_value=2.,
                                  max_value=5.,
                                  step=0.1,
                                  value=4.5)

# user popularity cutoff

popularity_cutoff = st.sidebar.slider('Please select a number of rating',
                                      min_value=0,
                                      max_value=2000,
                                      step=1,
                                      value=40)

# Conditions for generating maps
blue_ratings = st.sidebar.checkbox("Only show me good restaurants")
red_ratings = st.sidebar.checkbox("Only show me bad restaurants")

## POPULARITY AND RATINGS CUTOFFS
# Conditions for generating maps
blue_popular = st.sidebar.checkbox("Only show me popular restaurants")
red_popular = st.sidebar.checkbox("Only show me unpopular restaurants")

# Input an address
st.sidebar.subheader("Do you already have an address in mind?")

user_input = st.sidebar.text_input("Enter an address", "Mitte, Berlin")

g = geocoder.osm(user_input)

local_lat = g.osm["y"]
local_lng = g.osm["x"]

district = geocoder.osm(f"{options_district}, Berlin")
local_lat_district = district.osm["y"]
local_lng_district = district.osm["x"]
#st.sidebar.markdown("Coordinates corresponding to the address")
#st.sidebar.markdown(f"Local lat: {local_lat}")
#st.sidebar.markdown(f"Local lng: {local_lng}")

# Number of restaurants to be considered locally
number_of_nearby_restaurant_to_be_considered = st.sidebar.slider('How many nearest restaurants would you like to see?',
                            min_value = 5,
                            max_value = 100,
                            step=5,
                            value = 40)

# Determining color for ratings cutoff
df["ratings_color"] = df["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Chopping data frame with respect to popularity cutoff
df = df[df["user_ratings_total"]>popularity_cutoff]

## FIRST MAP
# Display the map
if options_district == "All":
    m = map_instance(zoom = zoom, initial_location=Berlin_center, width=width, height=height)
else:
    m = map_instance(zoom = 14, initial_location=[local_lat_district, local_lng_district], width=width, height=height)

if red_ratings and blue_ratings:
    m = generating_circles(m, df, "ratings_color")

elif red_ratings and not blue_ratings:
    df_red = df[df["ratings_color"] == "red"]
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
cuisine_list = [i for i in cuisine_list if i not in cuisine_clean_data_frame_to_remove]

df_top_cuisine = df.loc[df["food_type_1_english"].isin(cuisine_list[0:10])]
if len(cuisine_list) < 10:
    df_top_cuisine = df_top_cuisine.loc[df_top_cuisine["food_type_1_english"].isin(cuisine_list)]
else:
    df_top_cuisine = df_top_cuisine.loc[df_top_cuisine["food_type_1_english"].isin(cuisine_list[0:10])]


## INFO BOX BELOW THE MAP

st.header("Key points")
st.subheader("Consider this information when chosing a location for your restaurant:")

# general stats about Berlin

percent_of_good_restaurants = percent_of_good_restaurants(
    df_copy_for_stats, rating_cutoff, popularity_cutoff)
total_num_of_restaurants = len(df_copy_for_stats)
number_of_good_restaurants = number_of_good_restaurants(
    df_copy_for_stats, rating_cutoff, popularity_cutoff)

# cuisine stats
stats_cuisine = stats_per_cuisine(df_copy_for_stats, options_cuisine,
                                  rating_cutoff, popularity_cutoff)
five_most_common_cuisines = list(stats_cuisine['cuisine'][0:5])
five_most_common_percent = list(stats_cuisine['%_all_restaurants_in_Berlin']*100)[0:5]
number_cuisine = round(list(stats_cuisine['number_restaurants_in_Berlin'])[0])
percent_good_cuisine = list(stats_cuisine['%_considered_good']*100)[0]
percent_of_all = list(stats_cuisine['%_all_restaurants_in_Berlin']*100)[0]

best_rated_cuisines = stats_per_cuisine(df_copy_for_stats, 'All',
                                        rating_cutoff, popularity_cutoff)

best_rated_cuisines_df = best_rated_cuisines.sort_values(by=['%_considered_good'], ascending=False)
best_rated = best_rated_cuisines_df[~best_rated_cuisines_df['cuisine'].isin(cuisine_to_remove)]
best_rated_3_cuisines = list(best_rated['cuisine'])[0:3]
best_rated_3_perc = list(best_rated['%_considered_good'] * 100)[0:3]

berlin_cuisine = stats_cuisine.iloc[0]['number_restaurants_in_Berlin']
berlin_good_cuisine = stats_cuisine.iloc[0]['%_considered_good']

# hoods stats
stats_hoods = stats_per_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)
most_restaurants = stats_hoods.iloc[0]['district']
most_restaurants_perc = round(stats_hoods.iloc[0]['%_all_berlin_restaurants']*100)
best_hood = stats_hoods.sort_values(by=['%_all_good_restaurants'],ascending=False)
best_district = best_hood.iloc[0]['district']
best_district_per = round(best_hood.iloc[0]['%_all_good_restaurants']*100)

# hoods and cuisine stats
stats_hoods_cuisine = stats_per_hood_and_cuisine(df_copy_for_stats,
                                                 rating_cutoff,
                                                 popularity_cutoff)
main_cuisine_per_hood = list(stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]['cuisine'][0:5])
percent_main_cuisine = list(
stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]['%_restaurants_in_district'][0:5]*100)
num_cuisine_per_hood = stats_hoods_cuisine


stats_cuisine_hoods =stats_per_cuisine_and_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)

# text to be displayed:

if options_district == 'All' and options_cuisine == 'All':

<<<<<<< HEAD
    st.markdown(f"There are {total_num_of_restaurants} restaurants \
    in Berlin, among which {number_of_good_restaurants} \
    good restaurants. \
    The three most common types of cuisines are \
    {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}% of all restaurants),\
    {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}% of all restaurants),\
    {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}% of all restaurants)."
    )
    st.markdown("See more stats [here]")
=======
    st.write(f"\
    - There are {total_num_of_restaurants} restaurants in Berlin, \
    {number_of_good_restaurants} of them are good restaurants "                                                                                                                                                                                             )
    st.write(f"\
    - The three most common type of cuisines are\
    {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}% of all restaurants),\
    {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}% of all restaurants),\
    {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}% of all restaurants)."
             )

    st.write('For more information, select a district and a cuisine type.')

>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb
elif options_district == 'All' and options_cuisine != 'All':
    main_hood_per_cuisine = list(stats_cuisine_hoods[stats_hoods_cuisine['cuisine']
                                                     == options_cuisine.lower()]['district'][0:5])
    p = list(stats_cuisine_hoods[stats_cuisine_hoods['cuisine']
                                                     == options_cuisine.lower()]['percent_all_restaurants_of_berlin'][0:5]*100)

<<<<<<< HEAD
    st.markdown(f"There are {number_cuisine} **{options_cuisine}** restaurants\
    in Berlin, among which {percent_good_cuisine}% \
    good restaurants. **{options_cuisine}** restaurants represents {percent_of_all}%\
    of all restaurants in Berlin. **{options_cuisine}** restaurants are mostly located in\
=======
    st.write(f"\
        - There are {number_cuisine} {options_cuisine} restaurants in Berlin,\
        {percent_good_cuisine}% are good restaurants"                                                                                                                                                               )
    st.write(f"\
        - {options_cuisine} restaurants represents {round(percent_of_all)}% \
            of all Berlin restaurants"                                                                                                                                                        )
    st.write(f"\
        - {options_cuisine} restaurants are mostly located in \
>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb
    {main_hood_per_cuisine[0]} ({round(p[0])}%), {main_hood_per_cuisine[1]} ({round(p[1])}%) and \
    {main_hood_per_cuisine[2]} ({round(p[2])}%)"                                                                                                                                                                                                )

    st.write(f"In Berlin, the type of restaurants which have the best ratings are:\
    {best_rated_3_cuisines[0]} ({round(best_rated_3_perc[0])}%),\
    {best_rated_3_cuisines[1]} ({round(best_rated_3_perc[1])}%) and \
    {best_rated_3_cuisines[2]} ({round(best_rated_3_perc[1])}%)"                                                                                                                                                                                                )

<<<<<<< HEAD
    st.markdown("See more stats [here]")
=======
>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb
elif options_district != 'All' and options_cuisine == 'All':
    stats_hoods_hood = stats_hoods[stats_hoods['district']== options_district]

    num_restaurants = stats_hoods_hood.iloc[0]['number_of_restaurants']
    num_good_restaurants = stats_hoods_hood.iloc[0]['number_good_restaurants']
    percentage_good_restaurants_hood = round(stats_hoods_hood.iloc[0]['%_all_good_restaurants']*100)

<<<<<<< HEAD
    st.markdown(f"There are {num_restaurants} restaurants \
    in {options_district}, among which {num_good_restaurants} \
    good restaurants. \
    {percentage_good_restaurants_hood} % of the best restaurants in Berlin are located in this district.\
    The most common type of cuisine in this neighbordhood are: \
=======
    st.write(f"\
    - There are {num_restaurants} restaurants in {options_district}, \
    {round((num_good_restaurants/num_restaurants)*100)}% of them are good "                                                                                                                                                                                                                                 )
    st.write(f"\
        - {options_district} has {percentage_good_restaurants_hood} % of the best restaurants in Berlin"                                                                                                                                                                                                                                                                                                                        )
    st.write(f"\
    - Most common type of cuisine in {options_district}:\
>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb
    {main_cuisine_per_hood[0].capitalize()}, ({round(percent_main_cuisine[0])}%) \
    {main_cuisine_per_hood[1].capitalize()} ({round(percent_main_cuisine[1])}%) \
    and {main_cuisine_per_hood[2].capitalize()} ({round(percent_main_cuisine[2])}%)."
             )
<<<<<<< HEAD
    st.markdown("See more stats [here]")
=======

    st.write(f"In Berlin overall, there are: {total_num_of_restaurants} restaurants \
    {number_of_good_restaurants} of them are good"                                                                                                                                                      )
    st.write(f"- {most_restaurants} has most restaurants in Berlin ({most_restaurants_perc}%) \
    and {best_district} has most of the good restaurants ({best_district_per}%)"                                                                                                                                                                                                                                                )
    st.write(f"The most common types of cuisines in Berlin are:\
     {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}%), \
     {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}%) and \
     {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}%)"                                                                                                                                                                                                                                                                           )

>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb
else:
    stats_hoods_cuisine_hood = stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]
    stats_hoods_cuisine_cuisine = stats_hoods_cuisine_hood[stats_hoods_cuisine_hood['cuisine'] == options_cuisine.lower()]
    num = stats_hoods_cuisine_cuisine.iloc[0]['count']
    good = round(stats_hoods_cuisine_cuisine.iloc[0]['%_considered_good']*100)
<<<<<<< HEAD
    percent_of_all = round(stats_hoods_cuisine_cuisine.iloc[0]['percent_all_restaurants_of_berlin']*100)

    st.markdown(f"There are {num} **{options_cuisine}** restaurants in {options_district} based on your selected criterias.")
    st.markdown(f"**{good}**% are good restaurants.")
    st.markdown(f"**{percent_of_all}**% of the all the **{options_cuisine}** restaurants of Berlin are located in {options_district}.")
=======
    percent_of_all = round(stats_hoods_cuisine_cuisine.iloc[0]['%_all_good_restaurants_for_this_cuisine_in_berlin']*100)

    stats_hoods_good = stats_cuisine_hoods[
        stats_cuisine_hoods['cuisine'] == options_cuisine.lower()].sort_values(
            by=['percent_all_restaurants_of_berlin'], ascending=False)
    name = stats_hoods_good.iloc[0]['district']
    perce = round(stats_hoods_good.iloc[0]['percent_all_restaurants_of_berlin']*100)
    stats_hoods_2 = stats_cuisine_hoods[
        stats_cuisine_hoods['cuisine'] ==
        options_cuisine.lower()].sort_values(by=['%_all_good_restaurants_for_this_cuisine_in_berlin'],ascending=False)
    name_2 = stats_hoods_2.iloc[0]['district']
    perce_2 = round(stats_hoods_2.iloc[0]['%_all_good_restaurants_for_this_cuisine_in_berlin']*100)

    st.write(f" - There are {num} {options_cuisine.capitalize()} restaurants in {options_district}, \
        {good}% of them are good restaurants"                                                                                                                                                                                    )
    st.write(f" - {percent_of_all}% of the all the {options_cuisine.capitalize()} restaurants of Berlin \
    are located in {options_district} "                                                                                                                                                            )

    st.write(f" - In Berlin overall, there are {berlin_cuisine} {options_cuisine.capitalize()} restaurants,\
 {round(berlin_good_cuisine*100)}% of them are good "                                                                                                                                                                    )
    st.write(f" - {name} has most {options_cuisine.capitalize()} restaurants in Berlin ({perce}%)")
    st.write(f" - {name_2}  has most of the good {options_cuisine.capitalize()} restaurants ({perce_2}%)")
>>>>>>> d03285fa0cae65ef6673bd8915939ddf9c5794cb

    st.markdown("See more stats [here]")

## MAP ZOOMED IN

df_local = k_neighbours_df(df_copy, local_lat, local_lng, n_restaurants=number_of_nearby_restaurant_to_be_considered)

# Determining color for ratings cutoff
df_local["ratings_color"] = df_local["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Chopping data frame with respect to popularity cutoff
df_local = df_local[df_local["user_ratings_total"]>popularity_cutoff]

# In case of address input
st.header("Your closest competitors")

most_frq_price_level, avg_rating, best_competitor, cuisine_distribution, good_restaurants_per, bad_restaurants_per = neighbours_stats(df)

# Capitalising names
best_competitor_capitalise = []
for i in best_competitor.split():
    # i = str(i)
    # st.markdown(i)
    try:
        best_competitor_capitalise.append(i.capitalize())
        # st.markdown("true")
    except:
        best_competitor_capitalise.append(i)
best_competitor =  " ".join(best_competitor_capitalise)

# Printing local stats
st.markdown(f'Based on the address you provided, your top potential competitor would be: **{best_competitor}**.')
st.markdown(f'Most of them have price level **{most_frq_price_level}**.')
st.markdown(f'Their average rating is **{round(avg_rating, 2)}**, and **{good_restaurants_per}%** of restaurants are considered as good.')


# Making heading for the suggestion part
st.header('Our suggestions in the area')

# Adding description for the marker.
st.markdown('#### <span style="color:red">*Red marker*</span>: center of low rated resaturants of the area', unsafe_allow_html=True)
st.markdown('#### <span style="color:blue">*Blue marker*</span>: center of high rated resaturants of the area', unsafe_allow_html=True)
st.markdown('#### <span style="color:green">*Green marker*</span>: furthest locations from all restaurants in the area', unsafe_allow_html=True)
st.markdown("###### ")

# Estimating centroid bad and centroid good
center_bad_center_good = calc_centers(df_local, rating_cutoff)

if type(center_bad_center_good) == dict:
# n = folium.Figure(width=100, height=100)
    first_key = next(iter(center_bad_center_good))
    o = map_instance(zoom=15, initial_location=[center_bad_center_good[first_key][0], center_bad_center_good[first_key][1]],
                        width=width, height=height)
else:
    o = map_instance(zoom=15, initial_location=[center_bad_center_good[1][0], center_bad_center_good[1][1]],
                            width=width, height=height)

# Making circles around the popularity and color coding it.
o = generating_circles(o, df_local, "ratings_color")

# Making a suggestion based on good center and bad center
# suggested_lat = (0.9)*center_bad[0] + (0.1)*center_good[0]
# suggested_lng = (0.9)*center_bad[1] + (0.1)*center_good[1]

# number of suggestions based on distance
# st.sidebar.markdown("Rating cutoff")
suggestion_number_distance = st.slider('Number of green markers',
                            min_value = 1,
                            max_value = 10,
                            step=1,
                            value = 3)

# Dataframe with just latitudes and longitutes. They are to generate suggestions.
df_local_lat_lng = df_local[["lat", "lng", "distance"]]
# st.dataframe(df_local_lat_lng.head())

# Coordinates inside a local box
local_box = generating_circular_coordinates(df = df_local_lat_lng,
                                            lat = local_lat,
                                            lng = local_lng)
# st.markdown(len(local_box))

# Creating best location lists
best_location_based_on_distance_list = []
for i in range(suggestion_number_distance):
    # st.markdown(i)
    best_location_based_on_distance = locating_best_place_based_on_distance(box = local_box, df = df_local_lat_lng)
    best_location_based_on_distance_list.append(best_location_based_on_distance)
    to_append = [best_location_based_on_distance[0], best_location_based_on_distance[1], 0]
    df_local_lat_lng.loc[len(df_local_lat_lng.index)] = to_append


if type(center_bad_center_good) == dict:
    if first_key == "center_bad":
        color = "red"
    else:
        color = "darkblue"
    folium.Marker(location=[center_bad_center_good[first_key][0], center_bad_center_good[first_key][1]],
                popup="Center of low rated restarants",
                icon=folium.Icon(color=color)).add_to(o)
else:
    folium.Marker([center_bad_center_good[1][0], center_bad_center_good[1][1]],
                popup="Center of high rated restarants",
                icon=folium.Icon(color="darkblue")).add_to(o)
    folium.Marker([center_bad_center_good[0][0], center_bad_center_good[0][1]],
            popup="Center of low rated restarants",
            icon=folium.Icon(color="red")).add_to(o)

number = 1
for i in best_location_based_on_distance_list:
    folium.Marker(i,
                popup=f"Optimum location number {number} based on distance from nearest neighbour restaurant",
                icon=folium.Icon(color="darkgreen")).add_to(o)
    number+=1

folium_static(o)

# Making list of clean cuisine for local choices
cuisine_list_local = df_local["food_type_1_english"].value_counts().index.tolist()
cuisine_list_local = [i for i in cuisine_list_local if i not in cuisine_clean_data_frame_to_remove]

if len(cuisine_list_local) < 10:
    df_top_cuisine_local = df_local.loc[df_local["food_type_1_english"].isin(cuisine_list_local)]
else:
    df_top_cuisine_local = df_local.loc[df_local["food_type_1_english"].isin(cuisine_list_local[0:10])]


# fig, ax1 = plt.subplots()
# ax1 = sns.countplot(x = "food_type_1_english",
#                     data=df_top_cuisine_local,
#                     order = df_top_cuisine_local["food_type_1_english"].value_counts().index)

# # for p in ax1.patches:
# #     ax1.annotate('%{:.1f}'.format(p.get_height()), (p.get_x()+0.1, p.get_height()+50))

# st.subheader(f'Popular cusines locally')
# # ax.set_title("Food type")
# # ax.set_label(False)
# ax1.xaxis.label.set_visible(False)
# ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 30)
# st.pyplot(fig)

# Count plot general
#sns.set_theme(style="darkgrid")
#fig, ax = plt.subplots()
#ax = sns.countplot(x = "food_type_1_english",
#data=df_top_cuisine,
#order = df_top_cuisine["food_type_1_english"].value_counts().index)
#ax.set_title("Food type")
#ax.set_label(False)
#ax.xaxis.label.set_visible(False)
#ax.set_xticklabels(ax.get_xticklabels(), rotation = 30)
#st.pyplot(fig)

# Heading for second map plot
#st.header('Distribution of restaurants in Berlin based on number of user reviews')

# n = folium.Figure(width=100, height=100)
#n = map_instance()

#if red_popular and blue_popular:
# Making circles around the popularity and color coding it.
#n = generating_circles(n, df_copy, "popularity_color")

#elif blue_popular and not red_popular:
#df_blue_2 = df_copy[df_copy["popularity_color"] == "blue"]
#n = generating_circles(n, df_blue_2, "popularity_color")

#elif red_popular and not blue_popular:
#df_red_2 = df_copy[df_copy["popularity_color"] == "red"]
# heatmap_blue_ratings = df_blue[["lat", "lng", "rating"]]
#n = generating_circles(n, df_red_2, "popularity_color")

#else:
#n = generating_circles(n, df_copy, "popularity_color")

#with st:
#folium.LayerControl().add_to(n)
#folium_static(n)

# st.header("Global and local area comparision")

# st.markdown(f"{most_frq_price_level}, {avg_rating}, {cuisine_distribution}")

# st.markdown(f"{best_competitor}")


