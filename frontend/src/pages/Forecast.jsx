import React from "react";
import { useNavigate } from "react-router-dom";
import WeatherTable from "../components/WeatherTable";
import '../App.css';

const Forecast = ({ weatherData }) => {
  const navigate = useNavigate();

  if (!weatherData) {
    return (
      <div className="forecast-container">
        <p>No weather data available. Please search for a city.</p>
        <button className="back-button" onClick={() => navigate("/home")}>
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="forecast-container">
      <h1 className="app-title">Weather Forecast</h1>
      <WeatherTable weatherData={weatherData} />
      <button className="back-button" onClick={() => navigate("/home")}>
        Back to Home
      </button>
    </div>
  );
};

export default Forecast;