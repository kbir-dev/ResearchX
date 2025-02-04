import React from 'react';

const DownloadOptions = () => {
  return (
    <div>
      <button className="mt-4 p-2 bg-blue-500 text-white rounded">Download CSV</button>
      <button className="mt-4 p-2 bg-blue-500 text-white rounded">Download DOCX</button>
    </div>
  );
};

export default DownloadOptions;
