from app.services.aggregator import aggregate_reviews
from app.services.scorer import calculate_persona_scores, persona_score, PERSONA_WEIGHTS
from app.services.processor import extract_feature_scores


def test_aggregate_averages_only_reviews_that_mention_feature():
    agg = aggregate_reviews([{"pool": 9.0, "food": 8.0}, {"pool": 7.0}, {"wifi": 3.0}])
    assert agg["scores"]["pool"] == 8.0
    assert agg["scores"]["food"] == 8.0
    assert agg["scores"]["wifi"] == 3.0
    assert agg["scores"]["noise"] is None
    assert agg["counts"] == {"wifi": 1, "noise": 0, "pool": 2, "food": 1, "cleanliness": 0,
                             "location": 0, "value": 0, "accessibility": 0}
    assert agg["review_count"] == 3


def test_one_bad_review_no_longer_overwrites_many_good_ones():
    good = [{"pool": 9.0}] * 10
    bad = [{"pool": 1.0}]
    assert aggregate_reviews(good + bad)["scores"]["pool"] > 8.0


def test_missing_features_renormalise_instead_of_defaulting_to_five():
    # Only food known for a family: score should equal the food score, not be dragged to 5.
    assert persona_score({"food": 9.0}, PERSONA_WEIGHTS["family"]) == 9.0


def test_persona_score_none_when_no_data():
    assert persona_score({}, PERSONA_WEIGHTS["business"]) is None


def test_full_family_score_matches_weights():
    fs = {"pool": 8, "food": 6, "noise": 10, "cleanliness": 4, "value": 2}
    expected = round(8 * .30 + 6 * .25 + 10 * .20 + 4 * .15 + 2 * .10, 2)
    assert persona_score(fs, PERSONA_WEIGHTS["family"]) == expected


def test_summaries_reflect_data_and_missing_features():
    out = calculate_persona_scores({"pool": 8.1, "food": 7.4, "noise": None, "cleanliness": None,
                                    "value": None, "wifi": None, "location": None, "accessibility": None})
    assert "Pool 8.1/10" in out["family_summary"]
    assert "No reviews mention" in out["family_summary"]
    assert out["business_score"] is None
    assert "No reviews mention the features" in out["business_summary"]


def test_extractor_scores_only_mentioned_features():
    seen = []

    def fake_sentiment(text):
        seen.append(text)
        return 9.0 if "great" in text.lower() else 2.0

    text = "The pool was great. Wifi was awful and kept dropping. Nice place."
    scores = extract_feature_scores(text, sentiment_fn=fake_sentiment)
    assert scores == {"pool": 9.0, "wifi": 2.0}
    assert "food" not in scores
    assert len(seen) == 2  # one model call per mentioned feature


def test_extractor_drops_feature_when_model_fails():
    scores = extract_feature_scores("The pool was great.", sentiment_fn=lambda t: None)
    assert scores == {}


def test_keyword_matching_is_whole_word():
    scores = extract_feature_scores("Everything was great and the view was uplifting.", sentiment_fn=lambda t: 9.0)
    assert scores == {}  # "great" != "eat", "uplifting" != "lift"
