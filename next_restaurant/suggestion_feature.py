import pandas as pd 
import math
import geocoder

#HOW TO USE#
""" 1. run the k_neighbours_df function with the data_df, the lat, lng of the choosen location and the number of restaurants to return 
2. with the resulting df of the k_neighbours_df function run the calc_centers function to get the center of the bad and good centers 
"""

#user_input = geocoder.osm('sonnenallee30')
#lat = user_input.latlng[0]
#lng = user_input.latlng[1]

def deg_to_rad(deg):
    """
    Function to convert radians to degree.
    """
    return deg * (math.pi/180)
def distance(lat1, lng1, lat2, lng2):
    """
    This function is based on Haversine formula to estimate distance based
    on 2 sets of latitude and longitude
    a = sin²(ΔlatDifference/2) + cos(lat1).cos(lat2).sin²(ΔlonDifference/2)
    c = 2.atan2(√a, √(1−a))
    d = R.c
    """
    delta_lat = deg_to_rad(lat1-lat2)
    delta_lng = deg_to_rad(lng1-lng2)
    a = ((math.sin(delta_lat/2))*(math.sin(delta_lat/2))) + (math.cos(deg_to_rad(lat1))
                                        *math.cos(deg_to_rad(lat2))
                                        *((math.sin(delta_lng/2))*(math.sin(delta_lng/2))))
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    R = 6371 # This is in km, and the results are also in Km
    d = R*c
    return d


# takes the df of restaurants and the lat,lng for the prefered user location and outputs a df of k nearest restaurants
def k_neighbours_df (df, lat, lng,n_restaurants):
    df['distance'] = ''
    for i in range(len(df)):
        df['distance'][i] = distance(lat, lng, df['lat'][i], df['lng'][i])
    return df.sort_values(by='distance')[:n_restaurants]


"""calculate the center of 'good' and 'bad' restaurants of the choosing location.
Good and bad restaurants are decided based on the rating"""

def calc_centers (df,rating):
    bad_rest = df[df['rating'] < rating ]
    good_rest =  df[df['rating'] >= rating]
    center_bad = ((bad_rest['rating'] * bad_rest['lat']).sum()/bad_rest['rating'].sum() ,
                  (bad_rest['rating'] * bad_rest['lng']).sum()/bad_rest['rating'].sum())
    center_good = ((good_rest['rating'] * good_rest['lat']).sum()/good_rest['rating'].sum() ,
                   (good_rest['rating'] * good_rest['lng']).sum()/good_rest['rating'].sum())
    return center_bad, center_good