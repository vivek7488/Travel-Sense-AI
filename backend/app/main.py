from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.api.routes import properties, reviews, search
from app.services import supabase_client as db

app = FastAPI(title="TravelSense AI", description="Persona-weighted hotel scoring from reviews", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router)
app.include_router(reviews.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "TravelSense AI is running", "version": "1.1.0"}


@app.get("/health")
def health_check():
    try:
        ok = db.ping()
    except Exception:
        ok = False
    return {"status": "healthy" if ok else "degraded", "database": "connected" if ok else "unreachable"}
