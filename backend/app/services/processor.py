"""Turn one review into per-feature sentiment scores.

Only features the review actually mentions get a score. Features that are not
mentioned are left out (not defaulted to 5.0), so that aggregation across
reviews can distinguish "no data" from "average".
"""
import re
from app.services import huggingface

FEATURE_KEYWORDS = {
    "wifi": ["wifi", "wi-fi", "internet", "connection", "online", "signal", "bandwidth"],
    "noise": ["quiet", "noise", "loud", "peaceful", "silent", "noisy", "sound"],
    "pool": ["pool", "swimming", "swim", "splash", "jacuzzi"],
    "food": ["food", "breakfast", "restaurant", "meal", "dining", "eat", "menu", "buffet"],
    "cleanliness": ["clean", "dirty", "hygiene", "spotless", "tidy", "dust", "smell"],
    "location": ["location", "central", "nearby", "walking", "convenient", "close", "transport"],
    "value": ["value", "price", "worth", "affordable", "expensive", "cheap", "money"],
    "accessibility": ["wheelchair", "accessible", "elevator", "ramp", "disabled", "mobility", "lift"],
}

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

# Whole-word matching: "great" must not trigger "eat", "uplifting" must not trigger "lift".
_FEATURE_PATTERNS = {
    feature: re.compile(r"\b(" + "|".join(re.escape(k) for k in kws) + r")\b", re.IGNORECASE)
    for feature, kws in FEATURE_KEYWORDS.items()
}


def _sentences_mentioning(text, feature):
    pattern = _FEATURE_PATTERNS[feature]
    return [s for s in _SENTENCE_SPLIT.split(text) if pattern.search(s)]


def extract_feature_scores(text, sentiment_fn=None):
    """Return {feature: score} for features mentioned in `text`.

    `sentiment_fn` can be injected for tests; it takes text and returns 0-10 or None.
    """
    sentiment_fn = sentiment_fn or huggingface.analyze_sentiment
    scores = {}
    for feature in FEATURE_KEYWORDS:
        sentences = _sentences_mentioning(text, feature)
        if not sentences:
            continue
        score = sentiment_fn(" ".join(sentences[:3]))
        if score is not None:
            scores[feature] = score
    return scores


def process_text_review(text, sentiment_fn=None, classify_fn=None):
    classify_fn = classify_fn or huggingface.classify_traveler
    return {
        "feature_scores": extract_feature_scores(text, sentiment_fn),
        "traveler_type": classify_fn(text),
    }
