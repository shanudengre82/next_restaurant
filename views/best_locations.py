"""Find best locations page: address search and site suitability analysis."""

import sys
from pathlib import Path

import streamlit as st
from geopy.geocoders import Nominatim

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from next_restaurant.functions_for_df import (
    update_df_based_on_selected_cusine_and_district,
    get_map_instance,
    generating_circles,
    show_map,
)
from next_restaurant.features_to_suggest import (
    k_neighbours_df,
    calc_centers,
    neighbours_stats,
)
from next_restaurant.local_search_coordinates import (
    generating_circular_coordinates,
    get_locating_best_place_based_on_distance,
)
from next_restaurant.cuisine_stats_display import (
    display_additional_stats,
    display_suggestions_text,
)
from next_restaurant.app_state import load_data
from next_restaurant.parameters import HEIGHT


def render():
    """Render Find best locations page."""
    df = load_data()

    # Get sidebar state
    cuisine = st.session_state.get("cuisine", "All")
    district = st.session_state.get("district", "All")
    rating_cutoff = st.session_state.get("rating", 4.5)
    popularity_cutoff = st.session_state.get("reviews", 40)

    # Input section
    st.header("Find best locations")
    st.markdown("Analyze a specific address for site suitability based on existing competitors.")

    with st.container(border=True):
        st.caption("Your search area")
        col1, col2 = st.columns([3, 1])

        with col1:
            address = st.text_input(
                "Address or location",
                key="address",
                placeholder="e.g., Kreuzberg, Berlin",
                help="Enter a Berlin address or district name.",
            )

        with col2:
            nearby = st.slider(
                "Range (km)",
                min_value=1,
                max_value=50,
                key="nearby",
                value=st.session_state.get("nearby", 20),
                help="Search radius for nearby competitors.",
            )

    if not address:
        st.info("Enter an address to begin.")
        return

    # Geocode address
    try:
        geolocator = Nominatim(user_agent="next_restaurant", timeout=10)
        location = geolocator.geocode(address, timeout=10)
        if not location:
            st.error(f"Could not find '{address}'. Please try another address.")
            return
        local_lat, local_lng = location.latitude, location.longitude
    except Exception as e:
        st.error(f"Error geocoding address: {str(e)}")
        return

    # Filter and get nearby restaurants
    df_filtered = update_df_based_on_selected_cusine_and_district(df, cuisine, district)
    df_local = k_neighbours_df(
        df_filtered,
        local_lat,
        local_lng,
        n_restaurants=nearby * 50,  # Approximate
    )

    # Filter by range
    df_local = df_local[df_local["distance"] <= nearby]

    if len(df_local) == 0:
        st.warning(f"No restaurants found within {nearby} km. Try a larger radius.")
        return

    # Your closest competitors
    st.header("Your closest competitors")

    # Get statistics
    df_local_copy = df_local.copy()
    df_local_copy["ratings_color"] = df_local_copy["rating"].apply(
        lambda x: "orange" if x < rating_cutoff else "blue"
    )
    stats = neighbours_stats(df_local_copy)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total nearby", len(df_local))
    with col2:
        good_count = len(
            df_local[
                (df_local["rating"] >= rating_cutoff)
                & (df_local["userRatingsTotal"] >= popularity_cutoff)
            ]
        )
        st.metric("Rated as good", good_count)
    with col3:
        avg_rating = df_local["rating"].mean()
        st.metric("Avg rating", f"{avg_rating:.2f}")

    display_additional_stats(
        most_frq_priceLevel=stats[0],
        avg_rating=stats[1],
        good_restaurants_per=stats[4],
        best_competitor=stats[2],
    )

    # Competitors table
    st.subheader("Nearest restaurants to your address")
    _nearby = df_local.sort_values("distance").head(15)[
        ["namesClean", "foodType", "rating", "userRatingsTotal", "priceLevel", "distance"]
    ]
    st.dataframe(
        _nearby.rename(
            columns={
                "namesClean": "Name",
                "foodType": "Cuisine",
                "rating": "Rating",
                "userRatingsTotal": "Reviews",
                "priceLevel": "Price level",
                "distance": "Distance (km)",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    # Where to open section
    st.header("Where to open")
    display_suggestions_text()

    # Calculate centers and find best locations
    center_bad_center_good = calc_centers(df_local, rating_cutoff)

    if isinstance(center_bad_center_good, dict):
        first_key = next(iter(center_bad_center_good))
        coords = generating_circular_coordinates(
            center_bad_center_good[first_key], local_lat, local_lng, 2
        )
        best_places = get_locating_best_place_based_on_distance(coords, df_local, local_lat, local_lng)

        if len(best_places) > 0:
            n_suggestions = st.slider(
                "Show top N suggestions",
                min_value=1,
                max_value=min(10, len(best_places)),
                value=min(5, len(best_places)),
                key="location_count",
            )

            # Build map with suggestions
            m = get_map_instance(
                zoom=13, initial_location=[local_lat, local_lng], height=HEIGHT
            )

            # Add existing restaurants (reuse df_local_copy with ratings_color from above)
            m = generating_circles(m, df_local_copy, color="ratings_color")

            # Add suggestions as green markers
            import folium

            for idx, (loc_lat, loc_lng) in enumerate(best_places[:n_suggestions]):
                folium.CircleMarker(
                    location=[loc_lat, loc_lng],
                    radius=8,
                    popup=f"Suggestion #{idx + 1}",
                    color="green",
                    fill=True,
                    fill_color="green",
                    fill_opacity=0.8,
                    weight=2,
                ).add_to(m)

            show_map(m, key="best_locations_map", height=HEIGHT)
        else:
            st.info("No suitable locations found. Try adjusting your filters.")
    else:
        st.info("Unable to analyze this area. Try a different location.")
