import requests

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from app.config import OPENWEATHER_API_KEY


class WeatherInput(BaseModel):

    city: str = Field(
        min_length=1,
        max_length=100,
        description=(
            "Name of the city to get the current weather for."
        ),
    )


def get_weather(city: str) -> dict:

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

    except requests.Timeout:

        raise ValueError(
            "Weather service timed out. Please try again."
        )

    except requests.RequestException:

        raise ValueError(
            "Unable to connect to the weather service."
        )

    if response.status_code == 404:

        raise ValueError(
            f"City not found: {city}"
        )

    if response.status_code != 200:

        raise ValueError(
            "Weather service is currently unavailable."
        )

    try:

        data = response.json()

        return {
            "city": data["name"],
            "temperature_c": data["main"]["temp"],
            "feels_like_c": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
        }

    except (KeyError, TypeError, ValueError):

        raise ValueError(
            "Invalid response received from weather service."
        )


weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description=(
        "Get the current weather for a city. "
        "Use this tool when the user asks about current "
        "temperature, humidity, feels-like temperature, "
        "or weather conditions. "
        "The input must contain a city field."
    ),
    args_schema=WeatherInput,
)