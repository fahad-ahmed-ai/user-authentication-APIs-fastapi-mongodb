import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
APP_SECRET_KEY="thisismysecret"
SEND_GRID_API_KEY = os.getenv("SEND_GRID_API_KEY")
SEND_GRID_EMAIL = 'your-email'