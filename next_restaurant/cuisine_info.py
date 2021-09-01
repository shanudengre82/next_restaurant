import numpy as np

tuple_ = ('Asian', 'Middle eastern', 'Breakfast', 'European', 'Japanese', 'French', 'Indonesian',
'Portuguese', 'Indian', 'Italian', 'Greek', 'German', 'Amerikanisch - Barbecue', 'Turkish',
 'Grilled', 'Balkan', 'Mediterranean', 'Vietnamese', 'Halal', 'Spanish', 'Vegan', 'Lebanese',
 'American', 'International', 'Vegetarian', 'Pizza', 'Mexican', 'Thai', 'Korean', 'Steak',
 'Chinese', 'Fastfood', 'Brunch', 'Hotdog', 'African', 'Burgers', 'Latin american', 'Taiwanese',
 'Fusion', 'Bistro', 'Kosher', 'Brewery', 'Snacks', 'Chicken', 'Soup', 'Russian', 'Brazilian',
 'Ice', 'Sandwiches', 'Dutch', 'Organic', 'Caucasian', 'Fish', 'Austrian', 'Irish', 'British',
 'Tibetian', 'Hawaiian', 'Polish', 'Argentine', 'Caribbean', 'Peruvian', 'Swiss', 'Malaysian',
 'Singaporean', 'Hungarian', 'canteen', 'food', 'indpak', 'mediterranean', 'hotdogs', 'cafes',
 'vegetarian', 'modern_european', 'vietnamese', 'french', 'german', 'currysausage', 'italian',
 'peruvian', 'icecream', 'turkish', 'bars', 'korean', 'greek', 'spanish', 'vegan', 'burgers',
 'russian', 'divebars', 'sushi', 'pizza', 'latin', 'coffee', 'argentine', 'delicatessen',
  'tradamerican', 'lebanese', 'israeli', 'himalayan', 'swabian', 'wine_bars', 'hotdog',
  'international', 'mideastern', 'foodstands', 'halal', 'steak', 'indonesian', 'juicebars',
   'chinese', 'panasian', 'serbocroatian', 'bistros', 'thai', 'beergarden', 'bbq', 'oriental',
   'mexican', 'breakfast_brunch', 'falafel', 'brasseries', 'arabian', 'cocktailbars', 'brazilian',
   'foodtrucks', 'pubs', 'easterngerman', 'kebab', 'african',
'japanese', 'gourmet', 'restaurants', 'bavarian', 'gastropubs', 'schnitzel', 'beer_and_wine')


cuisine_num_wise = ("All", 'Italian', 'German', 'Asian', 'European', 'Middle eastern', 'Vietnamese',
'International', 'Japanese', 'Pizza', 'Indian', 'Chinese', 'Turkish', 'Greek', 'French', 'Burgers',
'Thai', 'Mediterranean', 'Mexican', 'American', 'Korean', 'Spanish', 'Cafes', 'Balkan', 'Vegan',
'Steak', 'Brunch', 'African')

# cuisine_most_frequent = ['Italian', 'German', 'Asian', 'European', 'Middle eastern', 'Vietnamese',
# 'International', 'Japanese', 'Pizza', 'Indian', 'Chinese']

cuisine_num_wise_clean_data_frame = ["all", 'asian', 'middle eastern', 'breakfast', 'european', 'indian',
 'mediterranean', 'american', 'turkish', 'steak', 'balkan', 'vegetarian or vegan',
 'international', 'mexican', 'fastfood', 'snacks', 'african', 'south american',
 'fusion', 'bars', 'soup', 'russian', 'ice', 'organic', 'caucasian', 'seafood', 'hawaiian', 'caribbean',
 'cafes']

cuisine_clean_data_frame_to_remove = ['Snacks', 'Bars', 'Ice']

cuisine_num_wise_clean_data_frame_capitalise = [i.capitalize() for i in cuisine_num_wise_clean_data_frame]

cuisine_most_frequent = cuisine_num_wise_clean_data_frame_capitalise[0: 10]

cuisine_With_less_than15 = (i for i in tuple_ if i not in cuisine_num_wise)


