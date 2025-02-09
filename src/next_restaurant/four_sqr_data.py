import requests
import pandas as pd


""" runs on a certain radius and for n runs starting form the city center lat, lng. returns a df and saves a df for each call in the function folder"""
categoryId = "4d4b7105d754a06374d81259"  # category Food


def get_four_sqr_api(client_id, client_secret, categoryId, runs, radius):
    url = "https://api.foursquare.com/v2/venues/explore"
    coordinates_list = (
        pd.read_csv("../raw_data/Berlin_coordinates_with_distances_index.csv")
        .sort_values(by="distance")
        .reset_index(drop=True)
    )
    df = pd.DataFrame(columns=["id", "name", "address", "lat", "lng", "category"])
    for i in range(runs):
        params = dict(
            client_id=client_id,
            client_secret=client_secret,
            v="20210824",
            ll=f"{coordinates_list.lat[i]},{coordinates_list.lng[i]}",
            categoryId=categoryId,
            limit=50,
            radius=radius,
        )
        response = requests.get(url=url, params=params, timeout=300).json()
        index = int(coordinates_list.iloc[i]["index"])
        pd.DataFrame(response).to_csv(
            f"./data/foursquare_berlin_coordinates_{index}.csv"
        )
        df_temp = pd.DataFrame(
            columns=["id", "name", "address", "lat", "lng", "category"]
        )
        for n in range(len(response["response"]["groups"][0]["items"])):
            four_sqr_id = response["response"]["groups"][0]["items"][n]["venue"]["id"]
            four_sqr_name = response["response"]["groups"][0]["items"][n]["venue"][
                "name"
            ]
            four_sqr_category = response["response"]["groups"][0]["items"][n]["venue"][
                "categories"
            ][0]["name"]
            four_sqr_address = " ".join(
                response["response"]["groups"][0]["items"][n]["venue"]["location"][
                    "formattedAddress"
                ]
            )
            four_sqr_lat = response["response"]["groups"][0]["items"][n]["venue"][
                "location"
            ]["lat"]
            four_sqr_lng = response["response"]["groups"][0]["items"][n]["venue"][
                "location"
            ]["lng"]
            df_temp.loc[len(df_temp)] = [
                four_sqr_id,
                four_sqr_name,
                four_sqr_address,
                four_sqr_lat,
                four_sqr_lng,
                four_sqr_category,
            ]
        df_temp.to_csv(f"foursquare_berlin_coordinates_{index}.csv")
        df = df.append(df_temp.drop_duplicates(subset="id"))
    return df.reset_index(drop="index")


def four_sqr_api_details(client_id, client_secret, venue_id):
    url = f"https://api.foursquare.com/v2/venues/{venue_id}"
    params = dict(client_id=client_id, client_secret=client_secret, v="20200826")
    response = requests.get(url=url, params=params, timeout=300).json()
    return response
