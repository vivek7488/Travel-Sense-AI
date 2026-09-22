from fastapi import APIRouter, HTTPException
from app.services import supabase_client as db
from app.services.property_scores import recompute_property_scores

router = APIRouter()


@router.get("/api/properties")
def list_properties(city: str = None, country: str = None, price_range: str = None):
    props = db.get_all_properties(city, country, price_range)   # filtered in the database, not in Python
    return {"properties": props, "total": len(props)}


@router.get("/api/properties/{property_id}")
def get_property(property_id: str):
    prop = db.get_property_by_id(property_id)
    if not prop:
        raise HTTPException(404, "Property not found")
    return prop


@router.get("/api/properties/{property_id}/scores")
def get_scores(property_id: str):
    scores = db.get_persona_scores_by_property(property_id)
    if not scores:
        raise HTTPException(404, "Scores not found")
    return scores


@router.get("/api/properties/{property_id}/analysis")
def get_analysis(property_id: str):
    analysis = db.get_analysis_by_property(property_id)
    if not analysis:
        raise HTTPException(404, "Analysis not found")
    return analysis


@router.get("/api/properties/{property_id}/reviews")
def get_reviews(property_id: str):
    reviews = db.get_reviews_by_property(property_id)
    return {"reviews": reviews, "total": len(reviews)}


@router.post("/api/properties/{property_id}/recompute")
def recompute(property_id: str):
    """Rebuild this property's scores from all stored reviews (use after the migration)."""
    if not db.get_property_by_id(property_id):
        raise HTTPException(404, "Property not found")
    return recompute_property_scores(property_id)
