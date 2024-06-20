// src/App.js
import React, { useState } from 'react';

const App = () => {
  const [inputData, setInputData] = useState('');
  const [processedData, setProcessedData] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    setInputData(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}processdata`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_data: inputData }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setProcessedData(data.processed_data);
      setError(null);
    } catch (error) {
      setError('Error processing data');
      setProcessedData(null);
    }
  };

  return (
    <div>
      <h1>Data Processor( Just reversing the string for demonstration)</h1>
      <input
        type="text"
        value={inputData}
        onChange={handleInputChange}
        placeholder="Enter data to process"
      />
      <button onClick={handleSubmit}>Process Data</button>
      {processedData && <div>Processed Data: {processedData}</div>}
      {error && <div>{error}</div>}
    </div>
  );
};

export default App;
