import { useState } from 'react';

const FIELDS = [
  { name: 'state',           label: 'State',              hint: 'Two-letter code',      placeholder: 'e.g. IN',         half: true  },
  { name: 'capacity',        label: 'Nameplate capacity', hint: 'MW',                   placeholder: 'e.g. 403',        half: true  },
  { name: 'heatInput',       label: 'Annual heat input',  hint: 'MMBtu/yr — from CAMPD',placeholder: 'e.g. 1598916',   half: true  },
  { name: 'annualGeneration',label: 'Annual generation',  hint: 'MWh/yr — from CAMPD',  placeholder: 'e.g. 166714',    half: true  },
  { name: 'baselineSO2',     label: 'Baseline SO₂',       hint: 'short tons/yr',        placeholder: 'e.g. 953',        half: true  },
  { name: 'baselineNOx',     label: 'Baseline NOₓ',       hint: 'short tons/yr',        placeholder: 'e.g. 227',        half: true  },
  { name: 'baselinePM25',    label: 'Baseline PM₂.₅',     hint: 'short tons/yr',        placeholder: 'e.g. 71.6',       half: true  },
  { name: 'baselineVOC',     label: 'Baseline VOC',       hint: 'short tons/yr',        placeholder: 'e.g. 4.1',        half: true  },
  { name: 'baselineCO2',     label: 'Baseline CO₂',       hint: 'short tons/yr',        placeholder: 'e.g. 164046',     half: false },
];

const styles = {
  card: {
    background: '#111827',
    border: '1px solid #1F2937',
    borderRadius: 16,
    padding: '28px 32px',
  },
  sectionLabel: {
    fontSize: 11,
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
    color: '#6B7280',
    marginBottom: 4,
  },
  heading: {
    fontSize: 16,
    fontWeight: 600,
    color: '#F9FAFB',
    margin: '0 0 24px 0',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '16px 20px',
  },
  fieldGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: 5,
  },
  label: {
    fontSize: 12,
    color: '#9CA3AF',
    fontWeight: 500,
  },
  input: {
    background: '#0F1117',
    border: '1px solid #374151',
    borderRadius: 8,
    padding: '9px 12px',
    fontSize: 13,
    color: '#F9FAFB',
    outline: 'none',
    transition: 'border-color 0.15s',
    width: '100%',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
  },
  hint: {
    fontSize: 11,
    color: '#4B5563',
  },
  footer: {
    marginTop: 24,
    display: 'flex',
    alignItems: 'center',
    gap: 16,
  },
  submitBtn: {
    padding: '10px 24px',
    fontSize: 13,
    fontWeight: 600,
    background: '#10B981',
    color: '#022c22',
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    letterSpacing: '0.02em',
    transition: 'opacity 0.15s',
  },
  resetBtn: {
    fontSize: 12,
    color: '#6B7280',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    textDecoration: 'underline',
    fontFamily: 'inherit',
  },
  error: {
    fontSize: 12,
    color: '#EF4444',
    marginTop: 8,
  },
};

export default function InputForm({ setResults }) {
  const [formData, setFormData] = useState({
    state: '', capacity: '', annualGeneration: '', heatInput: '',
    baselineSO2: '', baselineNOx: '', baselinePM25: '', baselineVOC: '', baselineCO2: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [focusedField, setFocusedField] = useState(null);

  function handleChange(e) {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  }

  function handleReset() {
    setFormData({
      state: '', capacity: '', annualGeneration: '', heatInput: '',
      baselineSO2: '', baselineNOx: '', baselinePM25: '', baselineVOC: '', baselineCO2: '',
    });
    setError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/scenario/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          capacity: parseInt(formData.capacity),
          heatInput: Number(formData.heatInput),
          annualGeneration: Number(formData.annualGeneration),
          baselineSO2: Number(formData.baselineSO2),
          baselineNOx: Number(formData.baselineNOx),
          baselinePM25: Number(formData.baselinePM25),
          baselineVOC: Number(formData.baselineVOC),
          baselineCO2: Number(formData.baselineCO2),
        }),
      });
      if (!response.ok) {
        const err = await response.json();
        setError(`Error ${response.status}: ${JSON.stringify(err.detail ?? err)}`);
        return;
      }
      const data = await response.json();
      setResults(data, formData);
    } catch (err) {
      setError('Could not reach the backend. Is uvicorn running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.card}>
      <p style={styles.sectionLabel}>Step 1</p>
      <h2 style={styles.heading}>Plant details</h2>

      <form onSubmit={handleSubmit}>
        <div style={styles.grid}>
          {FIELDS.map(field => (
            <div
              key={field.name}
              style={{
                ...styles.fieldGroup,
                gridColumn: field.half ? 'span 1' : '1 / -1',
              }}
            >
              <label style={styles.label}>{field.label}</label>
              <input
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                placeholder={field.placeholder}
                onFocus={() => setFocusedField(field.name)}
                onBlur={() => setFocusedField(null)}
                style={{
                  ...styles.input,
                  borderColor: focusedField === field.name ? '#10B981' : '#374151',
                }}
              />
              <span style={styles.hint}>{field.hint}</span>
            </div>
          ))}
        </div>

        {error && <p style={styles.error}>{error}</p>}

        <div style={styles.footer}>
          <button
            type="submit"
            disabled={loading}
            style={{ ...styles.submitBtn, opacity: loading ? 0.6 : 1 }}
          >
            {loading ? 'Calculating…' : 'Calculate scenarios ↗'}
          </button>
          <button type="button" onClick={handleReset} style={styles.resetBtn}>
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}