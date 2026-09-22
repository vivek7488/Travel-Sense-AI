from fastapi import APIRouter
from app.models.schemas import SearchRequest
from app.services.search import search_properties

router = APIRouter()

NEED_KEYWORDS = {
    "accessibility": ["accessibility", "wheelchair"],
    "business": ["business", "work"],
    "family": ["family", "kids", "children"],
}


def infer_traveler_type(request: SearchRequest):
    if request.needs:
        needs = request.needs.lower()
        for persona, words in NEED_KEYWORDS.items():
            if any(w in needs for w in words):
                return persona
    return request.traveler_type or "solo"


@router.post("/api/search")
def search(request: SearchRequest):
    traveler_type = infer_traveler_type(request)
    results = search_properties(request.query, traveler_type)
    return {"query": request.query, "traveler_type": traveler_type, "results": results, "total": len(results)}
