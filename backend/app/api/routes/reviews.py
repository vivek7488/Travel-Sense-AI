from fastapi import APIRouter, HTTPException
from app.models.schemas import ReviewUpload, TRAVELER_TYPES
from app.services.processor import process_text_review
from app.services import supabase_client as db
from app.services.property_scores import recompute_property_scores

router = APIRouter()


@router.post("/api/reviews/upload")
def upload_review(review: ReviewUpload):
    if review.traveler_type and review.traveler_type not in TRAVELER_TYPES:
        raise HTTPException(400, f"traveler_type must be one of {TRAVELER_TYPES}")
    if not db.get_property_by_id(review.property_id):
        raise HTTPException(404, "Property not found")

    result = process_text_review(review.review_text)
    traveler_type = review.traveler_type or result["traveler_type"]

    db.insert_review({
        "property_id": review.property_id,
        "review_text": review.review_text,
        "language": review.language,
        "source": review.source,
        "traveler_type": traveler_type,
        "feature_scores": result["feature_scores"],   # per-review scores, only mentioned features
    })
    updated = recompute_property_scores(review.property_id)
    return {
        "message": "Review processed",
        "traveler_type": traveler_type,
        "review_feature_scores": result["feature_scores"],
        "property_analysis": updated["analysis"],
        "property_persona_scores": updated["persona_scores"],
    }
