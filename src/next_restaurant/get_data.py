import pandas as pd
import requests  # type: ignore
import streamlit as st

from next_restaurant.custom_logger import APP_LOGGER


def get_raw_df() -> pd.DataFrame:
    try:
        response = requests.get(
            st.secrets["URL_TO_DATA"],
            auth=(st.secrets["USERNAME"], st.secrets["PASSWORD"]),
        )
    except KeyError:
        APP_LOGGER.warning(
            "All credentials not found, please check your saved streamlit credentials"
        )

    if response.status_code == 402:
        APP_LOGGER.warning("Please verify values of all the credentials")
    if response.status_code == 200:
        APP_LOGGER.info("Logging successfull, accessing data and making ")
        data = response.json()["sheet1"]
        df = pd.DataFrame(data)
        APP_LOGGER.info("Fetching file from web complete")
    else:
        APP_LOGGER.info(
            f"Error fetchhing data from web: {response.status_code}, {response.text}"
        )
        APP_LOGGER.info("Unable to load file from web, looking file locally")

    # reading file locally
    try:
        df = pd.read_csv("../../raw_data/clean_dataframe.csv")
    except FileNotFoundError:
        APP_LOGGER.warning("Unable to load file from web, looking file locally")
        raise FileNotFoundError(
            "Unable to find file ../../raw_data//clean_dataframe.csv"
        )
    return df
