"""
Natural-language search module for restaurants using TF-IDF and guardrails.

Provides query parsing, validation, and semantic search over restaurant data.
No Streamlit dependencies here for easy testing.
"""

import difflib
import re
import string
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Stop words to ignore in query parsing
STOP_WORDS = {
    "show",
    "me",
    "all",
    "the",
    "restaurants",
    "in",
    "with",
    "and",
    "or",
    "of",
    "to",
    "a",
    "an",
    "find",
    "get",
    "give",
    "display",
    "where",
    "what",
    "which",
    "who",
    "when",
    "berlin",  # Whole dataset is Berlin; it's not a location filter
    "rated",
    "top",
    "best",
    "highly",
    "reviews",
    "review",
    "stars",
    "star",
    "rating",
    "above",
    "over",
    "least",
    "minimum",
}

# Cuisine synonyms and variants
CUISINE_SYNONYMS = {
    "pasta": "Italian",
    "pizzeria": "Italian",
    "pizza": "Italian",
    "noodles": "Asian",
    "noodle": "Asian",
    "sushi": "Asian",
    "ramen": "Asian",
    "kebab": "Turkish",
    "kebaps": "Turkish",
    "gyro": "Turkish",
    "curry": "Asian",
    "indian": "Indian",
    "burger": "Fastfood",
    "burgers": "Fastfood",
    "fast food": "Fastfood",
    "fastfood": "Fastfood",
    "steak": "Steak",
    "steakhouse": "Steak",
    "asiatisch": "Asian",
    "italienisch": "Italian",
    "türkisch": "Turkish",
    "deutsch": "German",
    "französisch": "French",
}


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, remove accents, remove punctuation."""
    text = text.lower().strip()
    # Replace German umlauts
    text = text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    # NFD normalization and remove combining characters
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


@dataclass
class ParsedQuery:
    """Result of query parsing."""

    cuisines: Set[str]
    districts: Set[str]
    leftover_terms: List[str]
    query_text: str
    min_rating: Optional[float] = None
    min_reviews: Optional[int] = None


@dataclass
class GuardrailResult:
    """Result of query validation."""

    ok: bool
    message: str = ""
    parsed: Optional[ParsedQuery] = None


@dataclass
class Vocabulary:
    """Vocabulary of known cuisines and districts."""

    cuisines: Set[str]
    districts: Set[str]


def build_vocabulary(df: pd.DataFrame) -> Vocabulary:
    """Build vocabulary of cuisines and districts from dataframe."""
    cuisines = set()
    districts = set()

    # Collect from foodType and foodType2
    if "foodType" in df.columns:
        cuisines.update(df["foodType"].dropna().unique())
    if "foodType2" in df.columns:
        cuisines.update(df["foodType2"].dropna().unique())

    # Collect districts
    if "district" in df.columns:
        districts.update(
            d for d in df["district"].dropna().unique()
            if d and d != "All" and d != "Not Found"
        )

    return Vocabulary(cuisines=cuisines, districts=districts)


def parse_query(query: str, vocab: Vocabulary) -> ParsedQuery:
    """Parse query to extract cuisines, districts, and rating/review constraints."""
    if not query or not query.strip():
        return ParsedQuery(cuisines=set(), districts=set(), leftover_terms=[], query_text="")

    # Extract numeric constraints before normalization (which removes numbers)
    lower_query = query.lower()
    min_rating = None
    min_reviews = None

    # Keywords that map to 4.5 rating
    if any(kw in lower_query for kw in ["top rated", "best rated", "highly rated"]):
        min_rating = 4.5

    # Rating patterns: "rated 4.5", "above 4", "at least 4.5", "4 stars", etc.
    # Also handle commas: "4,5" means 4.5
    rating_patterns = [
        r"(?:rated|rating|above|over|at\s+least|min(?:imum)?|>=?)\s*([\d,]+(?:[\d,]*)?)",
        r"([\d,]+)\s*(?:\+\s*)?(?:stars?|rating)",
    ]
    for pattern in rating_patterns:
        match = re.search(pattern, lower_query, re.IGNORECASE)
        if match:
            try:
                val_str = match.group(1).replace(",", ".")  # Handle European format
                val = float(val_str)
                val = max(2.0, min(5.0, val))  # Clamp to slider range
                min_rating = val
                break
            except (ValueError, IndexError):
                pass

    # Review patterns: "100 reviews", "100+ reviews", "at least 50 reviews"
    review_patterns = [
        r"(?:at\s+least\s+|[\d,]+\s*\+?\s*)?(\d+)\s*(?:\+\s*)?(?:reviews?)",
    ]
    for pattern in review_patterns:
        match = re.search(pattern, lower_query, re.IGNORECASE)
        if match:
            try:
                val = int(match.group(1).replace(",", ""))
                val = max(0, min(2000, val))  # Clamp to slider range
                min_reviews = val
                break
            except (ValueError, IndexError):
                pass

    normalized = normalize_text(query)
    tokens = normalized.split()

    found_cuisines: Set[str] = set()
    found_districts: Set[str] = set()
    matched_indices: Set[int] = set()

    # Try to match multi-word terms first (districts like "prenzlauer berg")
    for i in range(len(tokens)):
        for length in range(min(3, len(tokens) - i), 0, -1):  # Try 3-word, 2-word, 1-word
            phrase = " ".join(tokens[i : i + length])

            # Check districts (multi-word capable)
            for district in vocab.districts:
                normalized_district = normalize_text(district)
                if phrase == normalized_district:
                    found_districts.add(district)
                    for j in range(i, i + length):
                        matched_indices.add(j)
                    break

            # Check cuisines
            for cuisine in vocab.cuisines:
                normalized_cuisine = normalize_text(cuisine)
                if phrase == normalized_cuisine:
                    found_cuisines.add(cuisine)
                    for j in range(i, i + length):
                        matched_indices.add(j)
                    break

    # Fuzzy matching for unmatched tokens (typos, synonyms)
    for i, token in enumerate(tokens):
        if i in matched_indices or token in STOP_WORDS:
            continue

        # Check synonyms
        if token in CUISINE_SYNONYMS:
            found_cuisines.add(CUISINE_SYNONYMS[token])
            matched_indices.add(i)
            continue

        # Fuzzy match cuisines (min 4 chars to avoid false positives)
        if len(token) >= 4:
            close_cuisines = difflib.get_close_matches(
                token, [normalize_text(c) for c in vocab.cuisines], n=1, cutoff=0.85
            )
            if close_cuisines:
                # Find original cuisine name
                for cuisine in vocab.cuisines:
                    if normalize_text(cuisine) == close_cuisines[0]:
                        found_cuisines.add(cuisine)
                        matched_indices.add(i)
                        break

            close_districts = difflib.get_close_matches(
                token, [normalize_text(d) for d in vocab.districts], n=1, cutoff=0.85
            )
            if close_districts:
                # Find original district name
                for district in vocab.districts:
                    if normalize_text(district) == close_districts[0]:
                        found_districts.add(district)
                        matched_indices.add(i)
                        break

    # Collect leftover terms
    leftover = [tokens[i] for i in range(len(tokens)) if i not in matched_indices and tokens[i] not in STOP_WORDS]

    return ParsedQuery(
        cuisines=found_cuisines,
        districts=found_districts,
        leftover_terms=leftover,
        query_text=query.strip(),
        min_rating=min_rating,
        min_reviews=min_reviews,
    )


def validate_query(query: str, vocab: Vocabulary) -> GuardrailResult:
    """Validate query against guardrail requirements."""
    if not query or not query.strip():
        return GuardrailResult(
            ok=False,
            message=(
                "Please enter a search query. Examples: 'italian restaurants', "
                "'top rated sushi in mitte', 'asian with 100+ reviews', 'kreuzberg above 4.5'"
            ),
        )

    if len(query) > 200:
        return GuardrailResult(
            ok=False,
            message="Query is too long (max 200 characters). Please be more concise.",
        )

    parsed = parse_query(query, vocab)

    # Guardrail: must have at least one cuisine OR one district
    if not parsed.cuisines and not parsed.districts:
        sample_cuisines = ", ".join(sorted(vocab.cuisines)[:5])
        sample_districts = ", ".join(sorted(vocab.districts)[:5])
        return GuardrailResult(
            ok=False,
            message=(
                f"Please include a cuisine or a district in your query.\n\n"
                f"**Example cuisines:** {sample_cuisines}, ...\n"
                f"**Example districts:** {sample_districts}, ...\n\n"
                f"Try: 'italian restaurants', 'top rated sushi in mitte', 'asian with 100+ reviews'"
            ),
        )

    return GuardrailResult(ok=True, message="", parsed=parsed)


@dataclass
class Selections:
    """Sidebar selections derived from a parsed query."""

    cuisine: Optional[str] = None
    district: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    notes: List[str] = field(default_factory=list)


def selections_from_query(
    parsed: ParsedQuery,
    cuisine_options: List[str],
    district_options: List[str],
) -> Selections:
    """Map parsed query to sidebar selections using first-match logic."""
    selections = Selections()

    # Normalize option lists for matching
    cuisine_map = {normalize_text(c): c for c in cuisine_options}
    district_map = {normalize_text(d): d for d in district_options if d != "All"}

    # Match cuisines (first one found in normalized order, alphabetically as tiebreaker)
    if parsed.cuisines:
        matched_cuisines = []
        for cuisine in sorted(parsed.cuisines):
            normalized = normalize_text(cuisine)
            if normalized in cuisine_map:
                matched_cuisines.append(cuisine)

        if matched_cuisines:
            selections.cuisine = cuisine_map[normalize_text(matched_cuisines[0])]
            if len(matched_cuisines) > 1:
                also_matched = ", ".join(matched_cuisines[1:])
                selections.notes.append(f"Applied {selections.cuisine}; also matched {also_matched}")
        else:
            selections.notes.append(
                f"'{', '.join(parsed.cuisines)}' is not a sidebar cuisine, so cuisine was left unchanged"
            )

    # Match districts (first one found, alphabetically as tiebreaker)
    if parsed.districts:
        matched_districts = []
        for district in sorted(parsed.districts):
            normalized = normalize_text(district)
            if normalized in district_map:
                matched_districts.append(district)

        if matched_districts:
            selections.district = district_map[normalize_text(matched_districts[0])]
            if len(matched_districts) > 1:
                also_matched = ", ".join(matched_districts[1:])
                selections.notes.append(f"Applied {selections.district}; also matched {also_matched}")
        else:
            selections.notes.append(
                f"'{', '.join(parsed.districts)}' is not a sidebar district, so district was left unchanged"
            )

    # Add rating/reviews if found
    if parsed.min_rating is not None:
        selections.rating = parsed.min_rating
    if parsed.min_reviews is not None:
        selections.reviews = parsed.min_reviews

    return selections


class RestaurantIndex:
    """TF-IDF search index over restaurants."""

    def __init__(self, vectorizer: TfidfVectorizer, vectors):
        self.vectorizer = vectorizer
        self.vectors = vectors

    @classmethod
    def build(cls, df: pd.DataFrame) -> "RestaurantIndex":
        """Build index from dataframe."""
        # Create document text per restaurant
        docs = []
        for _, row in df.iterrows():
            doc_parts = [
                str(row.get("namesClean", "")),
                str(row.get("foodType", "")),
                str(row.get("foodType2", "")),
                str(row.get("district", "")),
            ]
            # Normalize and concatenate
            doc = " ".join(normalize_text(part) for part in doc_parts if part)
            docs.append(doc)

        # Build TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            sublinear_tf=True,
            lowercase=True,
            stop_words=None,  # We handle stop words in query parsing
            max_features=None,
        )
        vectors = vectorizer.fit_transform(docs)

        return cls(vectorizer, vectors)

    def query_vector(self, query_text: str):
        """Transform query text to vector."""
        normalized = normalize_text(query_text)
        return self.vectorizer.transform([normalized])


def search(
    index: RestaurantIndex,
    df: pd.DataFrame,
    parsed: ParsedQuery,
    min_rating: float = 0.0,
    min_reviews: int = 0,
) -> pd.DataFrame:
    """Search restaurants matching the parsed query."""
    # If query was parsed but found no cuisines/districts, return empty
    if not parsed.cuisines and not parsed.districts:
        return df.iloc[0:0][["namesClean", "foodType", "district", "rating", "userRatingsTotal", "lat", "lng"]]

    # Start with all rows
    result_df = df.copy()

    # Hard filter by cuisine
    if parsed.cuisines:
        cuisine_filter = result_df["foodType"].isin(parsed.cuisines) | result_df["foodType2"].isin(
            parsed.cuisines
        )
        result_df = result_df[cuisine_filter]

    # Hard filter by district
    if parsed.districts:
        district_filter = result_df["district"].isin(parsed.districts)
        result_df = result_df[district_filter]

    # If no hard filters matched, return empty
    if len(result_df) == 0:
        return result_df[
            ["namesClean", "foodType", "district", "rating", "userRatingsTotal", "lat", "lng"]
        ]

    # Filter by min rating and reviews
    result_df = result_df[
        (result_df["rating"] >= min_rating) & (result_df["userRatingsTotal"] >= min_reviews)
    ]

    # Score by TF-IDF similarity + rating blend
    query_vec = index.query_vector(parsed.query_text)
    similarities = cosine_similarity(query_vec, index.vectors).flatten()

    # Only get scores for rows in result_df
    result_indices = result_df.index.tolist()
    scores = np.array([similarities[i] if i < len(similarities) else 0.0 for i in result_indices])

    # Blend: 70% TF-IDF similarity, 30% normalized rating
    normalized_rating = result_df["rating"].values / 5.0
    blended_score = 0.7 * scores + 0.3 * normalized_rating

    # Sort by blended score
    result_df = result_df.copy()
    result_df["_score"] = blended_score
    result_df = result_df.sort_values("_score", ascending=False)
    result_df = result_df.drop(columns=["_score"])

    # Return only required columns
    return result_df[["namesClean", "foodType", "district", "rating", "userRatingsTotal", "lat", "lng"]]
