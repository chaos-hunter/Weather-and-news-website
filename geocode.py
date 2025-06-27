# geocode.py
import requests

def geocode_single_city(city_name):
    """
    Returns a single best-match location for city_name by requesting only 1 result.
    If found, returns (lat, lon, resolved_name).
    Otherwise, returns (None, None, None).
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1
    }
    response = requests.get(url, params=params)
    if not response.ok:
        print(f"Geocoding request error: HTTP {response.status_code}")
        return None, None, None

    data = response.json()
    results = data.get("results", [])
    if not results:
        print(f"No geocoding results for '{city_name}'.")
        return None, None, None

    best_match = results[0]
    lat = best_match["latitude"]
    lon = best_match["longitude"]
    resolved_name = best_match["name"]
    return lat, lon, resolved_name
