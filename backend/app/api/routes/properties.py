from fastapi import APIRouter, HTTPException
from app.services.supabase_client import get_all_properties, get_property_by_id, get_reviews_by_property, get_analysis_by_property, get_persona_scores_by_property

router = APIRouter()

@router.get("/api/properties")
async def list_properties(city: str = None, country: str = None, price_range: str = None):
    props = get_all_properties()
    if city:
        props = [p for p in props if p.get("city","").lower() == city.lower()]
    if country:
        props = [p for p in props if p.get("country","").lower() == country.lower()]
    if price_range:
        props = [p for p in props if p.get("price_range","").lower() == price_range.lower()]
    return {"properties": props, "total": len(props)}

@router.get("/api/properties/{property_id}")
async def get_property(property_id: str):
    prop = get_property_by_id(property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@router.get("/api/properties/{property_id}/scores")
async def get_scores(property_id: str):
    scores = get_persona_scores_by_property(property_id)
    if not scores:
        raise HTTPException(status_code=404, detail="Scores not found")
    return scores

@router.get("/api/properties/{property_id}/analysis")
async def get_analysis(property_id: str):
    analysis = get_analysis_by_property(property_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/api/properties/{property_id}/reviews")
async def get_reviews(property_id: str):
    reviews = get_reviews_by_property(property_id)
    return {"reviews": reviews, "total": len(reviews)}
