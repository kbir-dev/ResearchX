import React, { useState } from 'react';

const SearchInput = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter research topic..."
        className="w-full p-4 rounded-lg bg-gray-800 text-white border-2 border-green-400 focus:outline-none focus:ring-2 focus:ring-green-400"
      />
      <button
        type="submit"
        className="mt-4 w-full p-4 bg-green-400 text-gray-900 rounded-lg font-bold hover:bg-green-300 transition duration-300"
      >
        Search
      </button>
    </form>
  );
};

export default SearchInput;
