# app.py
import os
from flask import Flask, render_template, request
from geocode import geocode_single_city
from weather import get_weather_text
from events import get_events_text

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    city        = None
    country     = None
    weather_txt = None
    news_txt    = None

    if request.method == "POST":
        city    = request.form.get("city","").strip()
        country = request.form.get("country","").strip()

        # --- WEATHER ---
        if city:
            lat, lon, name = geocode_single_city(city)
            if lat is not None:
                weather_txt = get_weather_text(lat, lon, name)
            else:
                weather_txt = f"Could not find '{city}'."
        else:
            weather_txt = "Enter a city."

        # --- NEWS ---
        if country:  # you can repurpose the “country” form field as your keyword
            news_txt = get_events_text(country)
        else:
            news_txt = "Enter a country to search events."

    return render_template(
        "index.html",
        city=city or "",
        country=country or "",
        weather_info=weather_txt,
        news_info=news_txt
    )

if __name__ == "__main__":
    # Make sure you set NEWS_API_TOKEN in your environment!
    app.run(debug=True)
