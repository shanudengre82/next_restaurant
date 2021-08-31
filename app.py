from streamlit_folium import folium_static
from next_restaurant.german_to_english import *
from next_restaurant.cuisine_info import cuisine_num_wise, cuisine_most_frequent, cuisine_num_wise_clean_data_frame_capitalise
from next_restaurant.parameters import *
from next_restaurant.functions_for_df import *
from next_restaurant.district import *
from next_restaurant.stats import *

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

## LOAD THE DATAFRAME

df = pd.read_csv("raw_data//clean_dataframe.csv")

# Determining the popularity based on number of ratings and color for a separator
df["popularity_res"] = df["user_ratings_total"].apply(popularity)

# Capitalize food_types for the selection dropdown
df["food_type_1_english"] = df["food_type"].str.capitalize()

# makes copies of the df for the second plot and the stats
df_copy = df.copy()
df_copy_for_stats = df.copy()


## MAIN PAGE

# Title and subheader
st.title("Next Restaurant")
st.header('Browse through the restaurants in Berlin')

# Display the map
m = map_instance()


## SIDEBAR

# Title
st.sidebar.markdown('''# Find the best place to open your restaurant''')

# Cuisine selection

st.sidebar.subheader("Do you already have a type of cuisine in mind?")

options_cuisine = st.sidebar.selectbox('Select a type of cuisine',
                                cuisine_num_wise_clean_data_frame_capitalise)

if options_cuisine != "All":
    df = df[df["food_type_1_english"] == options_cuisine]

# District selection

st.sidebar.subheader("Do you already have a district in mind?")

options_district = st.sidebar.selectbox(
    'Select a district', list_districts)

if options_district != "All":
    df = df[df["district"] == options_district]

# Input an address

st.sidebar.subheader("Do you already have an address in mind?")

user_input = st.sidebar.text_input("Enter an address", "Thomasiusstrasse 11, Berlin")

g = geocoder.osm(user_input)

# input popularity and ratings

st.sidebar.subheader("What would you consider a \"good\" restaurant\
                     based on customers ratings?"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          )

rating_cutoff = st.sidebar.slider('Please select a rating',
                                  min_value=2.,
                                  max_value=5.,
                                  step=0.1,
                                  value=4.6)

# user popularity cutoff
popularity_cutoff = st.sidebar.slider('Please select a number of rating',
                                      min_value=0,
                                      max_value=2000,
                                      step=1,
                                      value=50)

# Conditions for generating maps
blue_ratings = st.sidebar.checkbox("Only show me good restaurants")
red_ratings = st.sidebar.checkbox("Only show me bad restaurants")
# Conditions for generating maps
blue_popular = st.sidebar.checkbox("Only show me popular restaurants")
red_popular = st.sidebar.checkbox("Only show me unpopular restaurants")


## POPULARITY AND RATINGS CUTOFFS

# Determining color for ratings cutoff
df["ratings_color"] = df["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Chopping data frame with respect to popularity cutoff
df = df[df["user_ratings_total"]>popularity_cutoff]


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


# Determining color based on popularity cutoff
df_copy["popularity_color"] = df_copy["user_ratings_total"].apply(lambda x: "red" if x < popularity_cutoff else "blue")

df_top_cuisine = df_copy.loc[df_copy["food_type_1_english"].isin(cuisine_most_frequent)]


## INFO BOX BELOW THE MAP

st.header("Key points")
st.subheader("Consider this information when chosing a location for your restaurant:")

# general stats about Berlin

percent_of_good_restaurants = percent_of_good_restaurants(
    df_copy_for_stats, rating_cutoff, popularity_cutoff)
total_num_of_restaurants = len(df_copy_for_stats)
number_of_good_restaurants = number_of_good_restaurants(
    df, rating_cutoff, popularity_cutoff)

# cuisine stats
stats_cuisine = stats_per_cuisine(df_copy_for_stats, options_cuisine,
                                  rating_cutoff, popularity_cutoff)
five_most_common_cuisines = list(stats_cuisine['cuisine'][0:5])
five_most_common_percent = list(stats_cuisine['%_all_restaurants_in_Berlin']*100)[0:5]
number_cuisine = round(list(stats_cuisine['number_restaurants_in_Berlin'])[0])
percent_good_cuisine = list(stats_cuisine['%_considered_good']*100)[0]
percent_of_all = list(stats_cuisine['%_all_restaurants_in_Berlin']*100)[0]

# hoods stats
stats_hoods = stats_per_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)

# hoods and cuisine stats
stats_hoods_cuisine = stats_per_hood_and_cuisine(df_copy_for_stats,
                                                 rating_cutoff,
                                                 popularity_cutoff)
