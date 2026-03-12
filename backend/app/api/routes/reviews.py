from fastapi import APIRouter
from app.models.schemas import ReviewUpload
from app.services.processor import process_text_review
from app.services.scorer import calculate_persona_scores
from app.services.supabase_client import insert_review, update_analysis, update_persona_scores

router = APIRouter()

@router.post("/api/reviews/upload")
async def upload_review(review: ReviewUpload):
    result = process_text_review(review.review_text)
    feature_scores = result["feature_scores"]
    traveler_type = result["traveler_type"]
    if review.traveler_type:
        traveler_type = review.traveler_type
    insert_review({
        "property_id": review.property_id,
        "review_text": review.review_text,
        "language": review.language,
        "source": review.source,
        "traveler_type": traveler_type
    })
    update_analysis(review.property_id, {
        "wifi_score": feature_scores["wifi"],
        "noise_score": feature_scores["noise"],
        "pool_score": feature_scores["pool"],
        "accessibility_score": feature_scores["accessibility"],
        "food_score": feature_scores["food"],
        "cleanliness_score": feature_scores["cleanliness"],
        "location_score": feature_scores["location"],
        "value_score": feature_scores["value"]
    })
    persona_scores = calculate_persona_scores(feature_scores)
    update_persona_scores(review.property_id, persona_scores)
    return {
        "message": "Review uploaded and processed successfully",
        "traveler_type": traveler_type,
        "feature_scores": feature_scores,
        "persona_scores": persona_scores
    }
