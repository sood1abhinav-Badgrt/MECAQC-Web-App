import { useState } from 'react';
import InputForm from './InputForm';
import ResultsPanel from './ResultsPanel';

export default function App() {
  const [results, setResults] = useState(null);
  const [plantMeta, setPlantMeta] = useState(null);

  function handleResults(data, meta) {
    setResults(data);
    setPlantMeta(meta);
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: '#0A0C10',
      fontFamily: "'IBM Plex Sans', sans-serif",
    }}>
      <div style={{ maxWidth: 900, margin: '0 auto', padding: '40px 24px' }}>

        <div style={{ marginBottom: 32 }}>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: '#F9FAFB', margin: 0, letterSpacing: '-0.02em' }}>
            MECAQC
          </h1>
          <p style={{ fontSize: 13, color: '#6B7280', marginTop: 4 }}>
            Multi-pollutant Emissions Calculator for Air Quality and Climate
          </p>
        </div>

        <InputForm setResults={handleResults} />

        {results && <ResultsPanel results={results} plantMeta={plantMeta} />}
      </div>
    </div>
  );
}