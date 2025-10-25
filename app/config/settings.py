from dotenv import load_dotenv
import os 

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
 
class Settings:
    GROQ_API_KEY: str = GROQ_API_KEY
    TAVILY_API_KEY: str = TAVILY_API_KEY

    ALLOWED_MODEL_NAMES=[
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
    ]
settings = Settings()