"""Semantic search over properties, ranked by the requested persona's score."""
import httpx
from app.core.config import SUPABASE_URL
from app.services import supabase_client as db

_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # lazy: heavy import, only needed for search
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def search_properties(query, traveler_type="solo", limit=5, candidates=20):
    embedding = get_model().encode(query).tolist()
    r = httpx.post(
        SUPABASE_URL + "/rest/v1/rpc/match_properties",
        headers=db._headers(prefer=""),
        json={"query_embedding": embedding, "match_count": candidates},
        timeout=15,
    )
    r.raise_for_status()
    matches = r.json()
    if not isinstance(matches, list):
        return []

    ids = [str(m.get("property_id") or m.get("id")) for m in matches]
    props = db.get_properties_by_ids(ids)          # one query instead of N
    scores = db.get_persona_scores_by_ids(ids)      # one query instead of N

    results = []
    for pid in ids:
        prop, score_row = props.get(pid), scores.get(pid)
        if not prop or not score_row:
            continue
        results.append({
            "property": prop,
            "persona_score": score_row.get(traveler_type + "_score"),
            "summary": score_row.get(traveler_type + "_summary", ""),
            "family_score": score_row.get("family_score"),
            "business_score": score_row.get("business_score"),
            "solo_score": score_row.get("solo_score"),
            "accessibility_score": score_row.get("accessibility_score"),
        })
    # Properties with no data for this persona sort last rather than crashing the sort.
    results.sort(key=lambda x: (x["persona_score"] is None, -(x["persona_score"] or 0)))
    return results[:limit]