# use this dict to convert food_type_2 into broader food_type categories
food_types_categories = {
    'japanese': 'asian',
    'indonesian': 'asian',
    'vietnamese': 'asian',
    'portuguese': 'european',
    'french': 'european',
    'greek': 'mediterranean',
    'german': 'european',
    'amerikanisch - barbecue': 'american',
    'spanish': 'mediterranean',
    'lebanese': 'middle eastern',
    'pizza': 'european',
    'thai': 'asian',
    'korean': 'asian',
    'chinese': 'asian',
    'brunch': 'breakfast',
    'taiwanese': 'asian',
    'polish': 'european',
    'hotdog': 'snacks',
    'chicken': 'snacks',
    'sandwiches': 'snacks',
    'austrian': 'european',
    'argentine': 'south american',
    'peruvian': 'south american',
    'swiss': 'european',
    'malaysian': 'asian',
    'hungaran': 'balkan',
    'indpak': 'indian',
    'hotdogs': 'snacks',
    'currysausage': 'snacks',
    'icecream': 'ice',
    'sushi': 'asian',
    'latin': 'south american',
    'coffee': 'cafes',
    'tradamerican': 'american',
    'israeli': 'middle eastern',
    'foodstands': 'snacks',
    'mideastern': 'middle eastern',
    'breakfast_brunch': 'breakfast',
    'panasian': 'asian',
    'oriental': 'middle eastern',
    'falafel': 'middle eastern',
    'foodtrucks': 'snacks',
    'easterngerman': 'european',
    'kebab': 'fastfood',
    'bavarian': 'european',
    'schnitzel': 'european',
    'fish': 'seafood',
    'persian': 'middle eastern',
    'ramen': 'asian',
    'italian': 'european',
    'grilled': 'steak',
    'divebars': 'bars',
    'beachbars': 'bars',
    'beer_and_wine': 'bars',
    'hungarian': 'european',
    'tibetian': 'asian',
    'japanese': 'asian',
    'modern_european': 'european',
    'brasseries': 'european',
    'cocktailbars': 'bars',
    'pubs': 'bars',
    'beachbars': 'bars',
    'food': 'snacks',
    'gourmet': 'european',
    'gastropub': 'european',
    'beergarden': 'bars',
    'arabian': 'middle eastern',
    'moroccan': 'middle eastern',
    'delicatessen': 'snacks',
    'bistro': 'european',
    'vegan': 'vegetarian or vegan',
    'vegetarian': 'vegetarian or vegan',
    'brewery': 'bars',
    'burgers': 'fastfood',
    'swabian': 'european',
    'irish': 'european',
    'british': 'european',
    'juicebar': 'snacks',
    'halal': 'middle eastern',
    'kosher': 'middle eastern',
    'wine_bars': 'bars',
    'juicebars': 'snacks',
    'bistros': 'european',
    'canteen': 'european',
    'gastropubs': 'european',
    'restaurants': 'european',
    'brazilian': 'south american',
    'bbq': 'fastfood',
    'latin american': 'south american'
}

def categorize_food_types(df_name):

    # Temporary saves the first food_type categories into a new column

    df_name['food_type_3'] = df_name['food_type']

    # Grouping the foodtypes by borader categories based on the dictionary above

    df_name = df_name.replace({'food_type': food_types_categories})

    # Replace the nans in the food_type_2 columns by food_type_3
    # Replace values un food_type_2 columns by food_type_3 if food_type_2 is the same as food_type

    df_name.loc[df_name['food_type'] == df_name['food_type_2'], 'food_type_2'] = df_name['food_type_3']
    df_name['food_type_2'] = np.where(df_name['food_type_2'].isna(), df_name['food_type_3'],
                             df_name['food_type_2'])

    # Drop the food_type_3 columns as it is not needed anymore, also drop useless columns

    df_name.drop(columns='food_type_3', inplace=True)
    df_name.drop(columns='Unnamed: 0', inplace=True)

    return df_name

district_list = ["All", 'Mitte', 'Charlottenburg', 'Kreuzberg', 'Prenzlauer Berg', 'Schöneberg', 'Neukölln',
 'Wilmersdorf', 'Friedrichshain', 'Wedding', 'Moabit', 'Tiergarten', 'Friedenau', 'Charlottenburg-Nord', 'Steglitz', 'Britz',
 'Pankow', 'Lichtenberg', 'Friedrichsfelde', 'Reinickendorf', 'Französisch Buchholz', 'Tegel',
 'Weißensee', 'Wittenau', 'Niederschönhausen', 'Tempelhof', 'Oberschöneweide', 'Lichterfelde',
 'Alt-Hohenschönhausen', 'Mariendorf', 'Alt-Treptow', 'Plänterwald', 'Karlshorst', 'Grunewald',
 'Baumschulenweg', 'Stadtrandsiedlung Malchow', 'Niederschöneweide', 'Spandau', 'Karow', 'Gesundbrunnen', 'Marzahn', 'Buckow',
 'Malchow', 'Neu-Hohenschönhausen', 'Marienfelde', 'Wartenberg', 'Blankenburg', 'Heinersdorf', 'Lichtenrade', 'Westend']
