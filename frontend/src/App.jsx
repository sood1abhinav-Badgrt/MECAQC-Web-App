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
      background: '#18161A',
      fontFamily: "'IBM Plex Sans', sans-serif",
    }}>
      <div style={{ padding: '32px 10%' }}>

      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        marginBottom: 24, 
        paddingBottom: 16, 
        borderBottom: '0.5px solid #332F35' 
      }}>
    <div>
        <h1 style={{ fontSize: 22, fontWeight: 500, color: '#F2EFF4', margin: 0, letterSpacing: '-0.01em' }}>
          MECAQC
        </h1>
        <p style={{ fontSize: 13, color: '#615D65', marginTop: 2 }}>
          Multi-pollutant Emissions Calculator · Holloway Group, UW–Madison
        </p>
      </div>
      <span style={{
        fontSize: 10,
        padding: '3px 10px',
        borderRadius: 999,
        background: '#14694E33',
        border: '0.5px solid #1D9E7555',
        color: '#1D9E75',
       }}>
      Wu et al. 2024
    </span>
  </div>
  <div style={{ 
    display: 'grid', 
    gridTemplateColumns: results ? '290px 1fr' : '1fr', 
    gap: 16, 
    alignItems: 'start',
  }}>
        <InputForm setResults={handleResults} />
        {results && <ResultsPanel results={results} plantMeta={plantMeta} />}
    </div>
      </div>
    </div>
  );
}