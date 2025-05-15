import React from "react";

const WeatherTable = ({ weatherData }) => {
  if (!weatherData || Object.keys(weatherData).length === 0) {
    return <p>No weather data available. Please search for a city.</p>;
  }

  return (
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
              <p>High: {weatherData[date]?.high?.toFixed(2) || "N/A"}°C</p>
              <p>Low: {weatherData[date]?.low?.toFixed(2) || "N/A"}°C</p>
              <ul>
                {weatherData[date]?.conditions?.map((condition, index) => (
                  <li key={index}>{condition}</li>
                )) || <li>No conditions available</li>}
              </ul>
            </td>
          ))}
        </tr>
      </tbody>
    </table>
  );
};

export default WeatherTable;