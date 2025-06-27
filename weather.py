import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz


def get_weather_text(lat, lon, city_name=None):
    # Request 2 days of data
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto",
        "forecast_days": 2
    }
    response = requests.get(url, params=params)
    data = response.json()

    times = data["hourly"]["time"]
    temps = data["hourly"]["temperature_2m"]
    tz_name = data.get("timezone", "UTC")

    df = pd.DataFrame({"time": times, "temp": temps})
    # Convert to local timezone
    df["time"] = pd.to_datetime(df["time"]).dt.tz_localize("UTC").dt.tz_convert(tz_name)

    # Figure out now and now+24h in that local time zone
    try:
        local_tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        local_tz = pytz.UTC

    local_now = datetime.now(local_tz)
    local_24_later = local_now + timedelta(hours=24)

    # Keep only rows between now and now+24h
    df = df[(df["time"] >= local_now) & (df["time"] < local_24_later)]

    # Build the output
    today_str = local_now.strftime("%A, %B %d, %Y")
    location_str = city_name or f"{lat}, {lon}"

    lines = [f"Weather Forecast for {location_str}, {today_str}",
             "Time        Temperature (°C)",
             "--------------------------------"]

    if df.empty:
        lines.append("No data for the next 24 hours.")
    else:
        for _, row in df.iterrows():
            local_time_str = row["time"].strftime("%H:%M")
            temp_rounded = round(row["temp"])
            lines.append(f"{local_time_str:<12}{temp_rounded}")

    return "\n".join(lines)
