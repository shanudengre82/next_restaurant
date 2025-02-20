import numpy as np
from typing import Dict, List
import pandas as pd

RESTAURANT_TYPE: List[str] = [
    "Asian",
    "Middle eastern",
    "Breakfast",
    "European",
    "Japanese",
    "French",
    "Indonesian",
    "Portuguese",
    "Indian",
    "Italian",
    "Greek",
    "German",
    "Amerikanisch - Barbecue",
    "Turkish",
    "Grilled",
    "Balkan",
    "Mediterranean",
    "Vietnamese",
    "Halal",
    "Spanish",
    "Vegan",
    "Lebanese",
    "American",
    "International",
    "Vegetarian",
    "Pizza",
    "Mexican",
    "Thai",
    "Korean",
    "Steak",
    "Chinese",
    "Fastfood",
    "Brunch",
    "Hotdog",
    "African",
    "Burgers",
    "Latin american",
    "Taiwanese",
    "Fusion",
    "Bistro",
    "Kosher",
    "Brewery",
    "Snacks",
    "Chicken",
    "Soup",
    "Russian",
    "Brazilian",
    "Ice",
    "Sandwiches",
    "Dutch",
    "Organic",
    "Caucasian",
    "Fish",
    "Austrian",
    "Irish",
    "British",
    "Tibetian",
    "Hawaiian",
    "Polish",
    "Argentine",
    "Caribbean",
    "Peruvian",
    "Swiss",
    "Malaysian",
    "Singaporean",
    "Hungarian",
    "canteen",
    "food",
    "indpak",
    "mediterranean",
    "hotdogs",
    "cafes",
    "vegetarian",
    "modern_european",
    "vietnamese",
    "french",
    "german",
    "currysausage",
    "italian",
    "peruvian",
    "icecream",
    "turkish",
    "bars",
    "korean",
    "greek",
    "spanish",
    "vegan",
    "burgers",
    "russian",
    "divebars",
    "sushi",
    "pizza",
    "latin",
    "coffee",
    "argentine",
    "delicatessen",
    "tradamerican",
    "lebanese",
    "israeli",
    "himalayan",
    "swabian",
    "wine_bars",
    "hotdog",
    "international",
    "mideastern",
    "foodstands",
    "halal",
    "steak",
    "indonesian",
    "juicebars",
    "chinese",
    "panasian",
    "serbocroatian",
    "bistros",
    "thai",
    "beergarden",
    "bbq",
    "oriental",
    "mexican",
    "breakfast_brunch",
    "falafel",
    "brasseries",
    "arabian",
    "cocktailbars",
    "brazilian",
    "foodtrucks",
    "pubs",
    "easterngerman",
    "kebab",
    "african",
    "japanese",
    "gourmet",
    "restaurants",
    "bavarian",
    "gastropubs",
    "schnitzel",
    "beer_and_wine",
]


CUISINE_ORDERED: List[str] = [
    "All",
    "Italian",
    "German",
    "Asian",
    "European",
    "Middle eastern",
    "Vietnamese",
    "International",
    "Japanese",
    "Pizza",
    "Indian",
    "Chinese",
    "Turkish",
    "Greek",
    "French",
    "Burgers",
    "Thai",
    "Mediterranean",
    "Mexican",
    "American",
    "Korean",
    "Spanish",
    "Cafes",
    "Balkan",
    "Vegan",
    "Steak",
    "Brunch",
    "African",
]

CUSINE_ORDERED_DATA_FRAME: List[str] = [
    "all",
    "european",
    "asian",
    "italian",
    "german",
    "vietnamese",
    "pizza",
    "middle eastern",
    "mediterranean",
    "indian",
    "international",
    "chinese",
    "turkish",
    "fastfood",
    "snacks",
    "american",
    "mexican",
    "cafes",
    "steak",
    "vegetarian or vegan",
    "breakfast",
    "bars",
    "balkan",
    "south american",
    "african",
    "fusion",
    "russian",
    "organic",
    "seafood",
    "soup",
    "ice",
    "hawaiian",
    "caucasian",
    "caribbean",
]

CUISINE_CLEAN_DATA_FRAME_TO_REMOVE: List[str] = [
    "Snacks",
    "Bars",
    "Ice",
    "Bars",
    "Balkan",
    "South american",
    "African",
    "Fusion",
    "Russian",
    "Organic",
    "Seafood",
    "Soup",
    "Hawaiian",
    "Caucasian",
    "Caribbean",
]

CUISINE_TO_REMOVE: List[str] = [
    item.lower() for item in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]

CUSINE_ORDERED_DATA_FRAME_CAPITALISE: List[str] = [
    cuisine.capitalize() for cuisine in CUSINE_ORDERED_DATA_FRAME
]

CUISINE_MOST_FREQUENT: List[str] = CUSINE_ORDERED_DATA_FRAME_CAPITALISE[0:10]

