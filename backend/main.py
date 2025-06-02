from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)
CORS(app)

apiKey = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City name is required"}), 400
    else:
        print(f"Received city: {city}")
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

            print(f"Processing date: {date}, High: {temp_high}, Low: {temp_low}, Weather: {weather}")

            if "Rain" in weather:
                daily_summary[date]["conditions"].add("Rain is expected, Please carry Umbrella")
            if temp_high > 40:
                daily_summary[date]["conditions"].add("Temerature is more than 40, Use sunscreen lotion")

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
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join('static', path)):
        return send_from_directory('static', path)
    else:
        return send_from_directory('static', 'index.html')
        
if __name__ == '__main__':
    app.run(debug=True)