# In this script we define the parameters for the visualization of the map for Berlin


from typing import Dict, Tuple

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
