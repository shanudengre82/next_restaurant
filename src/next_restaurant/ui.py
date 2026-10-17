"""UI themes and styling helpers.

Each theme is a set of design tokens that are emitted as CSS variables
(--nr-*), so the stylesheet below stays the same for every theme.
"""

import html
from dataclasses import dataclass, fields

import streamlit as st


@dataclass(frozen=True)
class Theme:
    label: str
    font_import: str
    font_body: str
    font_heading: str
    primary: str
    on_primary: str
    bg: str
    surface: str
    border: str
    text: str
    muted: str
    sidebar_bg: str
    sidebar_text: str
    sidebar_muted: str
    input_bg: str
    input_text: str
    focus: str
    marker_high: str
    marker_low: str
    marker_suggest: str
    tile_filter: str


_GOOGLE_FONTS = "https://fonts.googleapis.com/css2?display=swap&family="

THEMES = {
    "enamel": Theme(
        label="Berlin Enamel",
        font_import=_GOOGLE_FONTS + "Barlow:wght@400;500;600&family=Barlow+Condensed:wght@600",
        font_body="'Barlow', sans-serif",
        font_heading="'Barlow Condensed', sans-serif",
        primary="#17375E",
        on_primary="#FFFFFF",
        bg="#FAFAF8",
        surface="#E4EAF1",
        border="#E4EAF1",
        text="#1B1F24",
        muted="#5B6672",
        sidebar_bg="#17375E",
        sidebar_text="#FFFFFF",
        sidebar_muted="#E4EAF1",
        input_bg="#FAFAF8",
        input_text="#1B1F24",
        focus="#17375E",
        marker_high="#17375E",
        marker_low="#D9480F",
        marker_suggest="#2B8A3E",
        tile_filter="none",
    ),
    "night": Theme(
        label="Night",
        font_import=_GOOGLE_FONTS + "Barlow:wght@400;500;600&family=Barlow+Condensed:wght@600",
        font_body="'Barlow', sans-serif",
        font_heading="'Barlow Condensed', sans-serif",
        primary="#7AB8FF",
        on_primary="#0B0F14",
        bg="#12161C",
        surface="#1C232C",
        border="#2A3340",
        text="#E6EAF0",
        muted="#9AA5B1",
        sidebar_bg="#0B0F14",
        sidebar_text="#E6EAF0",
        sidebar_muted="#9AA5B1",
        input_bg="#1C232C",
        input_text="#E6EAF0",
        focus="#7AB8FF",
        marker_high="#4DA3FF",
        marker_low="#FF8A3D",
        marker_suggest="#3DDC84",
        tile_filter="invert(1) hue-rotate(180deg) brightness(0.9) contrast(0.9)",
    ),
    "kiez": Theme(
        label="Kiez Warm",
        font_import=_GOOGLE_FONTS + "Nunito+Sans:wght@400;600&family=Fraunces:wght@600",
        font_body="'Nunito Sans', sans-serif",
        font_heading="'Fraunces', serif",
        primary="#B5452B",
        on_primary="#FFFFFF",
        bg="#FBF6EE",
        surface="#F1E6D6",
        border="#E6D5BF",
        text="#2B211C",
        muted="#6E5E52",
        sidebar_bg="#7A2E1E",
        sidebar_text="#FFF8EF",
        sidebar_muted="#F1E6D6",
        input_bg="#FFFBF5",
        input_text="#2B211C",
        focus="#B5452B",
        marker_high="#2F5D62",
        marker_low="#C2410C",
        marker_suggest="#4D7C0F",
        tile_filter="sepia(0.35) saturate(0.9)",
    ),
    "spree": Theme(
        label="Spree Green",
        font_import=_GOOGLE_FONTS + "Source+Sans+3:wght@400;600&family=Bitter:wght@600",
        font_body="'Source Sans 3', sans-serif",
        font_heading="'Bitter', serif",
        primary="#1F5E3B",
        on_primary="#FFFFFF",
        bg="#F7FAF7",
        surface="#E3EEE6",
        border="#D3E2D7",
        text="#18231C",
        muted="#55665B",
        sidebar_bg="#1F4D36",
        sidebar_text="#F2FAF4",
        sidebar_muted="#D3E2D7",
        input_bg="#FFFFFF",
        input_text="#18231C",
        focus="#1F5E3B",
        marker_high="#1D4ED8",
        marker_low="#C2410C",
        marker_suggest="#15803D",
        tile_filter="grayscale(1) brightness(1.05)",
    ),
    "contrast": Theme(
        label="High contrast",
        font_import=_GOOGLE_FONTS + "Atkinson+Hyperlegible:wght@400;700",
        font_body="'Atkinson Hyperlegible', sans-serif",
        font_heading="'Atkinson Hyperlegible', sans-serif",
        primary="#000000",
        on_primary="#FFFFFF",
        bg="#FFFFFF",
        surface="#F2F2F2",
        border="#000000",
        text="#000000",
        muted="#333333",
        sidebar_bg="#000000",
        sidebar_text="#FFFFFF",
        sidebar_muted="#FFFFFF",
        input_bg="#FFFFFF",
        input_text="#000000",
        focus="#FFD400",
        marker_high="#0033CC",
        marker_low="#CC3300",
        marker_suggest="#007A33",
        tile_filter="contrast(1.15)",
    ),
}

