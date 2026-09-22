"""Thin wrapper around the HuggingFace Inference API.

Only the two models the pipeline actually uses are listed here.
"""
import time
import httpx
from app.core.config import HF_API_KEY

HF_BASE = "https://api-inference.huggingface.co/models/"

MODELS = {
    "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "classification": "facebook/bart-large-mnli",
}


def call_model(task, payload, retries=3):
    url = HF_BASE + MODELS[task]
    headers = {"Authorization": "Bearer " + HF_API_KEY}
    for attempt in range(retries):
        try:
            r = httpx.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 503:  # model still loading
                time.sleep(5)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2)
    return {"error": "Model unavailable"}


def analyze_sentiment(text):
    """Return a 0-10 sentiment score for `text`, or None if the model failed."""
    result = call_model("sentiment", {"inputs": text[:512]})
    if not isinstance(result, list) or not result:
        return None
    scores = result[0] if isinstance(result[0], list) else result
    best = max(scores, key=lambda x: x.get("score", 0))
    label = best.get("label", "neutral").lower()
    score = best.get("score", 0.5)
    if "pos" in label:
        return round(score * 10, 2)
    if "neg" in label:
        return round((1 - score) * 10, 2)
    return 5.0


def classify_traveler(text):
    labels = ["family travel", "business travel", "solo travel", "accessibility needs"]
    result = call_model("classification", {"inputs": text[:512], "parameters": {"candidate_labels": labels}})
    if isinstance(result, dict) and "labels" in result:
        top = result["labels"][0]
        for key in ("family", "business", "accessibility"):
            if key in top:
                return key
        return "solo"
    return "solo"
