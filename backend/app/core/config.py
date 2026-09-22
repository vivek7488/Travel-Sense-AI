import os
from pathlib import Path
from dotenv import load_dotenv

# Load backend/.env relative to this file, so the project runs on any machine.
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
HF_API_KEY = os.getenv("HF_API_KEY", "")
APP_ENV = os.getenv("APP_ENV", "development")
APP_PORT = int(os.getenv("APP_PORT", "8001"))
# Comma-separated list of allowed frontend origins.
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",") if o.strip()]
