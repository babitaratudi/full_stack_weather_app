import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Home = ({ setWeatherData }) => {
  const [city, setCity] = useState("");
  const [error, setError] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const navigate = useNavigate();

  const fetchWeather = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error);
        setSuggestions(errorData.suggestions || []);
        return;
      }

      const data = await response.json();
      setWeatherData(data); // Pass data to parent state
      setError(null);
      setSuggestions([]);
      navigate("/forecast"); // Navigate to the forecast page
    } catch (err) {
      console.error(err);
      setError("An error occurred while fetching weather data.");
      setSuggestions([]);
    }
  };

  return (
    <div className="home-container">
      <h1 className="app-title">Weather App</h1>
      <div className="search-container">
        <input
          type="text"
          className="city-input"
          placeholder="Enter city name"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button className="search-button" onClick={fetchWeather}>
          Search
        </button>
      </div>
      {error && (
        <div className="error-container">
          <p className="error-text">{error}</p>
          {suggestions.length > 0 && (
            <div className="suggestions">
              <p>Did you mean:</p>
              <ul>
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    className="suggestion-item"
                    onClick={() => setCity(suggestion)}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;