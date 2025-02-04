import React, { useState } from 'react';
import SearchInput from '../components/SearchInput';
import LoadingState from '../components/LoadingState';
import ResultsDisplay from '../components/ResultsDisplay';
import DownloadOptions from '../components/DownloadOptions';

function App() {
  const [searchState, setSearchState] = useState('idle'); // idle, loading, results
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (query) => {
    setSearchState('loading');
    setError(null);
    setResults(null);

    try {
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

      // Fetch papers from backend
      const fetchResponse = await fetch(`${backendUrl}/fetch-papers/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, max_results: 10 }),
      });

      if (!fetchResponse.ok) {
        const fetchError = await fetchResponse.json();
        throw new Error(fetchError.detail || 'Failed to fetch papers.');
      }

      const fetchData = await fetchResponse.json();
      setResults(fetchData.papers);
      setSearchState('results');
    } catch (err) {
      console.error(err);
      setError(err.message);
      setSearchState('idle');
    }
  };

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-4xl font-bold mb-8 text-center">
        <span className="text-green-400">Research</span>X
      </h1>
      <SearchInput onSearch={handleSearch} />
      {searchState === 'loading' && <LoadingState />}
      {error && <p className="text-red-500 text-center">{error}</p>}
      {searchState === 'results' && (
        <>
          <ResultsDisplay results={results} />
          <DownloadOptions />
        </>
      )}
    </main>
  );
}

export default App;