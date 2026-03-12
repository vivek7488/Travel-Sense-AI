import httpx
from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

def get_headers():
    return {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def get_all_properties():
    r = httpx.get(SUPABASE_URL + "/rest/v1/properties?select=*", headers=get_headers())
    return r.json()

def get_property_by_id(property_id):
    r = httpx.get(SUPABASE_URL + "/rest/v1/properties?id=eq." + property_id + "&select=*", headers=get_headers())
    result = r.json()
    return result[0] if result else None

def get_reviews_by_property(property_id):
    r = httpx.get(SUPABASE_URL + "/rest/v1/reviews?property_id=eq." + property_id + "&select=*", headers=get_headers())
    return r.json()

def get_analysis_by_property(property_id):
    r = httpx.get(SUPABASE_URL + "/rest/v1/analysis?property_id=eq." + property_id + "&select=*", headers=get_headers())
    result = r.json()
    return result[0] if result else None

def get_persona_scores_by_property(property_id):
    r = httpx.get(SUPABASE_URL + "/rest/v1/persona_scores?property_id=eq." + property_id + "&select=*", headers=get_headers())
    result = r.json()
    return result[0] if result else None

def insert_review(data):
    r = httpx.post(SUPABASE_URL + "/rest/v1/reviews", headers=get_headers(), json=data)
    return r.json()

def update_analysis(property_id, scores):
    existing = get_analysis_by_property(property_id)
    if existing:
        r = httpx.patch(SUPABASE_URL + "/rest/v1/analysis?property_id=eq." + property_id, headers=get_headers(), json=scores)
    else:
        scores["property_id"] = property_id
        r = httpx.post(SUPABASE_URL + "/rest/v1/analysis", headers=get_headers(), json=scores)
    return r.json()

def update_persona_scores(property_id, scores):
    existing = get_persona_scores_by_property(property_id)
    if existing:
        r = httpx.patch(SUPABASE_URL + "/rest/v1/persona_scores?property_id=eq." + property_id, headers=get_headers(), json=scores)
    else:
        scores["property_id"] = property_id
        r = httpx.post(SUPABASE_URL + "/rest/v1/persona_scores", headers=get_headers(), json=scores)
    return r.json()
