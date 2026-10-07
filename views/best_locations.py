"""Find best locations page: address search and site suitability analysis."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from next_restaurant.functions_for_df import (
    update_df_based_on_selected_cusine_and_district,
    nearby_restaurants, get_map_instance, generating_circles, show_map
)
from next_restaurant.features_to_suggest import find_best_location
from next_restaurant.stats import neighbours_stats, calc_centers
from next_restaurant.app_state import load_data
from next_restaurant.parameters import geocode_address


def render():
    """Render Find best locations page."""
    # Load data
    df = load_data()

    # Get session state
    cuisine = st.session_state.get("cuisine", "All")
    district = st.session_state.get("district", "All")
    rating_cutoff = st.session_state.get("rating", 4.5)
    popularity_cutoff = st.session_state.get("reviews", 40)
    address = st.session_state.get("address", "Mitte, Berlin")
    nearby = st.session_state.get("nearby", 20)

    # Page intro
    st.markdown("**Find the best location to open** based on your address and nearest competitors.")

    # Input section
    with st.container(border=True):
        st.caption("Your search area")
        col1, col2 = st.columns([3, 1])

        with col1:
            st.text_input(
                "Address or location",
                key="address",
                placeholder="e.g., Kreuzberg, Berlin",
                help="Enter a Berlin address or district name.",
            )

        with col2:
            st.slider(
                "Range (km)",
                min_value=1,
                max_value=50,
                key="nearby",
                help="Search radius for nearby competitors.",
            )

    # Geocode address
    try:
        lat, lng = geocode_address(st.session_state.address)
    except Exception:
        st.error(f"Could not find '{st.session_state.address}'. Please try another address.")
        return

    # Get nearby restaurants
    df_filtered = update_df_based_on_selected_cusine_and_district(df, cuisine, district)
    df_nearby = nearby_restaurants(df_filtered, lat, lng, st.session_state.nearby)

    if len(df_nearby) == 0:
        st.warning("No restaurants found in this area. Try a larger radius.")
        return

    # Your closest competitors
    st.subheader("Your closest competitors")

    # Show stats
    stats = neighbours_stats(df_nearby, lat, lng, rating_cutoff, popularity_cutoff)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total nearby", len(df_nearby))
    with col2:
        st.metric("Good rated", stats.get("good_count", 0))
    with col3:
        st.metric("Avg rating", f"{stats.get('avg_rating', 0):.2f}")

    # Competitors table
    display_df = df_nearby[["namesClean", "foodType", "rating", "userRatingsTotal", "distance"]].copy()
    display_df.columns = ["Name", "Cuisine", "Rating", "Reviews", "Distance (km)"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Where to open
    st.subheader("Where to open")

    # Find best locations
    best_locations = find_best_location(
        df_nearby, lat, lng,
        min_rating=rating_cutoff,
        min_reviews=popularity_cutoff
    )

    if len(best_locations) > 0:
        st.slider(
            "Show top N suggestions",
            min_value=1,
            max_value=min(10, len(best_locations)),
            value=5,
            key="location_count",
            help="Number of best locations to display on the map."
        )

        # Build map with suggestions
        m = get_map_instance()

        # Add existing restaurants
        m = generating_circles(m, df_nearby)

        # Add suggestions as green markers
        n_to_show = st.session_state.location_count
        for idx, (loc_lat, loc_lng) in enumerate(best_locations[:n_to_show]):
            folium = __import__("folium")
            folium.CircleMarker(
                location=[loc_lat, loc_lng],
                radius=8,
                popup=f"Suggestion #{idx+1}",
                color="green",
                fill=True,
                fill_color="green",
                fill_opacity=0.8,
                weight=2,
            ).add_to(m)

        show_map(m, key="best_locations_map")
    else:
        st.info("No suitable locations found. Try adjusting your filters.")
