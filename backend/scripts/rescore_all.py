"""Recompute scores for every property from its stored reviews.

Run from backend/:  python scripts/rescore_all.py
Existing reviews that predate the migration have empty feature_scores and will
not contribute until re-processed with scripts/reprocess_reviews.py.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import supabase_client as db
from app.services.property_scores import recompute_property_scores

if __name__ == "__main__":
    props = db.get_all_properties()
    for i, p in enumerate(props, 1):
        res = recompute_property_scores(p["id"])
        print(f"[{i}/{len(props)}] {p.get('property_name')}: {res['analysis']['review_count']} reviews")
