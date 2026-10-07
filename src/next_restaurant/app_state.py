"""Shared app state and helpers for Streamlit multipage app."""

import streamlit as st
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / ".."))

from next_restaurant.get_data import get_raw_data
from next_restaurant.nlp_search import RestaurantIndex, build_vocabulary

# Sidebar search examples
EXAMPLES = [
    "Italian in Kreuzberg",
    "Top rated sushi in Mitte",
    "Pizza with 100+ reviews",
    "Vegan in Prenzlauer Berg",
    "Turkish above 4.5"
]

DEFAULTS = {
    "cuisine": "All",
    "district": "All",
    "address": "Mitte, Berlin",
    "rating": 4.5,
    "reviews": 40,
    "map_filter": "All restaurants",
    "nearby": 20,
    "nl_query": "",
    "applied_query": "",
}

def use_example(text: str) -> None:
    """Callback: set search query to example text and clear applied state."""
    st.session_state.nl_query = text
    st.session_state.applied_query = ""

def apply_preset(cuisine: str, district: str, address: str) -> None:
    """Apply use-case preset to session state."""
    st.session_state.update(cuisine=cuisine, district=district, address=address, nl_query="", applied_query="")

def reset_filters() -> None:
    """Reset all filters to defaults."""
    st.session_state.update(DEFAULTS)

def load_data():
    """Load and cache the raw data with error handling."""
    try:
        return get_raw_data()
    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        st.error("Unable to load data file, please reach out to shanudengre82@gmail.com")
        st.stop()

@st.cache_resource
def load_search_stack(_df):
    """Build and cache vocabulary and search index."""
    vocab = build_vocabulary(_df)
    index = RestaurantIndex.build(_df)
    return vocab, index
