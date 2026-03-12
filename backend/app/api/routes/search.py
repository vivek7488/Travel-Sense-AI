from fastapi import APIRouter
from app.models.schemas import SearchRequest
from app.services.search import search_properties

router = APIRouter()

@router.post("/api/search")
async def search(request: SearchRequest):
    traveler_type = request.traveler_type or "solo"
    if request.needs:
        needs = request.needs.lower()
        if "accessibility" in needs or "wheelchair" in needs:
            traveler_type = "accessibility"
        elif "business" in needs or "work" in needs:
            traveler_type = "business"
        elif "family" in needs or "kids" in needs or "children" in needs:
            traveler_type = "family"
    results = search_properties(request.query, traveler_type)
    return {
        "query": request.query,
        "traveler_type": traveler_type,
        "results": results,
        "total": len(results)
    }
