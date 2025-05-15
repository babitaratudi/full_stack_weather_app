from flask import Flask, jsonify, request
from flask_caching import Cache
import os
import logging
from services.weather_service import fetch_weather_data  # New service layer

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key from environment variables
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
if not API_KEY:
    logger.error("OPENWEATHERMAP_API_KEY is not set in environment variables.")
    raise EnvironmentError("API key is required.")

@app.route('/api/weather', methods=['GET'])
@cache.cached(timeout=300)  # Cache responses for 5 minutes
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    # Validate input
    if not city.isalpha():
        return jsonify({'error': 'Invalid city name'}), 400

    try:
        # Fetch weather data using the service layer
        weather_data = fetch_weather_data(city, API_KEY)
        weather_data["_links"] = {
            "self": f"/api/weather?city={city}",
            "forecast": f"/api/forecast?city={city}"
        }
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        return jsonify({'error': 'Failed to fetch weather data'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'False') == 'True')
