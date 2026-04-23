import { useState } from 'react';

const SCENARIOS = [
  { key: 'bau', label: 'BAU', name: 'Business as Usual', color: '#6B7280' },
  { key: 'ac',  label: 'AC',  name: 'Add-on Scrubber',   color: '#F59E0B' },
  { key: 'gt',  label: 'GT',  name: 'Gas Transition',    color: '#3B82F6' },
  { key: 'rt',  label: 'RT',  name: 'Renewable',         color: '#10B981' },
];

const POLLUTANTS = [
  { key: 'SO2ChangePerYear',  label: 'SO₂',   unit: 't/yr' },
  { key: 'NOxChangePerYear',  label: 'NOₓ',   unit: 't/yr' },
  { key: 'PM25ChangePerYear', label: 'PM₂.₅', unit: 't/yr' },
  { key: 'VOCChangePerYear',  label: 'VOC',   unit: 't/yr' },
  { key: 'CO2ChangePerYear',  label: 'CO₂',   unit: 't/yr' },
];

function fmt$(n) {
  const abs = Math.abs(n);
  const sign = n < 0 ? '-' : '+';
  if (abs >= 1e9) return `${sign}$${(abs / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${sign}$${(abs / 1e6).toFixed(1)}M`;
  if (abs >= 1e3) return `${sign}$${(abs / 1e3).toFixed(0)}K`;
  return `${sign}$${abs.toFixed(0)}`;
}

function fmtT(n) {
  const abs = Math.abs(n);
  const sign = n < 0 ? '-' : '+';
  if (abs >= 1e6) return `${sign}${(abs / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${sign}${(abs / 1e3).toFixed(1)}K`;
  return `${sign}${abs.toFixed(1)}`;
}

function BarRow({ label, value, maxAbs, color, formatFn }) {
  const pct = maxAbs > 0 ? (Math.abs(value) / maxAbs) * 100 : 0;
  const isPos = value >= 0;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
      <span style={{ width: 36, fontSize: 12, color: '#9CA3AF', flexShrink: 0, fontFamily: 'monospace' }}>
        {label}
      </span>
      <div style={{ flex: 1, height: 6, background: '#1F2937', borderRadius: 3, overflow: 'hidden' }}>
        <div style={{
          height: '100%',
          width: `${pct.toFixed(1)}%`,
          background: isPos ? color : '#EF4444',
          borderRadius: 3,
          transition: 'width 0.6s cubic-bezier(0.4,0,0.2,1)',
        }} />
      </div>
      <span style={{
        width: 72, fontSize: 12, textAlign: 'right', flexShrink: 0,
        color: isPos ? color : '#EF4444',
        fontFamily: 'monospace', fontWeight: 500,
      }}>
        {formatFn(value)}
      </span>
    </div>
  );
}

