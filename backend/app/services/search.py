import httpx
from sentence_transformers import SentenceTransformer
from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_headers():
    return {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json"
    }

def get_persona_weights(traveler_type):
    weights = {
        "family": {"pool": 0.30, "food": 0.25, "noise": 0.20, "cleanliness": 0.15, "value": 0.10},
        "business": {"wifi": 0.35, "location": 0.25, "noise": 0.20, "cleanliness": 0.20},
        "accessibility": {"accessibility": 0.40, "noise": 0.20, "cleanliness": 0.20, "location": 0.20},
        "solo": {"value": 0.30, "location": 0.25, "noise": 0.25, "wifi": 0.20}
    }
    return weights.get(traveler_type, weights["solo"])

def search_properties(query, traveler_type="solo", limit=5):
    embedding = model.encode(query).tolist()
    headers = get_headers()
    headers["Prefer"] = ""
    r = httpx.post(
        SUPABASE_URL + "/rest/v1/rpc/match_properties",
        headers=headers,
        json={"query_embedding": embedding, "match_count": 20}
    )
    matches = r.json()
    if not isinstance(matches, list):
        return []
    results = []
    for match in matches[:limit]:
        pid = match.get("property_id") or match.get("id")
        scores_r = httpx.get(
            SUPABASE_URL + "/rest/v1/persona_scores?property_id=eq." + str(pid) + "&select=*",
            headers=get_headers()
        )
        prop_r = httpx.get(
            SUPABASE_URL + "/rest/v1/properties?id=eq." + str(pid) + "&select=*",
            headers=get_headers()
        )
        scores = scores_r.json()
        prop = prop_r.json()
        if scores and prop:
            score_data = scores[0]
            prop_data = prop[0]
            persona_score = score_data.get(traveler_type + "_score", 5.0)
            results.append({
                "property": prop_data,
                "persona_score": persona_score,
                "summary": score_data.get(traveler_type + "_summary", ""),
                "family_score": score_data.get("family_score", 0),
                "business_score": score_data.get("business_score", 0),
                "solo_score": score_data.get("solo_score", 0),
                "accessibility_score": score_data.get("accessibility_score", 0)
            })
    results.sort(key=lambda x: x["persona_score"], reverse=True)
    return results
