import re
from typing import Any, List

import pandas as pd

berlin_areas = pd.read_csv("raw_data/berlin_areas.csv")

# extracts the postcodes from the full address using regex


def extract_postcode(text: str) -> Any:
    return re.findall(r"(?:^|\D)(\d{5})(?!\d)", text)[0]


# Returns district based on postcodes


def get_district(zip_code: str) -> Any:
    zipco = berlin_areas.loc[berlin_areas["PLZ"] == int(zip_code), "Stadtteil"]

    if len(zipco) == 1:
        return berlin_areas.loc[
            berlin_areas["PLZ"] == int(zip_code), "Stadtteil"
        ].values[0]
    elif len(zipco) > 1:
        zip_co_lst = list(zipco)
        return zip_co_lst[0]
    else:
        return "Not Found"


# get zipcode and district for all restaurants


def district_to_df(df_name: pd.DataFrame) -> pd.DataFrame:
    df_name["zip_code"] = df_name.fullAddress.apply(extract_postcode)
    df_name["district"] = df_name.zip_code.apply(get_district)
    return df_name


BERLIN_DISTRICTS: List[str] = [
    "All",
    "Charlottenburg",
    "Kreuzberg",
    "Friedrichshain",
    "Mitte",
    "Neukölln",
    "Prenzlauer Berg",
    "Schöneberg",
    "Wilmersdorf",
    "Wartenberg",
    "Lichtenberg",
    "Friedenau",
    "Wedding",
    "Charlottenburg-Nord",
    "Moabit",
    "Steglitz",
    "Karlshorst",
    "Pankow",
    "Britz",
    "Malchow",
    "Tiergarten",
    "Wittenau",
    "Niederschöneweide",
    "Alt-Hohenschönhausen",
    "Tegel",
    "Friedrichsfelde",
    "Niederschönhausen",
    "Alt-Treptow",
    "Plänterwald",
    "Französisch Buchholz",
    "Reinickendorf",
    "Tempelhof",
    "Stadtrandsiedlung Malchow",
    "Marienfelde",
    "Marzahn",
    "Baumschulenweg",
    "Westend",
    "Gesundbrunnen",
    "Weißensee",
    "Grunewald",
    "Karow",
    "Neu-Hohenschönhausen",
    "Oberschöneweide",
    "Mariendorf",
    "Lichterfelde",
    "Spandau",
    "Blankenburg",
    "Buckow",
    "Lichtenrade",
    "Heinersdorf",
]
