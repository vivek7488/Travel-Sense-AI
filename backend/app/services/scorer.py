"""Persona scoring.

Each persona weights the eight features differently. If a feature has no data
for a property, its weight is dropped and the remaining weights are
renormalised, so a missing pool score does not silently count as "average".
A persona score is None when none of its features have data.
"""

PERSONA_WEIGHTS = {
    "family": {"pool": 0.30, "food": 0.25, "noise": 0.20, "cleanliness": 0.15, "value": 0.10},
    "business": {"wifi": 0.35, "location": 0.25, "noise": 0.20, "cleanliness": 0.20},
    "solo": {"value": 0.30, "location": 0.25, "noise": 0.25, "wifi": 0.20},
    "accessibility": {"accessibility": 0.40, "noise": 0.20, "cleanliness": 0.20, "location": 0.20},
}

FEATURE_LABELS = {
    "wifi": "WiFi", "noise": "Quietness", "pool": "Pool", "food": "Food",
    "cleanliness": "Cleanliness", "location": "Location", "value": "Value", "accessibility": "Accessibility",
}


def persona_score(feature_scores, weights):
    """Weighted mean over features that have a score; None if none do."""
    available = {f: w for f, w in weights.items() if feature_scores.get(f) is not None}
    if not available:
        return None
    total_w = sum(available.values())
    return round(min(sum(feature_scores[f] * w for f, w in available.items()) / total_w, 10.0), 2)


def persona_summary(feature_scores, weights):
    """Short factual summary built from the persona's top-weighted features with data."""
    parts = []
    for f, _ in sorted(weights.items(), key=lambda kv: -kv[1]):
        s = feature_scores.get(f)
        if s is None:
            continue
        parts.append(f"{FEATURE_LABELS[f]} {s:.1f}/10")
        if len(parts) == 3:
            break
    missing = [FEATURE_LABELS[f] for f in weights if feature_scores.get(f) is None]
    text = ", ".join(parts) if parts else "No reviews mention the features this traveler cares about yet."
    if parts and missing:
        text += f". No reviews mention: {', '.join(missing)}"
    return text


def calculate_persona_scores(feature_scores):
    """feature_scores: {feature: float|None}. Returns the persona_scores row."""
    out = {}
    for persona, weights in PERSONA_WEIGHTS.items():
        out[f"{persona}_score"] = persona_score(feature_scores, weights)
        out[f"{persona}_summary"] = persona_summary(feature_scores, weights)
    return out
