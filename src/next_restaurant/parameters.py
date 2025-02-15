# In this script we define the parameters for the visualization of the map for Berlin


from typing import List, Dict, Tuple

#  Starting point
# Berlin_center = [52.5200066, 13.404954]

# Changed center to make it symmeteric
BERLIN_CENTER: Tuple[float, float] = (52.5, 13.49)

# Defining intial parameters for the map visuals
WIDTH: int = 1000
HEIGHT: int = 600
INITIAL_ZOOM: int = 11
INITIAL_RADIUS: int = 50

# defining gradient for heatmaps
GRADIENT_FOR_HEATMAPS: Dict[float, str] = {
    0.2: "purple",
    0.4: "purple",
    0.6: "purple",
    0.8: "orange",
    1: "orange",
}


BERLIN_DISTRICT_LIST: List[str] = [
    "All",
    "Mitte",
    "Charlottenburg",
    "Kreuzberg",
    "Prenzlauer Berg",
    "Schöneberg",
    "Neukölln",
    "Wilmersdorf",
    "Friedrichshain",
    "Wedding",
    "Moabit",
    "Tiergarten",
    "Friedenau",
    "Charlottenburg-Nord",
    "Steglitz",
    "Britz",
    "Pankow",
    "Lichtenberg",
    "Friedrichsfelde",
    "Reinickendorf",
    "Französisch Buchholz",
    "Tegel",
    "Weißensee",
    "Wittenau",
    "Niederschönhausen",
    "Tempelhof",
    "Oberschöneweide",
    "Lichterfelde",
    "Alt-Hohenschönhausen",
    "Mariendorf",
    "Alt-Treptow",
    "Plänterwald",
    "Karlshorst",
    "Grunewald",
    "Baumschulenweg",
    "Stadtrandsiedlung Malchow",
    "Niederschöneweide",
    "Spandau",
    "Karow",
    "Gesundbrunnen",
    "Marzahn",
    "Buckow",
    "Malchow",
    "Neu-Hohenschönhausen",
    "Marienfelde",
    "Wartenberg",
    "Blankenburg",
    "Heinersdorf",
    "Lichtenrade",
    "Westend",
]