export default function ResultsPanel({ results, plantMeta }) {
  const [selected, setSelected] = useState('rt');
  const scenario = results[selected];
  const accentColor = SCENARIOS.find(s => s.key === selected)?.color ?? '#10B981';

  const maxRedAbs = Math.max(...POLLUTANTS.map(p => Math.abs(scenario.reductions[p.key] ?? 0)));

  const benefitByPollutant = selected !== 'bau'
    ? POLLUTANTS.map(p => ({ ...p, value: scenario.reductions[p.key] ?? 0 }))
    : [];
  const maxBenAbs = Math.max(...benefitByPollutant.map(b => Math.abs(b.value)));

  return (
    <div style={{
      fontFamily: "'IBM Plex Sans', 'DM Sans', sans-serif",
      color: '#F9FAFB',
      background: '#0F1117',
      borderRadius: 16,
      padding: '28px 32px',
      marginTop: 24,
      border: '1px solid #1F2937',
    }}>

      {/* Header row */}
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 24 }}>
        <div>
          <p style={{ fontSize: 11, letterSpacing: '0.1em', textTransform: 'uppercase', color: '#6B7280', marginBottom: 4 }}>
            Scenario Analysis
          </p>
          <h2 style={{ fontSize: 20, fontWeight: 600, margin: 0, color: '#F9FAFB' }}>
            Results
          </h2>
        </div>
        {plantMeta && (
          <div style={{ display: 'flex', gap: 8 }}>
            {[plantMeta.state, `${plantMeta.capacity} MW`, `${Number(plantMeta.annualGeneration).toLocaleString()} MWh/yr`].map(tag => (
              <span key={tag} style={{
                fontSize: 11, padding: '3px 10px',
                borderRadius: 6, background: '#1F2937',
                border: '1px solid #374151', color: '#9CA3AF',
              }}>{tag}</span>
            ))}
          </div>
        )}
      </div>

      {/* Scenario selector cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginBottom: 24 }}>
        {SCENARIOS.map(s => {
          const nb = results[s.key]?.netBenefits?.netBenefit ?? 0;
          const isSelected = selected === s.key;
          return (
            <button
              key={s.key}
              onClick={() => setSelected(s.key)}
              style={{
                background: isSelected ? '#1A1F2E' : '#111827',
                border: isSelected ? `1.5px solid ${s.color}` : '1px solid #1F2937',
                borderRadius: 12,
                padding: '14px 16px',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.2s ease',
              }}
            >
              <div style={{
                display: 'inline-block', fontSize: 10, fontWeight: 600,
                letterSpacing: '0.08em', padding: '2px 7px',
                borderRadius: 4, marginBottom: 8,
                background: `${s.color}22`, color: s.color,
              }}>
                {s.label}
              </div>
              <div style={{ fontSize: 12, color: '#9CA3AF', marginBottom: 10, lineHeight: 1.3 }}>{s.name}</div>
              <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 3 }}>Net benefit / yr</div>
              <div style={{
                fontSize: 18, fontWeight: 700, fontFamily: 'monospace',
                color: nb >= 0 ? s.color : '#EF4444',
              }}>
                {fmt$(nb)}
              </div>
              {s.key === 'ac' && (
                <div style={{
                  marginTop: 8, fontSize: 10, padding: '2px 7px',
                  borderRadius: 4, background: '#78350F22', color: '#F59E0B',
                  display: 'inline-block',
                }}>
                  cost_ctrl = $0
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Detail panels */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>

        {/* Left: Emission reductions */}
        <div style={{
          background: '#111827', borderRadius: 12, padding: '18px 20px',
          border: '1px solid #1F2937',
        }}>
          <p style={{ fontSize: 11, color: '#6B7280', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 14 }}>
            Emission changes — {selected.toUpperCase()}
          </p>
          {selected === 'bau' ? (
            <div>
              <p style={{ fontSize: 13, color: '#6B7280', lineHeight: 1.7 }}>
                No emission reductions in BAU. This scenario represents continued coal operation and serves as the cost baseline.
              </p>
              <div style={{ marginTop: 16, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                {[
                  { label: 'Fixed O&M', value: results.bau.netBenefits.totalAnnualCost * 0.55 },
                  { label: 'Variable O&M', value: results.bau.netBenefits.totalAnnualCost * 0.14 },
                  { label: 'Fuel cost', value: results.bau.netBenefits.totalAnnualCost * 0.31 },
                  { label: 'Total TAC', value: results.bau.netBenefits.totalAnnualCost },
                ].map(row => (
                  <div key={row.label} style={{ background: '#0F1117', borderRadius: 8, padding: '10px 12px' }}>
                    <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 4 }}>{row.label}</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: '#EF4444', fontFamily: 'monospace' }}>
                      {fmt$(row.value).replace('+', '')}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            POLLUTANTS.map(p => (
              <BarRow
                key={p.key}
                label={p.label}
                value={scenario.reductions[p.key] ?? 0}
                maxAbs={maxRedAbs}
                color={accentColor}
                formatFn={fmtT}
              />
            ))
          )}
        </div>

        {/* Right: Net benefits breakdown */}
        <div style={{
          background: '#111827', borderRadius: 12, padding: '18px 20px',
          border: '1px solid #1F2937',
        }}>
          <p style={{ fontSize: 11, color: '#6B7280', letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 14 }}>
            Financials — {selected.toUpperCase()}
          </p>

          {/* Summary stat */}
          <div style={{ marginBottom: 18, padding: '14px 16px', background: '#0F1117', borderRadius: 10, border: `1px solid ${accentColor}33` }}>
            <div style={{ fontSize: 11, color: '#6B7280', marginBottom: 4 }}>Net benefit / year</div>
            <div style={{
              fontSize: 28, fontWeight: 700, fontFamily: 'monospace',
              color: scenario.netBenefits.netBenefit >= 0 ? accentColor : '#EF4444',
            }}>
              {fmt$(scenario.netBenefits.netBenefit)}
            </div>
          </div>

          {/* Cost breakdown rows */}
          {[
            { label: 'Total health & climate benefit', value: scenario.netBenefits.totalBenefit, positive: true },
            { label: 'Total annual cost (TAC)', value: -scenario.netBenefits.totalAnnualCost, positive: false },
            { label: 'Net benefit', value: scenario.netBenefits.netBenefit, positive: scenario.netBenefits.netBenefit >= 0 },
          ].map((row, i) => (
            <div key={i} style={{
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              padding: '8px 0',
              borderBottom: i < 2 ? '1px solid #1F2937' : 'none',
            }}>
              <span style={{ fontSize: 12, color: '#9CA3AF' }}>{row.label}</span>
              <span style={{
                fontSize: 13, fontWeight: 600, fontFamily: 'monospace',
                color: row.positive ? accentColor : '#EF4444',
              }}>
                {fmt$(row.value)}
              </span>
            </div>
          ))}

          <p style={{ marginTop: 14, fontSize: 11, color: '#4B5563', lineHeight: 1.6 }}>
            All costs in 2020 dollars. Source: Wu et al. 2024, ERL.
            {selected === 'ac' && ' AC cost_ctrl = $0 placeholder.'}
            {selected === 'gt' && ' Includes methane leak penalty.'}
          </p>
        </div>
      </div>
    </div>
  );
}