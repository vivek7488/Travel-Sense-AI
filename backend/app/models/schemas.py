from pydantic import BaseModel
from typing import Optional, List

class ReviewUpload(BaseModel):
    property_id: str
    review_text: str
    traveler_type: Optional[str] = None
    language: Optional[str] = "en"
    source: Optional[str] = "user"

class FeatureScores(BaseModel):
    wifi_score: float
    noise_score: float
    pool_score: float
    accessibility_score: float
    food_score: float
    cleanliness_score: float
    location_score: float
    value_score: float

class PersonaScores(BaseModel):
    family_score: float
    business_score: float
    accessibility_score: float
    solo_score: float
    family_summary: Optional[str] = None
    business_summary: Optional[str] = None
    accessibility_summary: Optional[str] = None
    solo_summary: Optional[str] = None

class PropertyResponse(BaseModel):
    id: str
    property_name: str
    location: str
    city: str
    country: str
    property_type: str
    price_range: str
    price_per_night_inr: Optional[int] = None

class SearchRequest(BaseModel):
    query: str
    traveler_type: Optional[str] = "solo"
    needs: Optional[str] = None
    priority: Optional[str] = None
    budget: Optional[str] = None
