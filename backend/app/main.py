from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import properties, reviews, search

app = FastAPI(
    title="TravelSense AI",
    description="Intelligent Travel Experience Analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(properties.router)
app.include_router(reviews.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "TravelSense AI is running", "status": "healthy", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "ai_pipeline": "ready"}