main_cuisine_per_hood = list(stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]['cuisine'][0:5])
percent_main_cuisine = list(
stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]['%_restaurants_in_district'][0:5]*100)
num_cuisine_per_hood = stats_hoods_cuisine
stats_hoods_cuisine =stats_per_cuisine_and_hood(df_copy_for_stats, rating_cutoff,
                                             popularity_cutoff)

# text to be displayed:

if options_district == 'All' and options_cuisine == 'All':

    st.write(f"There are {total_num_of_restaurants} restaurants\
    in Berlin,among which {number_of_good_restaurants} \
    good restaurants. \
    The three most common type of cuisines are \
    {five_most_common_cuisines[0].capitalize()} ({round(five_most_common_percent[0])}% of all restaurants),\
    {five_most_common_cuisines[1].capitalize()} ({round(five_most_common_percent[1])}% of all restaurants),\
    {five_most_common_cuisines[2].capitalize()} ({round(five_most_common_percent[2])}% of all restaurants)."
    )
elif options_district == 'All' and options_cuisine != 'All':
    main_hood_per_cuisine = list(stats_hoods_cuisine[stats_hoods_cuisine['cuisine']
                                                     == options_cuisine.lower()]['district'][0:5])
    p = list(stats_hoods_cuisine[stats_hoods_cuisine['cuisine']
                                                     == options_cuisine.lower()]['percent_all_restaurants_of_berlin'][0:5]*100)

    st.write(f"There are {number_cuisine} {options_cuisine} restaurants\
    in Berlin, among which {percent_good_cuisine}% \
    good restaurants. {options_cuisine} restaurants represents {percent_of_all}%\
    of all restaurants in Berlin. {options_cuisine} restaurants are mostly located in\
    {main_hood_per_cuisine[0]} ({round(p[0])}%), {main_hood_per_cuisine[1]} ({round(p[1])}%) and \
    {main_hood_per_cuisine[2]} ({round(p[2])}%)")
elif options_district != 'All' and options_cuisine == 'All':
    stats_hoods_hood = stats_hoods[stats_hoods['district']== options_district]

    num_restaurants = stats_hoods_hood.iloc[0]['number_of_restaurants']
    num_good_restaurants = stats_hoods_hood.iloc[0]['number_good_restaurants']
    percentage_good_restaurants_hood = round(stats_hoods_hood.iloc[0]['%_all_good_restaurants']*100)

    st.write(f"There are {num_restaurants} restaurants \
    in {options_district}, among which {num_good_restaurants} \
    good restaurants. \
    {percentage_good_restaurants_hood} % of the best restaurants in Berlin are located in this district.\
    The most common type of cuisine in this neighbordhood are: \
    {main_cuisine_per_hood[0].capitalize()}, ({round(percent_main_cuisine[0])}%) \
    {main_cuisine_per_hood[1].capitalize()} ({round(percent_main_cuisine[1])}%) \
    and {main_cuisine_per_hood[2].capitalize()} ({round(percent_main_cuisine[2])}%)."
             )
else:
    stats_hoods_cuisine_hood = stats_hoods_cuisine[stats_hoods_cuisine['district'] == options_district]
    stats_hoods_cuisine_cuisine = stats_hoods_cuisine_hood[stats_hoods_cuisine_hood['cuisine'] == options_cuisine.lower()]
    num = stats_hoods_cuisine_cuisine.iloc[0]['count']
    good = round(stats_hoods_cuisine_cuisine.iloc[0]['%_considered_good']*100)
    percent_of_all = round(stats_hoods_cuisine_cuisine.iloc[0]['percent_all_restaurants_of_berlin']*100)

    st.write(f"There are {num} {options_cuisine} restaurants \
    in {options_district}, among which {good}% are good restaurants. \
    {percent_of_all}% of the all the {options_cuisine} restaurants of Berlin \
    are located in {options_district}." )

## MAP ZOOMED IN
# In case of address input

st.header("Your closest competitors")

st.subheader('Based on this address, your potential closest\
competitors would be:\
')
st.write ("X restaurants, mostly X type of food.\
    Their average rating is X, and X are good restaurants. ")

local_lat = g.osm["y"]
local_lng = g.osm["x"]

# n = folium.Figure(width=100, height=100)
o = map_instance(zoom=12, initial_location=[local_lat, local_lng],
                        width=500, height=300)

df_local = nearby_restaurants(df_copy, local_lat, local_lng)

# Determining color for ratings cutoff
df_local["ratings_color"] = df_local["rating"].apply(lambda x: "red" if x < rating_cutoff else "blue")

# Making circles around the popularity and color coding it.
o = generating_circles(o, df_local, "ratings_color")

folium.LayerControl().add_to(o)
folium_static(o)






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
