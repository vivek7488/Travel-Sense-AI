# TravelSense AI

**Hotel scores weighted for the kind of traveler you are, not a single average of everyone who ever stayed.**

A 4.2-star average blends families, business travelers, solo backpackers and travelers with accessibility needs into one number. TravelSense scores every hotel four ways from the same reviews, so a family sees a family score and a business traveler sees a business score.

## Status

**Backend: working. Frontend: not built yet.** This repo is an API plus a scoring engine. The `frontend/` folder is a Vite/React scaffold with a placeholder page. See [Roadmap](#roadmap) for what is planned.

## How it works

1. **Extract** — each review is split into sentences. For each of 8 features (WiFi, noise, pool, food, cleanliness, location, value, accessibility) the sentences that mention it are sent to a sentiment model, giving a 0–10 score for that feature *in that review*. Features the review doesn't mention get no score.
2. **Classify** — a zero-shot classifier tags the review's traveler type (used when the reviewer didn't say).
3. **Aggregate** — a property's feature score is the mean over reviews that mention that feature, with a count of how many did. No mentions → no score, shown as such.
4. **Persona score** — a weighted mean of the features each persona cares about. Missing features are dropped and the remaining weights renormalised, so "no reviews mention the pool" is not treated as "the pool is average".
5. **Search** — the query is embedded with `all-MiniLM-L6-v2`, the nearest properties are fetched via a pgvector RPC, and results are ranked by the requested persona's score.

| Persona | Weights |
|---|---|
| Family | Pool 30% · Food 25% · Noise 20% · Cleanliness 15% · Value 10% |
| Business | WiFi 35% · Location 25% · Noise 20% · Cleanliness 20% |
| Solo | Value 30% · Location 25% · Noise 25% · WiFi 20% |
| Accessibility | Accessibility 40% · Noise 20% · Cleanliness 20% · Location 20% |

The weights are hand-chosen from interviews with 12 travelers; they are a starting point, not a tuned model.

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.10+) |
| Database | Supabase Postgres + pgvector |
| Models | HuggingFace Inference API: `cardiffnlp/twitter-roberta-base-sentiment-latest` (sentiment), `facebook/bart-large-mnli` (zero-shot traveler type) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local) |
| Seed data | TripAdvisor hotel reviews dataset (Kaggle) |

## Getting started

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # fill in Supabase + HuggingFace keys
uvicorn app.main:app --reload --port 8001
# API docs: http://localhost:8001/docs
```

Database: run `backend/migrations/001_per_review_scores.sql` in the Supabase SQL editor, then for existing data run `python scripts/reprocess_reviews.py` (scores each stored review) and `python scripts/rescore_all.py` (rebuilds property scores). The `match_properties` pgvector function must exist; see `backend/migrations/README.md`.

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/properties?city=Goa&price_range=mid` | List properties (filtered in the DB) |
| `GET` | `/api/properties/{id}` | One property |
| `GET` | `/api/properties/{id}/analysis` | Feature scores + how many reviews mention each |
| `GET` | `/api/properties/{id}/scores` | Four persona scores + summaries |
| `GET` | `/api/properties/{id}/reviews` | Reviews |
| `POST` | `/api/properties/{id}/recompute` | Rebuild scores from all stored reviews |
| `POST` | `/api/reviews/upload` | Add a review; re-scores the property |
| `POST` | `/api/search` | `{query, traveler_type, needs?}` → ranked results |
| `GET` | `/health` | Checks the database is reachable |

Example search response item:

```json
{
  "property": {"property_name": "…", "city": "Goa", "price_per_night_inr": 25000},
  "persona_score": 7.92,
  "summary": "Pool 8.1/10, Food 7.4/10, Quietness 8.3/10. No reviews mention: Value",
  "family_score": 7.92, "business_score": 6.10, "solo_score": 7.06, "accessibility_score": null
}
```

## Tests and evaluation

```bash
cd backend
pytest                          # unit tests for extraction, aggregation and scoring (no network)
python scripts/evaluate.py eval/labels.csv   # accuracy against hand-labelled reviews (needs HF key)
```

`eval/labels.csv` is a small template. The evaluation reports traveler-type accuracy, feature-detection precision/recall, and per-feature sentiment accuracy. Add labelled rows there to track quality as the extractor changes.

## Known limitations

- Feature detection is keyword-based (whole-word). Reviews that discuss a feature without using a listed keyword are missed; the evaluation script measures how often.
- Sentiment is computed on up to three sentences per feature, so a long review with mixed opinions on the same feature is coarsely scored.
- Persona weights are fixed and untuned.
- The Supabase service key is used server-side for all queries; there is no end-user auth.

## Roadmap

- Minimal web UI: search box, persona picker, results with the four scores
- Web-search fallback for hotels not in the database
- Learn persona weights from labelled data instead of hand-setting them
- Multilingual reviews (translation step before extraction)

## Author

Vivek Kumar — [GitHub](https://github.com/vivek7488)
