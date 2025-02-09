import requests
import pandas as pd
from urllib.parse import urlencode, urlparse

"""takes search term, lat, lng, and radius
and return a url to call yalp business search API"""


def generate_yelp_api_url(search_term, latitude, longitude, radius):
    yelp_sample = "https://api.yelp.com/v3/businesses/search"
    parsed_url = urlparse(yelp_sample)
    end_point = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    params = {
        "term": search_term,
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "limit": 50,
    }
    url_params = urlencode(params)
    url = f"{end_point}?{url_params}"
    return url


"""calls the yelp business search api starting from the city center and moving outwards"""


def call_yelp_api(search_term, yelp_key, start: int, end: int):
    coordinates_list = (
        pd.read_csv("../raw_data/Berlin_coordinates_with_distances_index.csv")
        .sort_values(by="distance")
        .reset_index(drop=True)
    )
    results = []
    for cordinate in coordinates_list.index[start:end]:
        yelp_url = generate_yelp_api_url(
            search_term,
            coordinates_list["lat"][cordinate],
            coordinates_list["lng"][cordinate],
            80,
        )
        headers = {"Authorization": f"Bearer {yelp_key}"}
        yelp_response = requests.get(yelp_url, headers=headers, timeout=300).json()
        index = int(coordinates_list.iloc[cordinate]["index"])
        pd.DataFrame(yelp_response).to_csv(f"yelp_berlin_coordinates_{index}.csv")
        results.extend(yelp_response["businesses"])
    return results
