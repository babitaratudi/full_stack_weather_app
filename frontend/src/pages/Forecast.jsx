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
      <table className="weather-table">
        <thead>
          <tr>
            {Object.keys(weatherData).map((date) => (
              <th key={date}>{date}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {Object.keys(weatherData).map((date) => (
              <td key={date}>
                <p>High: {weatherData[date]?.high?.toFixed(2)}°C</p>
                <p>Low: {weatherData[date]?.low?.toFixed(2)}°C</p>
                <ul>
                  {weatherData[date]?.conditions?.map((condition, index) => (
                    <li key={index}>{condition}</li>
                  ))}
                </ul>
              </td>
            ))}
          </tr>
        </tbody>
      </table>
      <button className="back-button" onClick={() => navigate("/home")}>
        Back to Home
      </button>
    </div>
  );
};

export default Forecast;