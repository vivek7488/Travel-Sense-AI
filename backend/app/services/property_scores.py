"""Recompute a property's feature and persona scores from ALL of its reviews."""
from app.services import supabase_client as db
from app.services.aggregator import aggregate_reviews
from app.services.scorer import calculate_persona_scores


def recompute_property_scores(property_id):
    reviews = db.get_reviews_by_property(property_id)
    agg = aggregate_reviews([r.get("feature_scores") or {} for r in reviews])

    analysis_row = {f"{f}_score": s for f, s in agg["scores"].items()}
    analysis_row.update({f"{f}_count": c for f, c in agg["counts"].items()})
    analysis_row["review_count"] = agg["review_count"]
    db.upsert_analysis(property_id, analysis_row)

    persona = calculate_persona_scores(agg["scores"])
    db.upsert_persona_scores(property_id, persona)
    return {"analysis": analysis_row, "persona_scores": persona}