DEFAULT_THEME = "enamel"


def init_theme() -> Theme:
    """Resolve the theme from the URL or session and keep both in sync."""
    slug = st.query_params.get("theme") or st.session_state.get("theme", DEFAULT_THEME)
    if slug not in THEMES:
        slug = DEFAULT_THEME
    st.session_state["theme"] = slug
    # Page navigation drops query params, so write it back on every run
    if st.query_params.get("theme") != slug:
        st.query_params["theme"] = slug
    return THEMES[slug]


def current_theme() -> Theme:
    """Return the theme chosen for this session."""
    return THEMES.get(st.session_state.get("theme", DEFAULT_THEME), THEMES[DEFAULT_THEME])


def sync_theme_query_param() -> None:
    """Widget callback: store the picked theme in the URL."""
    st.query_params["theme"] = st.session_state["theme"]


def _css_variables(theme: Theme) -> str:
    tokens = (f for f in fields(theme) if f.name not in ("label", "font_import"))
    return "\n".join(
        f"    --nr-{f.name.replace('_', '-')}: {getattr(theme, f.name)};" for f in tokens
    )


_STYLESHEET = """
/* Fonts (Material icon spans keep their own icon font) */
.stApp, .stApp :is(p, li, label, input, textarea, button, td, th, div, span):not([data-testid="stIconMaterial"]) {
    font-family: var(--nr-font-body);
}

.stApp :is(h1, h2, h3, h4, h5, h6),
.stApp :is(h1, h2, h3, h4, h5, h6) * {
    font-family: var(--nr-font-heading) !important;
    font-weight: 600;
}

/* Page background and text */
.stApp,
[data-testid="stHeader"] {
    background-color: var(--nr-bg) !important;
    color: var(--nr-text);
}

[data-testid="stMain"] :is(p, li, label, h1, h2, h3, h4, h5, h6, td, th),
[data-testid="stMain"] [data-testid="stWidgetLabel"] * {
    color: var(--nr-text);
}

[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stMain"] [data-testid="stCaptionContainer"] * {
    color: var(--nr-muted) !important;
}

[data-testid="stMain"] a {
    color: var(--nr-primary);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: var(--nr-sidebar-bg);
}

/* Sidebar text - only direct elements on the sidebar background */
[data-testid="stSidebar"] > div > div > div label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSidebar"] [data-testid="stExpander"] summary *,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: var(--nr-sidebar-text) !important;
}

/* Sidebar captions - slightly muted */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: var(--nr-sidebar-muted) !important;
}

[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border-color: rgba(255, 255, 255, 0.3);
}

[data-testid="stExpander"] summary {
    background-color: transparent !important;
}

/* Text inputs and select boxes */
.stTextInput input,
.stNumberInput input,
.stSelectbox [role="group"],
[data-baseweb="select"] > div {
    background-color: var(--nr-input-bg) !important;
    color: var(--nr-input-text) !important;
    border-color: var(--nr-border) !important;
}

.stTextInput input::placeholder,
.stSelectbox input::placeholder {
    color: var(--nr-muted) !important;
}

.stSelectbox [role="group"] *,
[data-baseweb="select"] * {
    color: var(--nr-input-text) !important;
}

.stSelectbox svg,
[data-baseweb="select"] svg {
    fill: var(--nr-input-text) !important;
    color: var(--nr-input-text) !important;
}

/* Sidebar alerts/warnings - dark text on their own background */
[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #1B1F24 !important;
}

/* Sidebar sliders and radio buttons */
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stSliderTickBarMax"],
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio label * {
    color: var(--nr-sidebar-text) !important;
}

/* Sidebar buttons - translucent with focus ring */
[data-testid="stSidebar"] button {
    background-color: rgba(255, 255, 255, 0.2) !important;
    color: var(--nr-sidebar-text) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 6px;
}

[data-testid="stSidebar"] button * {
    color: var(--nr-sidebar-text) !important;
}

[data-testid="stSidebar"] button:hover {
    background-color: rgba(255, 255, 255, 0.3) !important;
}

/* ...except the select box's own chevron button */
[data-testid="stSidebar"] .stSelectbox button {
    background-color: transparent !important;
    border: none !important;
}

[data-testid="stSidebar"] .stSelectbox button * {
    color: var(--nr-input-text) !important;
}

/* Main buttons */
[data-testid="stMain"] button[kind^="secondary"],
[data-testid="stMain"] button[kind^="primary"] {
    border-radius: 6px;
    background-color: var(--nr-primary) !important;
    border-color: var(--nr-primary) !important;
    color: var(--nr-on-primary) !important;
}

[data-testid="stMain"] button[kind^="secondary"] *,
[data-testid="stMain"] button[kind^="primary"] * {
    color: var(--nr-on-primary) !important;
}

[data-testid="stMain"] button[kind^="secondary"]:hover,
[data-testid="stMain"] button[kind^="primary"]:hover {
    filter: brightness(1.1);
}

/* Focus rings */
.stApp button:focus-visible,
.stApp input:focus-visible,
.stApp [role="slider"]:focus-visible {
    outline: 3px solid var(--nr-focus) !important;
    outline-offset: 2px !important;
}

/* Slider, radio and checkbox accents (the slider thumb is the translated handle) */
.stSlider [style*="translate(-50%, -50%)"] {
    background-color: var(--nr-primary) !important;
    border-color: var(--nr-primary) !important;
}

[data-testid="stSidebar"] .stSlider [style*="translate(-50%, -50%)"] {
    background-color: var(--nr-sidebar-text) !important;
    border-color: var(--nr-sidebar-text) !important;
}

.stApp input[type="radio"],
.stApp input[type="checkbox"] {
    accent-color: var(--nr-primary);
}

/* Dropdown/popover styling (opens outside sidebar) */
[data-baseweb="popover"] [data-baseweb="menu"],
ul[role="listbox"] {
    background-color: var(--nr-input-bg) !important;
    border: 1px solid var(--nr-border) !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] li *,
[role="option"],
[role="option"] * {
    color: var(--nr-input-text) !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background-color: var(--nr-surface) !important;
    color: var(--nr-input-text) !important;
}

[role="option"][aria-selected="true"] {
    font-weight: 600;
}

/* Border and divider colors */
hr {
    border-color: var(--nr-border) !important;
}

/* Bordered containers and expanders (border-color only shows where a border is drawn) */
[data-testid="stMain"] [data-testid="stVerticalBlock"],
[data-testid="stMain"] [data-testid="stExpander"] details {
    border-color: var(--nr-border) !important;
}

/* Table striping */
[data-testid="dataFrameContainer"] tbody tr:nth-child(odd) {
    background-color: var(--nr-bg);
}

[data-testid="dataFrameContainer"] tbody tr:nth-child(even) {
    background-color: var(--nr-surface);
}

/* Metric cards */
[data-testid="stMetric"] {
    border: 1px solid var(--nr-border);
    border-radius: 6px;
    padding: 1rem;
    background-color: var(--nr-surface);
}

[data-testid="stMetric"] * {
    color: var(--nr-text) !important;
}

/* Map legend */
.nr-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.25rem;
    color: var(--nr-muted);
    font-size: 0.875rem;
}

.nr-legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.nr-legend-dot {
    width: 0.8rem;
    height: 0.8rem;
    border-radius: 50%;
    border: 1px solid var(--nr-border);
    flex-shrink: 0;
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
    background-color: var(--nr-bg);
    border: 1px solid var(--nr-border);
    border-radius: 6px;
    color: var(--nr-primary);
    font-weight: 500;
}

.map-loader-ring {
    width: 48px;
    height: 48px;
    border: 5px solid var(--nr-surface);
    border-top-color: var(--nr-primary);
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
    border: 5px solid var(--nr-surface);
    border-top-color: var(--nr-primary);
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
    color: var(--nr-primary);
    font-weight: 500;
    z-index: 0;
}

[class*="st-key-map_wrap_"] iframe {
    position: relative;
    z-index: 1;
}
"""


def inject_theme(theme: Theme) -> None:
    """Inject the stylesheet with the given theme's tokens as CSS variables."""
    st.markdown(
        f"<style>\n@import url('{theme.font_import}');\n"
        f":root {{\n{_css_variables(theme)}\n}}\n"
        f"{_STYLESHEET}</style>",
        unsafe_allow_html=True,
    )


def legend_item(color: str, label: str) -> str:
    """Return a coloured dot followed by a label, for use inside a .nr-legend."""
    return (
        f'<span class="nr-legend-item"><span class="nr-legend-dot" '
        f'style="background-color: {color};"></span>{html.escape(label)}</span>'
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
            background-color: var(--nr-sidebar-bg);
            color: var(--nr-sidebar-text);
            padding: 1.5rem 2rem;
            border: 3px solid var(--nr-sidebar-text) inset;
            border-radius: 6px;
            text-align: center;
            font-family: var(--nr-font-heading);
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
