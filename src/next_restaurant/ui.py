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
