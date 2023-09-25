import React, { useState } from 'react';
import axios from 'axios';
import '../App.css';

function Navbar({ onSearchResults }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  // Function to handle search and make API call
  function handleSearch() {
    // Make an API call to 'api/v1/list' with the search query
    axios
      .get(`http://localhost:8000/api/v1/place?search=${searchQuery}`)
      .then((response) => {
        onSearchResults(response.data);
      })
      .catch((error) => {
        console.error('Error fetching search results:', error);
      });
  }

  // Function to handle Enter key press
  function handleEnterKeyPress(event) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }

  // Function to render search results
  function renderSearchResults() {
    if (searchResults.length === 0) {
      return null; // No results to display
    }

    return (
      <div className="search-results">
        {searchResults.map((result) => (
          <div key={result.id} className="search-result-item">
            {result.name} - {result.address}
          </div>
        ))}
      </div>
    );
  }

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h3>bespot.</h3>
      </div>
      <div className="navbar-center">
        {/* Add the search bar input */}
        <input
          type="text"
          placeholder="Search..."
          className="search-bar"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleEnterKeyPress}
        />
      </div>
      <div className="navbar-right">
        <ul className="nav-links">
          <li>Home</li>
          <li>About</li>
          <li>Contact</li>
        </ul>
        {renderSearchResults()}
      </div>
    </nav>
  );
}

export default Navbar;
