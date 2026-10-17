import re
from dataclasses import fields

from src.next_restaurant.ui import DEFAULT_THEME, THEMES, Theme, _css_variables


def test_default_theme_exists():
    assert DEFAULT_THEME in THEMES


def test_theme_slugs_are_url_safe():
    for slug in THEMES:
        assert re.fullmatch(r"[a-z][a-z0-9-]*", slug)


def test_every_theme_field_is_set():
    for slug, theme in THEMES.items():
        for field in fields(Theme):
            value = getattr(theme, field.name)
            assert isinstance(value, str) and value.strip(), f"{slug}.{field.name} is empty"


def test_theme_labels_are_unique():
    labels = [theme.label for theme in THEMES.values()]
    assert len(labels) == len(set(labels))


def test_css_variables_cover_design_tokens():
    css = _css_variables(THEMES[DEFAULT_THEME])
    assert "--nr-primary: #17375E;" in css
    assert "--nr-font-heading:" in css
    assert "--nr-label" not in css
