# next_restaurant

## Introduction
This project is focused upon the location Berlin. We have huge numbers of restaurant in Berlin and with this app, we try to use data of existing restaurants to predict best locations to open next restaurant.

To use streamlit app, please follow the [link](https://nextrestaurant.streamlit.app/)

## Installation steps

1. Clone the project and install it:

```bash
git clone git@github.com:shanudengre82/next_restaurant.git
cd next_restaurant
```
2. Python version requirement, python = ">=3.10,<3.13"

3. Install depedencies, please note that it requires
```bash
poetry install
```

4. Once all the dependencies are installed, we can run the streamlit app using

```bash
streamlit run app.py
```

## Two-Page Architecture

The app is now split into two focused pages accessible from the main navigation:

### Page 1: Explore Berlin
Explore the market by cuisine and district:
- **Search results table** (appears when a query is active) showing matching restaurants ranked by semantic similarity and rating
- **Interactive map** with restaurant locations color-coded by rating
- **Market insights** showing total restaurants, average rating, and review counts
- **Key points** highlighting the best-performing districts and cuisines

### Page 2: Find best locations
Analyze a specific address for site suitability:
- **Address search**: Enter any Berlin address or district name
- **Nearby radius**: Adjust the search area (1-50 km)
- **Competitors analysis**: See existing restaurants near your chosen location
- **Site recommendations**: Visual suggestions showing the best-positioned gaps for a new restaurant

## Sidebar: Natural Language Search

The left sidebar contains your primary interaction tools:

1. **Search box**: Describe what you're looking for in natural language
   - Examples: *"Italian restaurants"*, *"sushi in Mitte"*, *"vegan with 100+ reviews"*, *"Turkish above 4.5"*
   - **Supported constraints**:
     - Cuisines: Any cuisine from the dataset (Italian, Asian, Indian, etc.)
     - Districts: All Berlin districts (Mitte, Kreuzberg, Friedrichshain, etc.)
     - Ratings: "above 4.5", "top rated", "highly rated", etc.
     - Reviews: "100+ reviews", "at least 50 reviews", etc.
   - **Guardrails**: Your query must include a cuisine or a district. Invalid queries show helpful feedback.

2. **Example buttons**: Pre-built queries you can click to instantly search
   - Italian in Kreuzberg
   - Top rated sushi in Mitte
   - Pizza with 100+ reviews
   - Vegan in Prenzlauer Berg
   - Turkish above 4.5

3. **Filter expanders**:
   - **1. Where & what**: Manually select cuisine and district
   - **2. What is a good restaurant?**: Set minimum rating and review thresholds
   - **3. Map display**: Choose to show all, good, or low-rated restaurants

4. **About**: Information on how the app works

2. Please note that for the working of the app, raw_data/clean_dataframe.csv file is needed with following format

| priceLevel | rating | userRatingsTotal | lat | lng | fullAddress | district | foodType | foodType2 |
|-------------|--------|--------------------|-----|-----|--------------|----------|-----------|-------------|
| $$ | 4.3 | 980 | 52.1 | 13.1 | Address 1, Mitte, Berlin | Mitte | Indian | North Indian |
| $ | 4.2 | 1100 | 52.2 | 13.15 | Address 2, Mitte, Berlin | Mitte | Chinese | Chinese |

3. Once the streamlit web app is ruinning, we will see the following

![My Image](/images/image_1.png)

On the left, different selections related to the neighbourhood and cuisines are provided. The data will be filtered based on user defined preferences like the neighbourhood, cuisine and rating threshold.

4. In the bottom, another plot is provided which displays best areas to open a resturant based on user selection preferences. For reference, please see image below

![My Image](/images/image_3.png)

## Deploying on Render (free tier)

1. Create a Web Service from this repo (or use the `render.yaml` Blueprint), plan **Free**.
2. Under *Environment → Secret Files*, add `secrets.toml` with the contents of your local `.streamlit/secrets.toml` (it holds `[my_secrets] raw_data`).
3. Deploy. The free tier sleeps after 15 minutes idle, so the first load can take 30-60 seconds.
