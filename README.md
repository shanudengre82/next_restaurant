# next_restaurant

## Introduction
This project is focused upon the location Berlin. We have huge numbers of restaurant in Berlin and with this app, we try to use data of existing restaurants to predict best locations to open next restaurant.

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

## User Instructions

1. Please note that for the working of the app, raw_data/clean_dataframe.csv file is needed with following format

| priceLevel | rating | userRatingsTotal | lat | lng | fullAddress | district | foodType | foodType2 |
|-------------|--------|--------------------|-----|-----|--------------|----------|-----------|-------------|
| $$ | 4.3 | 980 | 52.1 | 13.1 | Address 1, Mitte, Berlin | Mitte | Indian | North Indian |
| $ | 4.2 | 1100 | 52.2 | 13.15 | Address 2, Mitte, Berlin | Mitte | Chinese | Chinese |

2. Once the streamlit web app is ruinning, we will see the following

![My Image](/images/image_1.png)

On the left, different selections related to the neighbourhood and cuisines are provided. The data will be filtered based on user defined preferences like the neighbourhood, cuisine and rating threshold.
