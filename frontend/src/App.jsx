import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Forecast from "./pages/Forecast";

const App = () => {
  const [weatherData, setWeatherData] = useState(null); // State to store weather data

  return (
    <Routes>
      {/* Home Page */}
      <Route path="/home" element={<Home setWeatherData={setWeatherData} />} />

      {/* Forecast Page */}
      <Route path="/forecast" element={<Forecast weatherData={weatherData} />} />

      {/* Redirect to /home by default */}
      <Route path="*" element={<Home setWeatherData={setWeatherData} />} />
    </Routes>
  );
};

export default App;