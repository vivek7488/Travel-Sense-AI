from app.services.huggingface import analyze_sentiment, classify_traveler

FEATURE_KEYWORDS = {
    "wifi": ["wifi", "internet", "connection", "online", "signal", "bandwidth"],
    "noise": ["quiet", "noise", "loud", "peaceful", "silent", "noisy", "sound"],
    "pool": ["pool", "swimming", "swim", "splash", "jacuzzi"],
    "food": ["food", "breakfast", "restaurant", "meal", "dining", "eat", "menu", "buffet"],
    "cleanliness": ["clean", "dirty", "hygiene", "spotless", "tidy", "dust", "smell"],
    "location": ["location", "central", "nearby", "walking", "convenient", "close", "transport"],
    "value": ["value", "price", "worth", "affordable", "expensive", "cheap", "money"],
    "accessibility": ["wheelchair", "accessible", "elevator", "ramp", "disabled", "mobility", "lift"]
}

def extract_feature_scores(text):
    text_lower = text.lower()
    scores = {}
    for feature, keywords in FEATURE_KEYWORDS.items():
        mentioned = any(kw in text_lower for kw in keywords)
        if mentioned:
            sentences = [s for s in text.split(".") if any(kw in s.lower() for kw in keywords)]
            feature_text = " ".join(sentences[:3]) if sentences else text[:300]
            scores[feature] = analyze_sentiment(feature_text)
        else:
            scores[feature] = 5.0
    return scores

def process_text_review(text):
    feature_scores = extract_feature_scores(text)
    traveler_type = classify_traveler(text)
    return {
        "feature_scores": feature_scores,
        "traveler_type": traveler_type,
        "processed_text": text
    }
