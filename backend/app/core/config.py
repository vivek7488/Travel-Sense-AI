import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("D:/TravelSenseAI/backend/.env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
APP_ENV = os.getenv("APP_ENV","development")
APP_PORT = int(os.getenv("APP_PORT","8001"))
