"""UI theme and styling helpers for Berlin enamel street sign aesthetic."""

import streamlit as st


def inject_theme():
    """Inject CSS for Berlin enamel street sign theme with Barlow font."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@600&display=swap');

        * {
            font-family: 'Barlow', sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Barlow Condensed', sans-serif;
            font-weight: 600;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #17375E;
        }

        /* Sidebar text - only direct elements on enamel background */
        [data-testid="stSidebar"] > div > div > div label,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] h5,
        [data-testid="stSidebar"] h6 {
            color: white !important;
        }

        /* Sidebar captions - slightly muted white */
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #E4EAF1 !important;
        }

        /* Sidebar text inputs - dark text on white */
        [data-testid="stSidebar"] .stTextInput input {
            background-color: #FAFAF8 !important;
            color: #1B1F24 !important;
            border: 1px solid #E4EAF1 !important;
        }

        [data-testid="stSidebar"] .stTextInput input::placeholder {
            color: #5B6672 !important;
        }

        /* Sidebar select boxes - dark text on white */
        [data-testid="stSidebar"] [data-baseweb="select"] * {
            color: #1B1F24 !important;
        }

        [data-testid="stSidebar"] .stSelectbox > div > div {
            background-color: #FAFAF8 !important;
        }

        /* Sidebar alerts/warnings - dark text on their own background */
        [data-testid="stSidebar"] [data-testid="stAlert"] * {
            color: #1B1F24 !important;
        }

        /* Sidebar sliders */
        [data-testid="stSidebar"] .stSlider label {
            color: white !important;
        }

        /* Sidebar radio buttons - white text for labels */
        [data-testid="stSidebar"] .stRadio label {
            color: white !important;
        }

        /* Sidebar buttons - translucent white with focus ring */
        [data-testid="stSidebar"] button {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            font-family: 'Barlow', sans-serif;
            border-radius: 6px;
        }

        [data-testid="stSidebar"] button:hover {
            background-color: rgba(255, 255, 255, 0.3) !important;
        }

        [data-testid="stSidebar"] button:focus {
            outline: 2px solid #FAFAF8 !important;
            outline-offset: 2px !important;
        }

        /* Dropdown/popover styling (opens outside sidebar) */
        [data-baseweb="popover"] [data-baseweb="menu"],
        ul[role="listbox"] {
            background-color: #FAFAF8 !important;
            border: 1px solid #E4EAF1 !important;
        }

        [data-baseweb="popover"] li,
        [data-baseweb="popover"] li *,
        [role="option"],
        [role="option"] * {
            color: #1B1F24 !important;
        }

        [role="option"]:hover,
        [role="option"][aria-selected="true"] {
            background-color: #E4EAF1 !important;
            color: #1B1F24 !important;
        }

        [role="option"][aria-selected="true"] {
            font-weight: 600;
        }

        /* Select clear button and icons */
        [data-baseweb="select"] svg {
            fill: #1B1F24 !important;
            color: #1B1F24 !important;
        }

        /* Main content background */
        .main {
            background-color: #FAFAF8;
            color: #1B1F24;
        }

        /* Border and divider colors */
        hr {
            border-color: #E4EAF1 !important;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #E4EAF1 !important;
            color: #1B1F24 !important;
        }

        /* Table striping */
        [data-testid="dataFrameContainer"] tbody tr:nth-child(odd) {
            background-color: #FAFAF8;
        }

        [data-testid="dataFrameContainer"] tbody tr:nth-child(even) {
            background-color: #E4EAF1;
        }

        /* Metric cards */
        [data-testid="metric-container"] {
            border: 1px solid #E4EAF1;
            border-radius: 6px;
            padding: 1rem;
            background-color: white;
        }

        /* Map loading spinner */
        @keyframes map-spin {
            to { transform: rotate(360deg); }
        }

        .map-loader {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            background-color: #FAFAF8;
            border: 1px solid #E4EAF1;
            border-radius: 6px;
            color: #17375E;
            font-weight: 500;
        }

        .map-loader-ring {
            width: 48px;
            height: 48px;
            border: 5px solid #E4EAF1;
            border-top-color: #17375E;
            border-radius: 50%;
            animation: map-spin 0.9s linear infinite;
        }

        /* Spinner behind the map iframe, visible until Leaflet paints over it */
        [class*="st-key-map_wrap_"] {
            position: relative;
        }

        [class*="st-key-map_wrap_"]::before {
            content: "";
            position: absolute;
            top: calc(50% - 40px);
            left: calc(50% - 24px);
            width: 48px;
            height: 48px;
            box-sizing: border-box;
            border: 5px solid #E4EAF1;
            border-top-color: #17375E;
            border-radius: 50%;
            animation: map-spin 0.9s linear infinite;
            z-index: 0;
        }

        [class*="st-key-map_wrap_"]::after {
            content: "Loading map…";
            position: absolute;
            top: calc(50% + 20px);
            left: 0;
            right: 0;
            text-align: center;
            color: #17375E;
            font-weight: 500;
            z-index: 0;
        }

        [class*="st-key-map_wrap_"] iframe {
            position: relative;
            z-index: 1;
        }

        /* Main buttons */
        .main button {
            font-family: 'Barlow', sans-serif;
            border-radius: 6px;
            background-color: #17375E !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def map_loader_html(height: int) -> str:
    """Return a map-sized placeholder with a circular spinner and loading text."""
    return (
        f'<div class="map-loader" style="height: {height}px;">'
        '<div class="map-loader-ring"></div>'
        "<div>Loading map…</div>"
        "</div>"
    )


def sign_title(text: str) -> None:
    """Render title as Berlin enamel street sign plate."""
    st.markdown(
        f"""
        <style>
        .sign-plate {{
            background-color: #17375E;
            color: white;
            padding: 1.5rem 2rem;
            border: 3px solid white inset;
            border-radius: 6px;
            text-align: center;
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 2.5rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        </style>
        <div class="sign-plate">{text}</div>
        """,
        unsafe_allow_html=True,
    )
