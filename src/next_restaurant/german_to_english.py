import streamlit as st

"""
In this module we make a function all the functions
needed to convert German names from here to English
"""
here_to_eng = {
    "Pizza": "Pizza",
    "International": "International",
    "Sandwiches": "Sandwiches",
    "Burger": "Burgers",
    "Spanisch": "Spanish",
    "Hotdogs": "Hotdog",
    "Vegan": "Vegan",
    "Halal": "Halal",
    "Fondue": "Fondue",
    "Mediterran": "Mediterranean",
    "Crêperie": "Creperies",
    "Polnisch": "Polish",
    "Pakistanisch": "Pakistani",
    "Vietnamesisch": "Vietnamese",
    "Chinesisch": "Chinese",
    "Argentinisch": "Argentine",
    "Türkisch": "Turkish",
    "Steakhaus": "Steak",
    "Japanisch": "Japanese",
    "Vegetarisch": "Vegetarian",
    "Indonesisch": "Indonesian",
    "Brasilianisch": "Brazilian",
    "Koreanisch": "Korean",
    "Peruanisch": "Peruvian",
    "Fusion": "Fusion",
    "Skandinavisch": "Scandinavian",
    "Deutsch": "German",
    "Französisch": "French",
    "Asiatisch": "Asian",
    "Singapurisch": "Singaporean",
    "Italienisch": "Italian",
    "Indisch": "Indian",
    "Thailändisch": "Thai",
    "Suppen": "Soup",
    "Europäisch": "European",
    "Libanesisch": "Lebanese",
    "Brunch": "Brunch",
    "Amerikanisch": "American",
    "Irisch": "Irish",
    "Eis": "Ice",
    "Mexikanisch": "Mexican",
    "Spanisch - Tapas": "Spanish",
    "Fastfood": "Fastfood",
    "Balkanküche": "Balkan",
    "Bistro-Küche": "Bistro",
    "Südostasiatisch": "Asian",
    "Afrikanisch": "African",
    "Osteuropäisch": "European",
    "Russisch": "Russian",
    "Äthiopisch": "European",
    "Südamerikanisch": "Latin american",
    "Lateinamerikanisch": "Latin american",
    "Britisch": "British",
    "Portugiesisch": "Portuguese",
    "Australisch": "Austrian",
    "Gebäck": "Pastry",
    "Marokkanisch": "Moroccan",
    "Jüdisch/koscher": "Kosher",
    "Ungarisch": "Hungarian",
    "Tibetisch": "Tibetian",
    "Chilenisch": "Chilean",
    "Malaysisch": "Malaysian",
    "Belgisch": "Belgian",
    "Kubanisch": "Cuban",
    "Nahöstlich": "Middle eastern",
    "Karibisch": "Caribbean",
    "Brauhaus": "Brewery",
    "Amerikanisch - barbecue": "American",
    "Japanisch - Sushi": "Japanese",
    "Naturkost/Vollwert": "Organic",
    "Hähnchen": "Chicken",
    "Grillgerichte": "Grilled",
    "Griechisch": "Greek",
    "Snacks und Getränke": "Snacks",
    "Kaukasisch": "Caucasian",
    "Fisch und Meeresfrüchte": "Fish",
    "Amerikanisch - Soul Food": "American",
    "Kontinentaleuropäisch": "European",
    "Frühstück": "Breakfast",
    "Hawaiianisch/polynesisch": "Hawaiian",
    "Österreichisch": "Austrian",
    "Indisch - nordindisch": "Indian",
    "Chinesisch - taiwanisch": "Taiwanese",
    "Schweizer Küche": "Swiss",
    "Amerikanisch - südwestamerikanische Küche": "American",
    "Niederländisch": "Dutch",
    "Amerikanisch - Cajun": "American",
}


@st.cache_data
def german_to_english(x):
    if x in here_to_eng:
        return here_to_eng[x].capitalize()
    else:
        return x.capitalize()


@st.cache_data
def food_type_conversion(df_name):
    df_name.replace({"food_type_2": food_type_conversion}, inplace=True)
    df_name.replace({"food_type": food_type_conversion}, inplace=True)
    df_name["food_type"] = df_name["food_type"].str.lower()
    df_name["food_type_2"] = df_name["food_type_2"].str.lower()
    return df_name
