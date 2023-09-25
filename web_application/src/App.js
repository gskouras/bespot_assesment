import React, { useState } from 'react';
import Navbar from './components/Navbar.js';
import PlaceList from './components/Placelist';

function ParentComponent() {
  const [searchResults, setSearchResults] = useState([]);

  // Callback function to receive search results
  function handleSearchResults(results) {
    if (results.length > 0) {
      setSearchResults(results);
    }
    else {
      results[0] = "empty"
      setSearchResults(results);
    }
  }

  return (
    <div>
      <Navbar onSearchResults={handleSearchResults} />
      {}
      <PlaceList data={searchResults} />
    </div>
  );
}

export default ParentComponent;
