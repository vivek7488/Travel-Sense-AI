def calculate_persona_scores(feature_scores):
    wifi = feature_scores.get("wifi", 5.0)
    noise = feature_scores.get("noise", 5.0)
    pool = feature_scores.get("pool", 5.0)
    food = feature_scores.get("food", 5.0)
    cleanliness = feature_scores.get("cleanliness", 5.0)
    location = feature_scores.get("location", 5.0)
    value = feature_scores.get("value", 5.0)
    accessibility = feature_scores.get("accessibility", 5.0)

    family = round(pool*0.30 + food*0.25 + noise*0.20 + cleanliness*0.15 + value*0.10, 2)
    business = round(wifi*0.35 + location*0.25 + noise*0.20 + cleanliness*0.20, 2)
    solo = round(value*0.30 + location*0.25 + noise*0.25 + wifi*0.20, 2)
    access = round(accessibility*0.40 + noise*0.20 + cleanliness*0.20 + location*0.20, 2)

    return {
        "family_score": min(family, 10.0),
        "business_score": min(business, 10.0),
        "solo_score": min(solo, 10.0),
        "accessibility_score": min(access, 10.0),
        "family_summary": "Great for families with good pool and dining facilities.",
        "business_summary": "Suitable for business travelers with reliable wifi and location.",
        "solo_summary": "Good value for solo travelers with convenient location.",
        "accessibility_summary": "Moderate accessibility features available."
    }