CUSINE_LESS_FREQUENT: List[str] = [
    cuisine for cuisine in RESTAURANT_TYPE if cuisine not in CUISINE_ORDERED
]

# use this dict to convert foodType2 into broader foodType categories
foodType_CATEGORIES: Dict[str, str] = {
    "japanese": "asian",
    "indonesian": "asian",
    "vietnamese": "asian",
    "portuguese": "european",
    "french": "european",
    "greek": "mediterranean",
    "german": "european",
    "amerikanisch - barbecue": "american",
    "spanish": "mediterranean",
    "lebanese": "middle eastern",
    "pizza": "european",
    "thai": "asian",
    "korean": "asian",
    "chinese": "asian",
    "brunch": "breakfast",
    "taiwanese": "asian",
    "polish": "european",
    "hotdog": "snacks",
    "chicken": "snacks",
    "sandwiches": "snacks",
    "austrian": "european",
    "argentine": "south american",
    "peruvian": "south american",
    "swiss": "european",
    "malaysian": "asian",
    "hungaran": "balkan",
    "indpak": "indian",
    "hotdogs": "snacks",
    "currysausage": "snacks",
    "icecream": "ice",
    "sushi": "asian",
    "latin": "south american",
    "coffee": "cafes",
    "tradamerican": "american",
    "israeli": "middle eastern",
    "foodstands": "snacks",
    "mideastern": "middle eastern",
    "breakfast_brunch": "breakfast",
    "panasian": "asian",
    "oriental": "middle eastern",
    "falafel": "middle eastern",
    "foodtrucks": "snacks",
    "easterngerman": "european",
    "kebab": "fastfood",
    "bavarian": "european",
    "schnitzel": "european",
    "fish": "seafood",
    "persian": "middle eastern",
    "ramen": "asian",
    "italian": "european",
    "grilled": "steak",
    "divebars": "bars",
    "beachbars": "bars",
    "beer_and_wine": "bars",
    "hungarian": "european",
    "tibetian": "asian",
    "modern_european": "european",
    "brasseries": "european",
    "cocktailbars": "bars",
    "pubs": "bars",
    "food": "snacks",
    "gourmet": "european",
    "gastropub": "european",
    "beergarden": "bars",
    "arabian": "middle eastern",
    "moroccan": "middle eastern",
    "delicatessen": "snacks",
    "bistro": "european",
    "vegan": "vegetarian or vegan",
    "vegetarian": "vegetarian or vegan",
    "brewery": "bars",
    "burgers": "fastfood",
    "swabian": "european",
    "irish": "european",
    "british": "european",
    "juicebar": "snacks",
    "halal": "middle eastern",
    "kosher": "middle eastern",
    "wine_bars": "bars",
    "juicebars": "snacks",
    "bistros": "european",
    "canteen": "european",
    "gastropubs": "european",
    "restaurants": "european",
    "brazilian": "south american",
    "bbq": "fastfood",
    "latin american": "south american",
}


CUISINE_OPTIONS: List[str] = [
    cuisine
    for cuisine in CUSINE_ORDERED_DATA_FRAME_CAPITALISE
    if cuisine not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE
]


def categorize_foodTypes(
    df: pd.DataFrame, restaurant_type_mapping: Dict[str, str]
) -> pd.DataFrame:
    # Backup original 'foodType' column
    df["foodType_3"] = df["foodType"]

    # Replace foodType values based on mapping
    df["foodType"] = df["foodType"].replace(restaurant_type_mapping)

    # Update 'foodType2' where it is either NaN or identical to the new 'foodType'
    df["foodType2"] = df["foodType2"].fillna(df["foodType_3"])
    df.loc[df["foodType"] == df["foodType2"], "foodType2"] = df["foodType_3"]

    # Drop unnecessary columns if they exist
    df.drop(
        columns=[col for col in ["foodType_3", "Unnamed: 0"] if col in df],
        inplace=True,
    )

    return df


def change_main_foodTypes(df: pd.DataFrame) -> pd.DataFrame:
    # Define mapping conditions: (current foodType, new foodType2) -> updated foodType
    mapping = {
        ("european", "german"): "german",
        ("european", "italian"): "italian",
        ("asian", "vietnamese"): "vietnamese",
        ("asian", "japanese"): "japanese",
        ("asian", "chinese"): "chinese",
        ("asian", "indian"): "indian",
        ("middle eastern", "turkish"): "turkish",
    }

    # Use vectorized operations with .replace and .map
    mask = df[["foodType", "foodType2"]].apply(tuple, axis=1).map(mapping)
    df["foodType"] = mask.fillna(df["foodType"])

    # Ensure "pizza" always takes precedence
    df["foodType"] = np.where(df["foodType2"] == "pizza", "pizza", df["foodType"])

    return df
