import React from "react";

const SearchBar = ({ city, setCity, onSearch }) => (
  <div className="search-container">
    <input
      type="text"
      className="city-input"
      placeholder="Enter city name"
      value={city}
      onChange={(e) => setCity(e.target.value)}
    />
    <button className="search-button" onClick={onSearch}>
      Search
    </button>
  </div>
);

export default SearchBar;