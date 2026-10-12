import os

from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

MAX_AGENT_STEPS = 5


if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")


if not OPENWEATHER_API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY is not set in the .env file"
    )