# Loads environment variables (e.g., Redis host, Groq API key).
# Can support .env parsing with python-dotenv.

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "test123")  # default fallback for dev
