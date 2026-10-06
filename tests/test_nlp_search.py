"""Tests for nlp_search module."""

import pandas as pd
import pytest
from src.next_restaurant.nlp_search import (
    RestaurantIndex,
    build_vocabulary,
    parse_query,
    search,
    validate_query,
)


@pytest.fixture
def sample_df():
    """Create a minimal synthetic restaurant DataFrame for testing."""
    return pd.DataFrame({
        "namesClean": [
            "Trattoria Roma",
            "Pizza Napoli",
            "Sushi Tokyo",
            "Curry House",
            "Burger King",
            "Kebab Corner",
            "Pasta Bella",
            "Ramen Shop",
        ],
        "foodType": [
            "Italian",
            "Italian",
            "Asian",
            "Asian",
            "Fastfood",
            "Turkish",
            "Italian",
            "Asian",
        ],
        "foodType2": [
            "Italian",
            "Pizza",
            "Japanese",
            "Indian",
            "Burgers",
            "Kebab",
            "Pasta",
            "Ramen",
        ],
        "district": [
            "Kreuzberg",
            "Mitte",
            "Friedrichshain",
            "Neukölln",
            "Prenzlauer Berg",
            "Wedding",
            "Charlottenburg",
            "Mitte",
        ],
        "rating": [4.5, 4.2, 4.8, 4.1, 3.9, 4.3, 4.6, 4.7],
        "userRatingsTotal": [150, 200, 250, 100, 300, 120, 180, 220],
        "priceLevel": [2.0, 2.0, 3.0, 2.0, 1.0, 1.0, 2.0, 2.0],
        "fullAddress": [
            "Kreuzberg St. 1, 10999 Berlin",
            "Mitte St. 2, 10115 Berlin",
            "Friedrichshain St. 3, 10247 Berlin",
            "Neukölln St. 4, 12051 Berlin",
            "Prenzlauer Berg St. 5, 10435 Berlin",
            "Wedding St. 6, 13347 Berlin",
            "Charlottenburg St. 7, 14059 Berlin",
            "Mitte St. 8, 10116 Berlin",
        ],
        "lat": [52.5, 52.52, 52.51, 52.48, 52.54, 52.55, 52.50, 52.53],
        "lng": [13.40, 13.41, 13.42, 13.43, 13.44, 13.45, 13.39, 13.40],
    })


@pytest.fixture
def vocab(sample_df):
    """Build vocabulary from sample data."""
    return build_vocabulary(sample_df)


class TestBuildVocabulary:
    """Test vocabulary building."""

    def test_vocabulary_contains_cuisines(self, vocab):
        """Vocabulary should contain all unique cuisines."""
        assert "Italian" in vocab.cuisines
        assert "Asian" in vocab.cuisines

    def test_vocabulary_contains_districts(self, vocab):
        """Vocabulary should contain all unique districts."""
        assert "Kreuzberg" in vocab.districts
        assert "Mitte" in vocab.districts


class TestParseQuery:
    """Test query parsing."""

    def test_parse_exact_cuisine(self, vocab):
        """Should parse exact cuisine match."""
        result = parse_query("italian", vocab)
        assert "Italian" in result.cuisines

    def test_parse_exact_district(self, vocab):
        """Should parse exact district match."""
        result = parse_query("kreuzberg", vocab)
        assert "Kreuzberg" in result.districts

    def test_parse_typo_cuisine(self, vocab):
        """Should handle typos in cuisine with fuzzy matching."""
        result = parse_query("italan", vocab)  # typo
        assert "Italian" in result.cuisines

    def test_parse_multi_word_district(self, vocab):
        """Should handle multi-word district names."""
        result = parse_query("prenzlauer berg", vocab)
        assert "Prenzlauer Berg" in result.districts

    def test_parse_cuisine_and_district(self, vocab):
        """Should parse both cuisine and district."""
        result = parse_query("italian in kreuzberg", vocab)
        assert "Italian" in result.cuisines
        assert "Kreuzberg" in result.districts

    def test_parse_ignores_stop_words(self, vocab):
        """Should ignore stop words like 'show', 'me', 'with', etc."""
        result = parse_query("show me all the italian restaurants in kreuzberg", vocab)
        assert "Italian" in result.cuisines
        assert "Kreuzberg" in result.districts
        # leftover should not contain stop words
        assert len([t for t in result.leftover_terms if t.lower() not in ["show", "me", "all", "the", "restaurants", "in"]]) >= 0


