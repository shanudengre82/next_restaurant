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

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > div {
            color: white;
        }

        [data-testid="stSidebar"] label {
            color: white;
        }

        [data-testid="stSidebar"] .stTextInput > div > div > input {
            background-color: #FAFAF8;
            color: #1B1F24;
        }

        [data-testid="stSidebar"] .stSelectbox > div > div > div {
            background-color: #FAFAF8;
            color: #1B1F24;
        }

        [data-testid="stSidebar"] .stSlider > div > div {
            color: white;
        }

        /* Main content background */
        body {
            background-color: #FAFAF8;
            color: #1B1F24;
        }

        /* Border and divider colors */
        hr {
            border-color: #E4EAF1;
        }

        .streamlit-expanderHeader {
            background-color: #E4EAF1;
        }

        /* Map and container borders */
        [data-testid="stContainer"] {
            border-color: #E4EAF1;
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
        }

        /* Buttons */
        button {
            font-family: 'Barlow', sans-serif;
            border-radius: 6px;
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
