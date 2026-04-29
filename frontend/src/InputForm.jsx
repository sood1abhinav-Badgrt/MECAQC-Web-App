import { useState } from 'react';

const FIELDS = [
  { name: 'state',           label: 'State',              hint: 'Two-letter code',       placeholder: 'e.g. AL',      half: true, type: "string"},
  { name: 'capacity',        label: 'Nameplate capacity', hint: 'MW',                    placeholder: 'e.g. 403',     half: true, type: "number"},
  { name: 'heatInput',       label: 'Annual heat input',  hint: 'MMBtu/yr — from CAMPD', placeholder: 'e.g. 1598916', half: true, type: "number"  },
  { name: 'annualGeneration',label: 'Annual generation',  hint: 'MWh/yr — from CAMPD',   placeholder: 'e.g. 166714',  half: true, type: "number"  },
  { name: 'baselineSO2',     label: 'Baseline SO₂',       hint: 'short tons/yr',         placeholder: 'e.g. 953',     half: true, type: "number"  },
  { name: 'baselineNOx',     label: 'Baseline NOₓ',       hint: 'short tons/yr',         placeholder: 'e.g. 227',     half: true, type: "number"  },
  { name: 'baselinePM25',    label: 'Baseline PM₂.₅',     hint: 'short tons/yr',         placeholder: 'e.g. 71.6',    half: true, type: "number"  },
  { name: 'baselineVOC',     label: 'Baseline VOC',       hint: 'short tons/yr',         placeholder: 'e.g. 4.1',     half: true, type: "number"  },
  { name: 'baselineCO2',     label: 'Baseline CO₂',       hint: 'short tons/yr',         placeholder: 'e.g. 164046',  half: false, type: "number"},
];

const styles = {
  card: {
    background: '#221F23',
    border: '0.5px solid #332F35',
    borderRadius: 12,
    padding: '20px',
  },
  sectionLabel: {
    fontSize: 10,
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
    color: '#615D65',
    marginBottom: 10,
  },
  heading: {
    fontSize: 13,
    fontWeight: 500,
    color: '#F2EFF4',
    margin: '0 0 14px 0',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '10px 8px',
  },
  fieldGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
  },
  label: {
    fontSize: 11,
    color: '#9E9AA2',
    fontWeight: 400,
  },
  input: {
    background: '#2A2729',
    border: '0.5px solid #332F35',
    borderRadius: 7,
    padding: '7px 10px',
    fontSize: 12,
    color: '#F2EFF4',
    outline: 'none',
    transition: 'border-color 0.15s',
    width: '100%',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
  },
  hint: {
    fontSize: 10,
    color: '#615D65',
  },
  footer: {
    marginTop: 16,
    display: 'flex',
    alignItems: 'center',
    gap: 12,
  },
  submitBtn: {
    padding: '8px 18px',
    fontSize: 12,
    fontWeight: 500,
    background: '#1D9E75',
    color: '#fff',
    border: 'none',
    borderRadius: 7,
    cursor: 'pointer',
    transition: 'opacity 0.15s',
  },
  resetBtn: {
    fontSize: 11,
    color: '#615D65',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    textDecoration: 'underline',
    fontFamily: 'inherit',
  },
  error: {
    fontSize: 12,
    color: '#E24B4A',
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
    for(const field of FIELDS)
    {
      const value = formData[field.name]
      if(value == "" || (field.type == "number" && Number.isFinite(Number(value)) == false))
      {
        setError("Please fill in all fields with valid numbers.")
        return;
      }  
      
    }
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
            <>
              {field.name === 'baselineSO2' && (
                <>
                  <div style={{ gridColumn: '1 / -1', borderTop: '0.5px solid #332F35', margin: '6px 0' }} />
                  <p style={{ ...styles.sectionLabel, gridColumn: '1 / -1', marginBottom: 4 }}>Baseline emissions</p>
                </>
              )}
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
                    borderColor: focusedField === field.name ? '#1D9E75' : '#332F35',
                  }}
                />
                <span style={styles.hint}>{field.hint}</span>
              </div>
            </>
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