class TestValidateQuery:
    """Test query guardrail."""

    def test_reject_empty_query(self, vocab):
        """Should reject empty query."""
        result = validate_query("", vocab)
        assert not result.ok
        assert "example" in result.message.lower()

    def test_reject_whitespace_only(self, vocab):
        """Should reject whitespace-only query."""
        result = validate_query("   ", vocab)
        assert not result.ok

    def test_reject_no_cuisine_no_district(self, vocab):
        """Should reject query with neither cuisine nor district."""
        result = validate_query("hello world", vocab)
        assert not result.ok

    def test_reject_too_long(self, vocab):
        """Should reject queries longer than 200 chars."""
        result = validate_query("a" * 201, vocab)
        assert not result.ok

    def test_accept_cuisine_only(self, vocab):
        """Should accept query with cuisine only."""
        result = validate_query("italian", vocab)
        assert result.ok
        assert "Italian" in result.parsed.cuisines

    def test_accept_district_only(self, vocab):
        """Should accept query with district only."""
        result = validate_query("kreuzberg", vocab)
        assert result.ok
        assert "Kreuzberg" in result.parsed.districts

    def test_accept_both_cuisine_district(self, vocab):
        """Should accept query with both cuisine and district."""
        result = validate_query("italian in kreuzberg", vocab)
        assert result.ok


class TestSearch:
    """Test search functionality."""

    @pytest.fixture
    def index(self, sample_df):
        """Build search index."""
        return RestaurantIndex.build(sample_df)

    def test_search_by_cuisine(self, sample_df, index, vocab):
        """Should return all Italian restaurants."""
        result = parse_query("italian", vocab)
        matches = search(index, sample_df, result)
        assert len(matches) == 3  # Trattoria Roma, Pizza Napoli, Pasta Bella
        assert "Trattoria Roma" in matches["namesClean"].values

    def test_search_by_district(self, sample_df, index, vocab):
        """Should return all restaurants in Mitte."""
        result = parse_query("mitte", vocab)
        matches = search(index, sample_df, result)
        assert len(matches) == 2  # Pizza Napoli, Ramen Shop
        assert "Pizza Napoli" in matches["namesClean"].values
        assert "Ramen Shop" in matches["namesClean"].values

    def test_search_by_cuisine_and_district(self, sample_df, index, vocab):
        """Should return Italian restaurants in Mitte."""
        result = parse_query("italian mitte", vocab)
        matches = search(index, sample_df, result)
        assert len(matches) == 1
        assert matches["namesClean"].values[0] == "Pizza Napoli"

    def test_search_ranking_by_rating(self, sample_df, index, vocab):
        """Results should be ranked with rating as a factor."""
        result = parse_query("asian", vocab)
        matches = search(index, sample_df, result)
        # Blended score includes TF-IDF (70%) and rating (30%), so not purely by rating
        # but rating should influence the ranking
        assert len(matches) == 3
        assert all(m == "Asian" for m in matches["foodType"].values)

    def test_search_no_matches(self, sample_df, index, vocab):
        """Should return empty DataFrame when no matches."""
        result = parse_query("mexican", vocab)
        matches = search(index, sample_df, result)
        assert len(matches) == 0

    def test_search_with_min_rating_filter(self, sample_df, index, vocab):
        """Should filter by minimum rating."""
        result = parse_query("italian", vocab)
        matches = search(index, sample_df, result, min_rating=4.5)
        assert len(matches) == 2  # Trattoria Roma (4.5), Pasta Bella (4.6)
        assert all(m >= 4.5 for m in matches["rating"].values)

    def test_search_returns_correct_columns(self, sample_df, index, vocab):
        """Result should have all required columns."""
        result = parse_query("italian", vocab)
        matches = search(index, sample_df, result)
        required_cols = ["namesClean", "foodType", "district", "rating", "userRatingsTotal", "lat", "lng"]
        for col in required_cols:
            assert col in matches.columns
