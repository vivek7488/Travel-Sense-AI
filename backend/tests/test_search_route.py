from app.api.routes.search import infer_traveler_type
from app.models.schemas import SearchRequest


def test_needs_override_traveler_type():
    assert infer_traveler_type(SearchRequest(query="hotel", traveler_type="solo", needs="wheelchair access")) == "accessibility"
    assert infer_traveler_type(SearchRequest(query="hotel", traveler_type="solo", needs="travelling with kids")) == "family"


def test_defaults_to_solo():
    assert infer_traveler_type(SearchRequest(query="hotel", traveler_type=None)) == "solo"
