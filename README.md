# 🌍 TravelSense AI

> **Personalized hotel scores based on WHO you are — not an average of everyone who ever stayed there.**

![TravelSense AI](https://img.shields.io/badge/TravelSense-AI-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-green?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green?style=for-the-badge)

---

## 🎯 The Problem

Every hotel review platform shows you a generic 4.2-star average. That number is calculated from families, business travelers, solo backpackers, and elderly travelers — all combined into one meaningless number.

**TravelSense AI solves this.** Same hotel. Same reviews. A completely different score based on who you are.

---

## ✨ Features

- 🔍 **Plain English Search** — Type naturally: *"quiet family hotel in Goa with pool under ₹10,000"*
- 🎯 **Persona-Based Scoring** — 4 traveler types, each with unique weighted scores
- 🌐 **Live Web Search Fallback** — If a hotel isn't in our database, AI searches the internet and analyzes it in real time
- 🧠 **AI Review Pipeline** — 8 AI models analyze every review (sentiment, NER, classification, summarization)
- 📊 **Radar Chart Dashboard** — 8 feature dimensions visualized per property
- 🗣️ **Multimodal Upload** — Submit reviews via text, voice, or photo
- 🌍 **195+ Properties** — Across 39 cities worldwide
- 🔐 **Auth** — Email, Google OAuth, Phone OTP via Supabase Auth

---

## 👥 The 4 Traveler Personas

| Persona | What They Care About | Score Weights |
|---------|---------------------|---------------|
| 👨‍👩‍👧 Family | Pool, Food, Safety, Kids | Pool×30% + Food×25% + Noise×20% + Clean×15% + Value×10% |
| 💼 Business | WiFi, Quiet, Location | WiFi×35% + Location×25% + Noise×20% + Clean×20% |
| ♿ Accessibility | Ramps, Elevators, Support | Access×40% + Noise×20% + Clean×20% + Location×20% |
| 🧳 Solo | Value, Vibe, Location | Value×30% + Location×25% + Noise×25% + WiFi×20% |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS + Framer Motion |
| Backend | FastAPI (Python) |
| Database | Supabase PostgreSQL + pgvector |
| AI Models | HuggingFace Inference API (8 models) |
| Semantic Search | sentence-transformers all-MiniLM-L6-v2 |
| Web Search | Tavily API |
| Auth | Supabase Auth |
| Deployment | Google Cloud Run + Firebase Hosting |

---

## 🤖 AI Pipeline

```
User Input (Text / Voice / Photo)
         │
         ▼
   Whisper (Speech → Text)
   BLIP (Image → Caption)
         │
         ▼
   mBART (Translation if non-English)
         │
         ▼
   BERT NER (Feature Extraction)
   RoBERTa (Sentiment per Feature)
         │
         ▼
   BART (Traveler Type Classification)
         │
         ▼
   Persona Score Calculator
   (Weighted formula per persona)
         │
         ▼
   PEGASUS (AI Summary Generation)
         │
         ▼
   Save to Supabase + Update Embeddings
```

---

## 📁 Project Structure

```
TravelSenseAI/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── api/routes/
│   │   │   ├── properties.py       # Property CRUD endpoints
│   │   │   ├── reviews.py          # Review upload endpoint
│   │   │   └── search.py           # Search with Tavily fallback
│   │   ├── core/
│   │   │   └── config.py           # Environment variables
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic models
│   │   └── services/
│   │       ├── huggingface.py      # HF API caller
│   │       ├── processor.py        # Feature extraction
│   │       ├── scorer.py           # Persona score calculator
│   │       ├── search.py           # Search engine + Tavily
│   │       ├── supabase_client.py  # Database helpers
│   │       └── web_search.py       # Tavily integration
│   └── .env                        # API keys (never commit)
│
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── Home.jsx            # 3D globe landing page
│       │   ├── SearchResults.jsx   # Results with persona scores
│       │   ├── PropertyDetail.jsx  # Radar chart + reviews
│       │   ├── Browse.jsx          # City browser
│       │   ├── Upload.jsx          # Submit review
│       │   └── Login.jsx           # Auth page
│       ├── components/
│       │   ├── Globe.jsx           # Canvas 3D rotating globe
│       │   └── PersonaQuestionnaire.jsx
│       ├── context/
│       │   └── AuthContext.jsx     # Supabase Auth
│       └── lib/
│           └── supabase.js         # Supabase JS client
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Supabase account
- HuggingFace API key (free)
- Tavily API key (free 1K/month)

### 1. Clone the repository

```bash
git clone https://github.com/vivek7488/Travel-Sense-AI.git
cd Travel-Sense-AI
```

### 2. Backend setup

```bash
cd backend

# Install dependencies
pip install fastapi uvicorn httpx python-dotenv sentence-transformers

# Create .env file
notepad .env
```

Add to `.env`:

```
APP_ENV=development
APP_PORT=8001
HF_API_KEY=your_huggingface_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
TAVILY_API_KEY=your_tavily_key
```

```bash
# Start backend
uvicorn app.main:app --reload --port 8001
```

### 3. Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:8001" > .env

# Start frontend
npm run dev
```

### 4. Open in browser

```
Frontend: http://localhost:5174
Backend API docs: http://localhost:8001/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/properties` | List all properties |
| `GET` | `/api/properties?city=Goa` | Filter by city |
| `GET` | `/api/properties/{id}` | Get single property |
| `GET` | `/api/properties/{id}/scores` | Get persona scores |
| `GET` | `/api/properties/{id}/analysis` | Get feature scores |
| `GET` | `/api/properties/{id}/reviews` | Get all reviews |
| `POST` | `/api/properties/add` | Add new property |
| `POST` | `/api/reviews/upload` | Submit a review |
| `POST` | `/api/search` | Search with persona |

### Search Request Example

```json
POST /api/search
{
  "query": "quiet family hotel in Goa with pool",
  "traveler_type": "family",
  "budget": "mid"
}
```

### Search Response Example

```json
{
  "query": "quiet family hotel in Goa with pool",
  "traveler_type": "family",
  "total": 5,
  "results": [
    {
      "property": {
        "property_name": "Taj Holiday Village Goa",
        "city": "Goa",
        "country": "India",
        "price_per_night_inr": 25000
      },
      "persona_score": 7.92,
      "family_score": 7.92,
      "business_score": 6.10,
      "solo_score": 7.06,
      "accessibility_score": 7.34,
      "summary": "Pool is great (7.45/10). Food is excellent (8.63/10)."
    }
  ]
}
```

---

## 🗄️ Database Schema

### properties
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| property_name | TEXT | Hotel name |
| city | TEXT | City for filtering |
| country | TEXT | Country |
| property_type | TEXT | hotel/resort/hostel/villa |
| price_range | TEXT | budget/mid/luxury |
| price_per_night_inr | INTEGER | Price in INR |

### analysis (scores 0–10)
| Column | Description |
|--------|-------------|
| wifi_score | WiFi quality (0–10) |
| noise_score | 10 = very quiet, 0 = very noisy |
| pool_score | Pool quality (0–10) |
| food_score | Food and dining (0–10) |
| cleanliness_score | Cleanliness (0–10) |
| location_score | Location convenience (0–10) |
| value_score | Value for money (0–10) |
| accessibility_score | Accessibility features (0–10) |

### persona_scores (scores 0–10)
| Column | Description |
|--------|-------------|
| family_score | Weighted score for families |
| business_score | Weighted score for business |
| solo_score | Weighted score for solo |
| accessibility_score | Weighted score for accessibility |
| family_summary | AI-written summary for families |
| business_summary | AI-written summary for business |
| solo_summary | AI-written summary for solo |
| accessibility_summary | AI-written summary for accessibility |

---

## 🌐 Search Intelligence

When a user searches for a hotel or city not in our database:

1. **City Detection** — Extracts city from natural language query
2. **Database Search** — Checks Supabase for existing properties
3. **Tavily Fallback** — If fewer than 3 results, searches the internet
4. **AI Processing** — Fetched reviews run through the full AI pipeline
5. **Auto-Save** — New property saved to database for future searches
6. **Return Results** — Personalized scores returned to user

---

## 🗺️ Cities Covered

**India:** Goa · Mumbai · Delhi · Jaipur · Manali · Bangalore · Chennai · Hyderabad · Kolkata · Kochi · Udaipur · Varanasi · Agra · Patna · Pune · Ooty · Rishikesh

**International:** Dubai · Bali · Bangkok · London · Paris · Tokyo · Singapore · Sydney · Amsterdam · Rome · Barcelona · Istanbul · Prague · Vienna · Kuala Lumpur · Hong Kong · Cape Town · Toronto · Santorini · Phuket · Maldives

---

## 🔒 Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_API_KEY` | HuggingFace Inference API key |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_ANON_KEY` | Supabase anonymous key |
| `SUPABASE_SERVICE_KEY` | Supabase service role key |
| `TAVILY_API_KEY` | Tavily search API key |

---

## 🙏 Acknowledgements

- [HuggingFace](https://huggingface.co) — AI model inference
- [Supabase](https://supabase.com) — Database and auth
- [Tavily](https://tavily.com) — Real-time web search
- [TripAdvisor Kaggle Dataset](https://www.kaggle.com) — Seed review data

---

## 👤 Author

**Vivek** — Creator of TravelSense AI

- GitHub: [@vivek7488](https://github.com/vivek7488)
- Project: [Travel-Sense-AI](https://github.com/vivek7488/Travel-Sense-AI)

---

<div align="center">
  <strong>🌍 TravelSense AI — Hotels scored for you, not everyone</strong>
</div>
