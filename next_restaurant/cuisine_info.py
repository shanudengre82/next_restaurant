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

cuisine_With_less_than15 = (i for i in tuple_ if i not in cuisine_num_wise)
