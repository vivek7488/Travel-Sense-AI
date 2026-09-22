"""Run the feature extractor on stored reviews that have no feature_scores yet.

Run from backend/:  python scripts/reprocess_reviews.py
Calls the HuggingFace API once per mentioned feature per review, so it is slow
on large datasets; it resumes safely because processed reviews are skipped.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
from app.services import supabase_client as db
from app.services.processor import extract_feature_scores

if __name__ == "__main__":
    rows = db._get("reviews", {"select": "id,review_text,feature_scores", "feature_scores": "eq.{}"})
    print(f"{len(rows)} reviews to process")
    for i, row in enumerate(rows, 1):
        scores = extract_feature_scores(row["review_text"])
        r = httpx.patch(db.REST + "reviews", headers=db._headers("return=minimal"),
                        params={"id": "eq." + str(row["id"])}, json={"feature_scores": scores}, timeout=15)
        r.raise_for_status()
        print(f"[{i}/{len(rows)}] {row['id']}: {list(scores)}")
