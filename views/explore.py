"""Explore Berlin page: results table, map, and market analysis."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from next_restaurant.functions_for_df import (
    update_df_based_on_selected_cusine_and_district,
    get_map_instance, generating_circles, show_map
)
from next_restaurant.nlp_search import validate_query, search
from next_restaurant.stats import (
    restaurant_count_by_district, avg_rating_by_cuisine, good_restaurants_count
)
from next_restaurant.app_state import load_data, load_search_stack


def render():
    """Render Explore Berlin page."""
    # Load data
    df = load_data()
    vocab, search_index = load_search_stack(df)

    # Get session state
    nl_query = st.session_state.get("nl_query", "")
    applied_query = st.session_state.get("applied_query", "")
    cuisine = st.session_state.get("cuisine", "All")
    district = st.session_state.get("district", "All")
    rating_cutoff = st.session_state.get("rating", 4.5)
    popularity_cutoff = st.session_state.get("reviews", 40)
    map_filter = st.session_state.get("map_filter", "All restaurants")

    # Show results table if query is active
    if nl_query and applied_query:
        validation = validate_query(nl_query, vocab)
        if validation.ok:
            results_df = search(
                search_index, df, validation.parsed,
                min_rating=rating_cutoff, min_reviews=popularity_cutoff
            )

            if len(results_df) > 0:
                st.subheader("Search results")
                # Rename columns for display
                display_df = results_df.copy()
                display_df.columns = ["Name", "Cuisine", "District", "Rating", "Reviews", "Lat", "Lng"]
                st.dataframe(
                    display_df[["Name", "Cuisine", "District", "Rating", "Reviews"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No restaurants match your search criteria.")

    # Filter data by cuisine and district
    df_filtered = update_df_based_on_selected_cusine_and_district(df, cuisine, district)

    # Explore map
    st.subheader("Explore Berlin")

    # Apply map filter
    if map_filter == "Only good restaurants":
        df_map = df_filtered[
            (df_filtered["rating"] >= rating_cutoff) &
            (df_filtered["userRatingsTotal"] >= popularity_cutoff)
        ]
    elif map_filter == "Only low rated restaurants":
        df_map = df_filtered[df_filtered["rating"] < 4.0]
    else:  # All restaurants
        df_map = df_filtered

    # Build and show map
    m = get_map_instance()
    m = generating_circles(m, df_map)
    show_map(m, key="explore_map")

    # KPI metrics
    st.subheader("Market insights")
    col1, col2, col3 = st.columns(3)

    with col1:
        count = len(df_filtered)
        good_count = len(df_filtered[
            (df_filtered["rating"] >= rating_cutoff) &
            (df_filtered["userRatingsTotal"] >= popularity_cutoff)
        ])
        st.metric("Total restaurants", count)
        st.caption(f"{good_count} are 'good'")

    with col2:
        avg_rating = df_filtered["rating"].mean()
        st.metric("Average rating", f"{avg_rating:.2f}" if not st.session_state.get("_nan") else "—")

    with col3:
        avg_reviews = df_filtered["userRatingsTotal"].mean()
        st.metric("Avg reviews", int(avg_reviews) if not st.session_state.get("_nan") else "—")

    # Key points
    st.subheader("Key points")

    points = []

    # Point 1: Best district by count
    if cuisine != "All" or district != "All":
        dist_counts = restaurant_count_by_district(df_filtered)
        if len(dist_counts) > 0:
            top_district = dist_counts.index[0]
            top_count = dist_counts.iloc[0]
            points.append(f"**{top_district}** has the most restaurants ({int(top_count)})")

    # Point 2: Best cuisine by rating
    if district == "All":
        cuisine_ratings = avg_rating_by_cuisine(df_filtered)
        if len(cuisine_ratings) > 0:
            top_cuisine = cuisine_ratings.index[0]
            top_rating = cuisine_ratings.iloc[0]
            points.append(f"**{top_cuisine}** has the highest average rating ({top_rating:.2f})")

    # Point 3: Number of "good" restaurants
    good = good_restaurants_count(df_filtered, rating_cutoff, popularity_cutoff)
    points.append(f"**{int(good)}** restaurants meet the 'good' criteria")

    if points:
        for point in points[:3]:  # Show top 3
            st.markdown(f"• {point}")
    else:
        st.info("No data available for this selection.")
