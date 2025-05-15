from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

apiKey = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City name is required"}), 400

    try:
        # Fetch weather data
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apiKey}&units=metric'
        )
        if response.status_code == 404:
            # If city not found, fetch suggestions
            suggestion_response = requests.get(
                f'https://api.openweathermap.org/data/2.5/find?q={city}&appid={apiKey}&units=metric'
            )
            suggestions = suggestion_response.json().get("list", [])
            suggested_cities = [item["name"] for item in suggestions]
            return jsonify({
                "error": f"City '{city}' not found.",
                "suggestions": suggested_cities
            }), 404

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

            if "Rain" in weather:
                daily_summary[date]["conditions"].add("Carry umbrella")
            if temp_high > 40:
                daily_summary[date]["conditions"].add("Use sunscreen lotion")

        result = {
            date: {
                "high": daily_summary[date]["high"],
                "low": daily_summary[date]["low"],
                "conditions": list(daily_summary[date]["conditions"]),
            }
            for date in list(daily_summary.keys())[:3]
        }
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)