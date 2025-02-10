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

CUSINE_ORDERED_DATA_FRAME = List[str] = [
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

# use this dict to convert food_type_2 into broader food_type categories
FOOD_TYPE_CATEGORIES: Dict[str, str] = {
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


def categorize_food_types(df_name: pd.DataFrame) -> pd.DataFrame:
    # Temporary saves the first food_type categories into a new column
    df_name["food_type_3"] = df_name["food_type"]

    # Grouping the foodtypes by borader categories based on the dictionary above
    df_name = df_name.replace({"food_type": RESTAURANT_TYPE})

    # Replace the nans in the food_type_2 columns by food_type_3
    # Replace values in food_type_2 columns by food_type_3 if food_type_2 is the same as food_type

    df_name.loc[df_name["food_type"] == df_name["food_type_2"], "food_type_2"] = (
        df_name["food_type_3"]
    )
    df_name["food_type_2"] = np.where(
        df_name["food_type_2"].isna(), df_name["food_type_3"], df_name["food_type_2"]
    )

    # Drop the food_type_3 columns as it is not needed anymore, also drop useless columns

    df_name.drop(columns="food_type_3", inplace=True)
    df_name.drop(columns="Unnamed: 0", inplace=True)

    return df_name


# change main food_types_2 to food_type (german, pizza, italian, vietnamese, japaneses, chinese, turkish, indian)


def change_main_food_types(df):
    df["food_type"] = np.where(
        (df["food_type_2"] == "german") & (df["food_type"] == "european"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "italian") & (df["food_type"] == "european"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        df["food_type_2"] == "pizza", df["food_type_2"], df["food_type"]
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "vietnamese") & (df["food_type"] == "asian"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "japanese") & (df["food_type"] == "asian"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "chinese") & (df["food_type"] == "asian"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "indian") & (df["food_type"] == "asian"),
        df["food_type_2"],
        df["food_type"],
    )

    df["food_type"] = np.where(
        (df["food_type_2"] == "turkish") & (df["food_type"] == "middle eastern"),
        df["food_type_2"],
        df["food_type"],
    )

    return df
