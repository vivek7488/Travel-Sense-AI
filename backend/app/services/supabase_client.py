"""Supabase (PostgREST) helpers. All calls run server-side with the service key."""
import httpx
from app.core.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

REST = SUPABASE_URL + "/rest/v1/"


def _headers(prefer="return=representation"):
    return {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
        "Prefer": prefer,
    }


def _get(table, params):
    r = httpx.get(REST + table, headers=_headers(), params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def _first(rows):
    return rows[0] if rows else None


def ping():
    """Cheap connectivity check used by /health."""
    r = httpx.get(REST + "properties", headers=_headers(), params={"select": "id", "limit": "1"}, timeout=5)
    return r.status_code == 200


def get_all_properties(city=None, country=None, price_range=None):
    params = {"select": "*"}
    if city:
        params["city"] = "ilike." + city
    if country:
        params["country"] = "ilike." + country
    if price_range:
        params["price_range"] = "ilike." + price_range
    return _get("properties", params)


def get_properties_by_ids(ids):
    if not ids:
        return {}
    rows = _get("properties", {"select": "*", "id": "in.(" + ",".join(ids) + ")"})
    return {row["id"]: row for row in rows}


def get_persona_scores_by_ids(ids):
    if not ids:
        return {}
    rows = _get("persona_scores", {"select": "*", "property_id": "in.(" + ",".join(ids) + ")"})
    return {row["property_id"]: row for row in rows}


def get_property_by_id(property_id):
    return _first(_get("properties", {"select": "*", "id": "eq." + property_id}))


def get_reviews_by_property(property_id):
    return _get("reviews", {"select": "*", "property_id": "eq." + property_id, "order": "created_at.desc"})


def get_analysis_by_property(property_id):
    return _first(_get("analysis", {"select": "*", "property_id": "eq." + property_id}))


def get_persona_scores_by_property(property_id):
    return _first(_get("persona_scores", {"select": "*", "property_id": "eq." + property_id}))


def insert_review(data):
    r = httpx.post(REST + "reviews", headers=_headers(), json=data, timeout=15)
    r.raise_for_status()
    return _first(r.json())


def _upsert(table, property_id, data):
    payload = dict(data, property_id=property_id)
    r = httpx.post(REST + table, headers=_headers("resolution=merge-duplicates,return=representation"),
                   json=payload, timeout=15)
    r.raise_for_status()
    return _first(r.json())


def upsert_analysis(property_id, data):
    return _upsert("analysis", property_id, data)


def upsert_persona_scores(property_id, data):
    return _upsert("persona_scores", property_id, data)
