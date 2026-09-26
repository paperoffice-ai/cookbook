#!/usr/bin/env python3
"""PaperOffice AI — Fetch weather data (FREE, costs no credits!)"""
import os
import sys
import json
import requests

API_URL = "https://api.paperoffice.ai/latest/weather"
API_KEY = os.environ.get("PAPEROFFICE_API_KEY", "")


def get_weather(lat: float, lon: float, lang: str = "de", token: str = API_KEY) -> dict:
    """Fetches current weather data, forecast, and air quality for coordinates."""
    if not token:
        raise ValueError("PAPEROFFICE_API_KEY not set")

    response = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={"lat": lat, "lon": lon, "lang": lang},
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    lat = float(sys.argv[1]) if len(sys.argv) > 1 else 52.52
    lon = float(sys.argv[2]) if len(sys.argv) > 2 else 13.41

    data = get_weather(lat, lon)
    current = data.get("current", {})
    condition = current.get("condition", {})

    print(f"Temperature: {current.get('temp_c')}°C")
    print(f"Condition:   {condition.get('text')}")
    print(f"Humidity:    {current.get('humidity')}%")
    print(f"Wind:        {current.get('wind_kph')} km/h")

    air = data.get("air_quality", {})
    if air:
        print(f"Air quality: {json.dumps(air, ensure_ascii=False)[:200]}")

    forecast = data.get("forecast", [])
    if forecast:
        print(f"\nForecast ({len(forecast)} days):")
        for day in forecast[:3]:
            print(f"  {day.get('date')}: {day.get('day', {}).get('condition', {}).get('text')} "
                  f"({day.get('day', {}).get('mintemp_c')}–{day.get('day', {}).get('maxtemp_c')}°C)")
