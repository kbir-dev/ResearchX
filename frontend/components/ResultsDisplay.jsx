import React from 'react';

const ResultsDisplay = ({ results }) => {
  return (
    <div>
      {results && results.length > 0 ? (
        results.map((paper, index) => (
          <div key={index} className="mb-4 p-4 border border-gray-700 rounded">
            <h3 className="text-lg font-bold">{paper.title}</h3>
            <p>{paper.authors}</p>
          </div>
        ))
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
};

export default ResultsDisplay;
