"""Combine per-review feature scores into one score per feature for a property.

A property's score for a feature is the mean over reviews that mention that
feature. Features no review mentions have no score (None) and a count of 0.
"""
from app.models.schemas import FEATURES


def aggregate_reviews(review_feature_scores):
    """review_feature_scores: list of {feature: score} dicts, one per review.

    Returns {"scores": {feature: float|None}, "counts": {feature: int}, "review_count": int}.
    """
    totals = {f: 0.0 for f in FEATURES}
    counts = {f: 0 for f in FEATURES}
    for review in review_feature_scores:
        for feature, score in (review or {}).items():
            if feature in totals and score is not None:
                totals[feature] += float(score)
                counts[feature] += 1
    scores = {f: (round(totals[f] / counts[f], 2) if counts[f] else None) for f in FEATURES}
    return {"scores": scores, "counts": counts, "review_count": len(review_feature_scores)}
