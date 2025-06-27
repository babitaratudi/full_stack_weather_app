from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

apiKey = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    city = data.get("city")

    # Input validation: city must contain only letters (no digits, no spaces)
    if not city:
        return jsonify({"error": "City name is required"}), 400

    if not re.match(r"^[A-Za-z]+$", city):
        return jsonify({"error": "City name must contain only letters (no digits or spaces)."}), 400

    else:
        print(f"Received city: {city}")
    try:
        # Fetch weather data
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}&units=metric', 
            timeout=60 # timeout in seconds
        )

        response.raise_for_status()
        forecast = response.json()["list"]

        daily_summary = {}
        for entry in forecast:
            date = entry["dt_txt"].split(" ")[0]
            temp_high = entry["main"]["temp_max"]
            temp_low = entry["main"]["temp_min"]
            weather = entry["weather"][0]["main"]

            if date not in daily_summary:
                daily_summary[date] = {
                    "high": temp_high,
                    "low": temp_low,
                    "conditions": set(),
                }
            else:
                daily_summary[date]["high"] = max(daily_summary[date]["high"], temp_high)
                daily_summary[date]["low"] = min(daily_summary[date]["low"], temp_low)

            print(f"Processing date: {date}, High: {temp_high}, Low: {temp_low}, Weather: {weather}")

            if "Rain" in weather:
                daily_summary[date]["conditions"].add("Rain is expected, Please carry Umbrella")
            if temp_high > 40:
                daily_summary[date]["conditions"].add("Temerature is more than 40, Use sunscreen lotion")
            if temp_low < 10:
                daily_summary[date]["conditions"].add("It's cold, wear warm clothes")
            # Add wind condition
            wind_speed = entry.get("wind", {}).get("speed", 0)
            if wind_speed > 10:
                daily_summary[date]["conditions"].add("It’s too windy, watch out!")
            # Add thunderstorm condition
            if "Thunderstorm" in weather:
                daily_summary[date]["conditions"].add("Don’t step out! A Storm is brewing!")

            print(f"Updated daily summary for {date}: {daily_summary[date]}")

        result = {
            date: {
                "high": daily_summary[date]["high"],
                "low": daily_summary[date]["low"],
                "conditions": list(daily_summary[date]["conditions"]),
            }
            for date in list(daily_summary.keys())[:3]
        }
        return jsonify(result)
    except requests.exceptions.Timeout:
        return jsonify({"error": "Weather service timed out. Please try again later."}), 504
    except requests.exceptions.RequestException:
        return jsonify({"error": f"No weather information found for \"{city}\". Please check the city name and try again with other city name."}), 500

if __name__ == '__main__':
    app.run(debug=True)