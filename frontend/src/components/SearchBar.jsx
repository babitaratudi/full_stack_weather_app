import React from 'react';

function SearchBar({ onSearch }) {
  return (
    <div>
      <input type="text" placeholder="Enter city" />
      <button onClick={onSearch}>Search</button>
    </div>
  );
}

export default SearchBar;
