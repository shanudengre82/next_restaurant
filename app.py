"""Next Restaurant: multipage Streamlit app with sidebar search."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from next_restaurant.app_state import (
    DEFAULTS,
    EXAMPLES,
    use_example,
    apply_preset,
    reset_filters,
    load_data,
    load_search_stack,
)
from next_restaurant.cuisine_info import CUISINE_OPTIONS
from next_restaurant.district import BERLIN_DISTRICTS
from next_restaurant.nlp_search import validate_query, selections_from_query
from next_restaurant.ui import inject_theme

st.set_page_config(page_title="NEXT RESTAURANT", initial_sidebar_state="expanded", layout="wide")

# Apply theme
inject_theme()

# Initialize session state
for _key, _value in DEFAULTS.items():
    st.session_state.setdefault(_key, _value)

# Keep-alive: preserve page-2-only widgets when navigating to page 1
st.session_state.setdefault("address", DEFAULTS["address"])
st.session_state.setdefault("nearby", DEFAULTS["nearby"])

# Load data
df = load_data()
vocab, search_index = load_search_stack(df)

# SIDEBAR
st.sidebar.title("Your filters")

# Natural language search box
nl_query = st.sidebar.text_input(
    "Describe what you're looking for",
    placeholder="e.g., top rated italian in mitte",
    key="nl_query",
    help="Examples: 'italian', 'sushi in kreuzberg', 'top rated', '100+ reviews', 'above 4.5'",
)

# Example buttons
st.sidebar.caption("Try an example")
for example in EXAMPLES:
    st.sidebar.button(
        example,
        key=f"example_{example}",
        on_click=use_example,
        args=(example,),
        use_container_width=True,
    )

# Query application logic
query_feedback = ""
if nl_query and nl_query != st.session_state.applied_query:
    validation = validate_query(nl_query, vocab)
    if validation.ok:
        parsed = validation.parsed
        selections = selections_from_query(parsed, CUISINE_OPTIONS, BERLIN_DISTRICTS)
        # Apply selections before widgets are created
        if selections.cuisine:
            st.session_state.cuisine = selections.cuisine
        if selections.district:
            st.session_state.district = selections.district
        if selections.rating is not None:
            st.session_state.rating = selections.rating
        if selections.reviews is not None:
            st.session_state.reviews = selections.reviews
        # Build feedback text
        feedback_parts = []
        if selections.cuisine:
            feedback_parts.append(f"Cuisine: {selections.cuisine}")
        if selections.district:
            feedback_parts.append(f"District: {selections.district}")
        if selections.rating is not None:
            feedback_parts.append(f"Rating ≥ {selections.rating}")
        if selections.reviews is not None:
            feedback_parts.append(f"Reviews ≥ {selections.reviews}")
        query_feedback = " · ".join(feedback_parts)
        if selections.notes:
            query_feedback += "\n" + "\n".join(selections.notes)
        st.session_state.applied_query = nl_query
    else:
        st.sidebar.warning(validation.message)
elif nl_query:
    # Show feedback if query hasn't changed
    validation = validate_query(nl_query, vocab)
    if validation.ok:
        parsed = validation.parsed
        selections = selections_from_query(parsed, CUISINE_OPTIONS, BERLIN_DISTRICTS)
        feedback_parts = []
        if selections.cuisine:
            feedback_parts.append(f"Cuisine: {selections.cuisine}")
        if selections.district:
            feedback_parts.append(f"District: {selections.district}")
        if selections.rating is not None:
            feedback_parts.append(f"Rating ≥ {selections.rating}")
        if selections.reviews is not None:
            feedback_parts.append(f"Reviews ≥ {selections.reviews}")
        query_feedback = " · ".join(feedback_parts)

if query_feedback:
    st.sidebar.caption(f"**Applied:** {query_feedback}")

# Reset button
st.sidebar.button("Reset filters", on_click=reset_filters, use_container_width=True)

# Sidebar filters
with st.sidebar.expander("Where & what", expanded=True):
    st.selectbox(
        "Cuisine",
        CUISINE_OPTIONS,
        key="cuisine",
        help="Pick a cuisine or 'All' to look at every type of restaurant.",
    )
    st.selectbox(
        "District",
        BERLIN_DISTRICTS,
        key="district",
        help="Pick a district or 'All' to look at the whole city.",
    )

with st.sidebar.expander("Quality thresholds", expanded=True):
    st.slider(
        "Minimum rating",
        min_value=2.0,
        max_value=5.0,
        step=0.1,
        key="rating",
        help="Restaurants at or above this rating count as good.",
    )
    st.slider(
        "Minimum reviews",
        min_value=0,
        max_value=2000,
        step=1,
        key="reviews",
        help="Ignore restaurants with fewer reviews than this.",
    )

with st.sidebar.expander("Map", expanded=True):
    st.radio(
        "Show on the map",
        ["All restaurants", "Only good restaurants", "Only low rated restaurants"],
        key="map_filter",
    )

with st.sidebar.expander("About", expanded=False):
    st.markdown(
        """
**How it works**

**Data.** Ratings, review counts, price levels and locations of restaurants in
Berlin, grouped by district and cuisine.

**What is a good restaurant?** One with a rating at or above your minimum rating
and at least your minimum number of reviews (set in the sidebar).

**Where to open.** Around your address we take the nearest restaurants, locate the
centre of the high and low rated ones, and search a grid of points for the places
furthest from any existing restaurant. Those are the green markers.

**Good to know.** The data is a snapshot and ratings are only a proxy for demand.
Use the results as a starting point, not as a final decision.
        """
    )
    st.markdown(
        "Built with Python, pandas, Streamlit and Folium. "
        "Source code: [github.com/shanudengre82/next_restaurant]"
        "(https://github.com/shanudengre82/next_restaurant)"
    )

# Main title and intro
st.title("Next Restaurant")
st.markdown(
    "##### Find the best place to open your next restaurant in Berlin, "
    "backed by the ratings of existing restaurants."
)

# Use-case cards
USE_CASES = [
    (
        "Pick a district & cuisine",
        "Is a cuisine under-served or already crowded in the district you like?",
        ("Italian", "Mitte", "Mitte, Berlin"),
    ),
    (
        "Scout an address",
        "See the closest competitors, their price level and average rating.",
        ("All", "All", "Kreuzberg, Berlin"),
    ),
    (
        "Find the gap",
        "Get map markers for spots furthest from nearby restaurants.",
        ("Asian", "Friedrichshain", "Friedrichshain, Berlin"),
    ),
    (
        "Understand the market",
        "Compare districts and cuisines by how many restaurants are rated good.",
        ("All", "All", "Mitte, Berlin"),
    ),
]

_cols = st.columns(len(USE_CASES))
for _col, (_title, _text, _preset) in zip(_cols, USE_CASES):
    with _col.container(border=True):
        st.markdown(f"**{_title}**")
        st.caption(_text)
        st.button(
            _title,
            key=f"preset_{_title}",
            on_click=apply_preset,
            args=_preset,
            use_container_width=True,
        )

st.caption(
    "Use the search box or filters on the left, then scroll down to see results and explore further."
)

# Page navigation
def explore_page():
    """Load and render Explore Berlin page."""
    from views import explore
    explore.render()

def best_locations_page():
    """Load and render Find best locations page."""
    from views import best_locations
    best_locations.render()

# Use st.navigation for page routing
pages = [
    st.Page(explore_page, title="Explore Berlin"),
    st.Page(best_locations_page, title="Find best locations"),
]

pg = st.navigation(pages)
pg.run()
