import httpx
import time
from app.core.config import HF_API_KEY

HF_BASE = "https://api-inference.huggingface.co/models/"

MODELS = {
    "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "ner": "dslim/bert-base-NER",
    "summarization": "google/pegasus-xsum",
    "classification": "facebook/bart-large-mnli",
    "translation": "facebook/mbart-large-50-many-to-many-mmt",
    "image_caption": "Salesforce/blip-image-captioning-base",
    "speech": "openai/whisper-base"
}

def call_model(task, payload, retries=3):
    url = HF_BASE + MODELS[task]
    headers = {"Authorization": "Bearer " + HF_API_KEY}
    for attempt in range(retries):
        try:
            r = httpx.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 503:
                time.sleep(5)
                continue
            return r.json()
        except Exception as e:
            if attempt == retries - 1:
                return {"error": str(e)}
            time.sleep(2)
    return {"error": "Model unavailable"}

def analyze_sentiment(text):
    result = call_model("sentiment", {"inputs": text[:512]})
    if isinstance(result, list) and len(result) > 0:
        scores = result[0] if isinstance(result[0], list) else result
        best = max(scores, key=lambda x: x.get("score", 0))
        label = best.get("label", "neutral").lower()
        score = best.get("score", 0.5)
        if "pos" in label:
            return round(score * 10, 2)
        elif "neg" in label:
            return round((1 - score) * 10, 2)
        return 5.0
    return 5.0

def classify_traveler(text):
    labels = ["family travel", "business travel", "solo travel", "accessibility needs"]
    result = call_model("classification", {"inputs": text[:512], "parameters": {"candidate_labels": labels}})
    if "labels" in result:
        top = result["labels"][0]
        if "family" in top: return "family"
        if "business" in top: return "business"
        if "accessibility" in top: return "accessibility"
        return "solo"
    return "solo"

def summarize_text(text):
    result = call_model("summarization", {"inputs": text[:1024]})
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("summary_text", text[:200])
    return text[:200]
