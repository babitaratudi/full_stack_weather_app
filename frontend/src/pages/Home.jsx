import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import SearchBar from "../components/SearchBar";

const Home = ({ setWeatherData }) => {
  const [city, setCity] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const fetchWeather = async () => {
    try {
      const response = await fetch(`/api`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error);
        return;
      }

      const data = await response.json();
      setWeatherData(data);
      setError(null);
      navigate("/forecast");
    } catch (err) {
      console.error(err);
      setError("An error occurred while fetching weather data.");
    }
  };

  return (
    <div className="home-container">
      <h1 className="app-title">Weather App</h1>
      <SearchBar city={city} setCity={setCity} onSearch={fetchWeather}/>
      {error && (
        <div className="error-container">
          <p className="error-text">{error}</p>
        </div>
      )}
    </div>
  );
};

export default Home;