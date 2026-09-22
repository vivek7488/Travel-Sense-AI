from pydantic import BaseModel, Field
from typing import Optional, Dict, List

TRAVELER_TYPES = ("family", "business", "solo", "accessibility")
FEATURES = ("wifi", "noise", "pool", "food", "cleanliness", "location", "value", "accessibility")


class ReviewUpload(BaseModel):
    property_id: str
    review_text: str = Field(min_length=10)
    traveler_type: Optional[str] = None
    language: Optional[str] = "en"
    source: Optional[str] = "user"


class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    traveler_type: Optional[str] = "solo"
    needs: Optional[str] = None
    budget: Optional[str] = None


class PersonaScores(BaseModel):
    family_score: Optional[float]
    business_score: Optional[float]
    solo_score: Optional[float]
    accessibility_score: Optional[float]
    family_summary: str
    business_summary: str
    solo_summary: str
    accessibility_summary: str
