"""Explore Berlin page: results table, map, and market analysis."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from next_restaurant.functions_for_df import (
    update_df_based_on_selected_cusine_and_district,
    get_map_instance,
    generating_circles,
    show_map,
)
from next_restaurant.nlp_search import validate_query, search
from next_restaurant.cuisine_stats_display import (
    all_district_all_cuisines,
    all_district_selected_cuisine,
    selected_district_all_cuisine,
    selected_district_selected_cuisine,
    display_map_legend,
)
from next_restaurant.stats import (
    get_number_of_good_restaurants,
    get_percent_of_good_restaurants,
    update_stats_per_cuisine,
    update_stats_per_hood,
    update_stats_per_cuisine_and_hood,
    update_stats_per_hood_and_cuisine,
)
from next_restaurant.app_state import load_data, load_search_stack
from next_restaurant.parameters import BERLIN_CENTER, HEIGHT, INITIAL_ZOOM
from next_restaurant.cuisine_info import CUISINE_OPTIONS, CUISINE_CLEAN_DATA_FRAME_TO_REMOVE


def render():
    """Render Explore Berlin page."""
    df = load_data()
    vocab, search_index = load_search_stack(df)

    # Get sidebar state
    nl_query = st.session_state.get("nl_query", "")
    applied_query = st.session_state.get("applied_query", "")
    cuisine = st.session_state.get("cuisine", "All")
    district = st.session_state.get("district", "All")
    rating_cutoff = st.session_state.get("rating", 4.5)
    popularity_cutoff = st.session_state.get("reviews", 40)
    map_filter = st.session_state.get("map_filter", "All restaurants")

    # Show search results if query is active
    if nl_query and applied_query:
        validation = validate_query(nl_query, vocab)
        if validation.ok:
            results_df = search(
                search_index, df, validation.parsed,
                min_rating=rating_cutoff, min_reviews=popularity_cutoff
            )
            if len(results_df) > 0:
                st.subheader("Search results")
                st.dataframe(
                    results_df[["namesClean", "foodType", "district", "rating", "userRatingsTotal"]].rename(
                        columns={
                            "namesClean": "Restaurant",
                            "foodType": "Cuisine",
                            "district": "District",
                            "rating": "Rating",
                            "userRatingsTotal": "Reviews",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

    # Explore Berlin map section
    st.header("Explore Berlin")

    df_filtered = update_df_based_on_selected_cusine_and_district(df, cuisine, district)
    df_copy_for_stats = df_filtered.copy()

    # Apply map filter
    if map_filter == "Only good restaurants":
        df_map = df_filtered[
            (df_filtered["rating"] >= rating_cutoff)
            & (df_filtered["userRatingsTotal"] >= popularity_cutoff)
        ]
    elif map_filter == "Only low rated restaurants":
        df_map = df_filtered[df_filtered["rating"] < 4.0]
    else:
        df_map = df_filtered

    # Build map
    if district == "All":
        m = get_map_instance(zoom=INITIAL_ZOOM, initial_location=BERLIN_CENTER, height=HEIGHT)
    else:
        try:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="next_restaurant")
            location = geolocator.geocode(f"{district}, Berlin")
            if location:
                m = get_map_instance(
                    zoom=14, initial_location=[location.latitude, location.longitude], height=HEIGHT
                )
            else:
                m = get_map_instance(zoom=INITIAL_ZOOM, initial_location=BERLIN_CENTER, height=HEIGHT)
        except Exception:
            m = get_map_instance(zoom=INITIAL_ZOOM, initial_location=BERLIN_CENTER, height=HEIGHT)

    # Add restaurant markers with color based on rating
    df_map_copy = df_map.copy()
    df_map_copy["ratings_color"] = df_map_copy["rating"].apply(
        lambda x: "orange" if x < rating_cutoff else "blue"
    )
    m = generating_circles(m, df_map_copy, color="ratings_color")
    show_map(m, key="explore_map", height=HEIGHT, legend=display_map_legend)

    # KPI metrics
    kpi_cols = st.columns(4)
    total_restaurants = len(df_filtered)
    good_restaurants = len(
        df_filtered[
            (df_filtered["rating"] >= rating_cutoff)
            & (df_filtered["userRatingsTotal"] >= popularity_cutoff)
        ]
    )
    percent_good = (
        100 * good_restaurants / total_restaurants if total_restaurants > 0 else 0
    )

    cuisine_list = df["foodType"].value_counts().index.tolist()
    cuisine_list = [c for c in cuisine_list if c not in CUISINE_CLEAN_DATA_FRAME_TO_REMOVE]

    kpi_cols[0].metric("Restaurants", f"{total_restaurants:,}")
    kpi_cols[1].metric("Rated as good", f"{percent_good:.0f}%")
    kpi_cols[2].metric("Avg rating", f"{df_filtered['rating'].mean():.2f}")
    kpi_cols[3].metric("Most common", cuisine_list[0].capitalize() if cuisine_list else "—")

    # Key points section
    st.subheader("Key points")
    st.markdown("Consider this information when choosing a location for your restaurant:")

    # Calculate statistics
    stats_cuisine = update_stats_per_cuisine(
        df_copy_for_stats, cuisine, rating_cutoff, popularity_cutoff
    )
    stats_hoods = update_stats_per_hood(df_copy_for_stats, rating_cutoff, popularity_cutoff)

    if cuisine == "All" and district == "All":
        all_district_all_cuisines(
            total_number_of_restaurants=total_restaurants,
            number_of_good_restaurants=good_restaurants,
            five_most_common_cuisines=cuisine_list[:5],
            five_most_common_percent=[100 * len(df[df["foodType"] == c]) / len(df) for c in cuisine_list[:5]],
        )
    elif cuisine != "All" and district == "All":
        stats_hoods_cuisine = update_stats_per_hood_and_cuisine(
            df_copy_for_stats, cuisine, rating_cutoff, popularity_cutoff
        )
        all_district_selected_cuisine(
            stats_hoods_cuisine=stats_hoods_cuisine,
            stats_cuisine_hoods=stats_hoods_cuisine,
            options_cuisine=cuisine,
            number_cuisine=len(df[df["foodType"] == cuisine]),
            percent_good_cuisine=100 * good_restaurants / total_restaurants if total_restaurants > 0 else 0,
            percent_of_all=100 * len(df[df["foodType"] == cuisine]) / len(df),
            best_rated_3_cuisines=cuisine_list[:3],
            best_rated_3_perc=[100 * len(df[df["foodType"] == c]) / len(df) for c in cuisine_list[:3]],
        )
    elif cuisine == "All" and district != "All":
        selected_district_all_cuisine(
            stats_hoods=stats_hoods,
            options_district=district,
            main_cuisine_per_hood=stats_hoods.iloc[0]["cuisine"] if len(stats_hoods) > 0 else "—",
            percent_main_cuisine=100,
            total_num_of_restaurants=total_restaurants,
            number_of_good_restaurants=good_restaurants,
            most_restaurants=stats_hoods.iloc[0]["district"] if len(stats_hoods) > 0 else district,
            most_restaurants_perc=100,
            best_district=district,
            best_district_per=percent_good,
            five_most_common_cuisines=cuisine_list[:5],
            five_most_common_percent=[100 * len(df[df["foodType"] == c]) / len(df) for c in cuisine_list[:5]],
        )
    else:
        stats_cuisine_hoods = update_stats_per_cuisine_and_hood(
            df_copy_for_stats, cuisine, district, rating_cutoff, popularity_cutoff
        )
        selected_district_selected_cuisine(
            stats_hoods_cuisine=stats_cuisine_hoods,
            stats_cuisine_hoods=stats_cuisine_hoods,
            options_district=district,
            options_cuisine=cuisine,
            berlin_cuisine=total_restaurants,
            berlin_good_cuisine=good_restaurants,
        )
