"""Measure how well the pipeline agrees with human labels.

Usage (from backend/):  python scripts/evaluate.py eval/labels.csv

The CSV needs columns:
  review_text, traveler_type, <feature>_label ...
where traveler_type is one of family/business/solo/accessibility and each
<feature>_label is: pos, neg, or blank (feature not mentioned) for
wifi, noise, pool, food, cleanliness, location, value, accessibility.

Reports:
  - traveler-type classification accuracy
  - feature detection precision/recall (did we detect the feature at all?)
  - feature sentiment accuracy (pos if score >= 6, neg if score <= 4)
Calls the HuggingFace API, so it needs HF_API_KEY in .env.
"""
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.schemas import FEATURES
from app.services.processor import process_text_review


def main(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    if not rows:
        sys.exit("no rows")
    type_hits = 0
    det_tp = det_fp = det_fn = 0
    sent_hits = sent_total = 0

    for row in rows:
        out = process_text_review(row["review_text"])
        type_hits += out["traveler_type"] == row["traveler_type"].strip().lower()
        for f in FEATURES:
            label = (row.get(f"{f}_label") or "").strip().lower()
            predicted = f in out["feature_scores"]
            if predicted and label:
                det_tp += 1
                score = out["feature_scores"][f]
                pred_sent = "pos" if score >= 6 else "neg" if score <= 4 else "neutral"
                sent_total += 1
                sent_hits += pred_sent == label
            elif predicted and not label:
                det_fp += 1
            elif not predicted and label:
                det_fn += 1

    n = len(rows)
    prec = det_tp / (det_tp + det_fp) if det_tp + det_fp else 0
    rec = det_tp / (det_tp + det_fn) if det_tp + det_fn else 0
    print(f"Reviews evaluated:              {n}")
    print(f"Traveler-type accuracy:         {type_hits / n:.0%}")
    print(f"Feature detection precision:    {prec:.0%}  recall: {rec:.0%}")
    print(f"Feature sentiment accuracy:     {sent_hits / sent_total:.0%} ({sent_total} labelled mentions)" if sent_total else "no labelled mentions")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "eval/labels.csv")
