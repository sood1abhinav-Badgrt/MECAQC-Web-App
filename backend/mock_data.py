# All constants sourced from Wu et al. 2024 (SI_XW_2020.pdf) and MECAQC zip.
# Table references are to SI_XW_2020.pdf unless otherwise noted.
# NOx and PM25 control efficiencies from Holloway control table (not in paper).

# ── Nationally uniform ────────────────────────────────────────────────────────

HEAT_RATE_PENALTY = 0.0163   # 1.63% — Table S2.1, EPA IPM v6 Ch. 5
DISCOUNT_RATE     = 0.07     # 7% — Equation S2.5
ASSET_LIFE        = 20       # years — Equation S2.5
ANNUALIZATION     = 0.07 / (1 - (1.07 ** -20))  # capital recovery factor ≈ 0.09439

SCC_CO2 = 185.0   # $/ton — Table S2.5
BPT_VOC = 2400.0  # $/ton — Table S2.5

# ── Capital costs ($/kW) — Table S2.3, EIA Capital Cost Estimates 2016 ───────

CAP_NG    = 1046.0    # $/kW — NGCC capital cost
CAP_SOLAR = 2721.0    # $/kW — utility-scale solar PV
CAP_WIND  = 2008.0    # $/kW — onshore wind

# ── O&M costs — Table S2.3, EIA Generating Unit Annual Capital 2019 ──────────

# BAU coal — two rates by plant size per Table S2.3
OM_COAL_FIXED_SMALL = 46.53   # $/kW/yr — capacity < 500 MW
OM_COAL_FIXED_LARGE = 35.80   # $/kW/yr — capacity >= 500 MW
OM_COAL_VAR         =  1.87   # $/MWh

# GT gas
OM_NG_FIXED = 11.77   # $/kW/yr — NGCC fixed O&M
OM_NG_VAR   =  3.70   # $/MWh   — NGCC variable O&M

# RT renewables
OM_SOLAR_FIXED = 25.50   # $/kW/yr — solar PV fixed O&M
OM_WIND_FIXED  = 42.40   # $/kW/yr — onshore wind fixed O&M

# ── Fuel costs — Table S2.3, EIA Table 7.4 ───────────────────────────────────

FUEL_COAL = 2.11   # $/MMBtu — 2020 coal price (bituminous)
FUEL_NG   = 2.40   # $/MMBtu — 2020 natural gas price

# ── Methane leak constants — Equations S2.11, S2.12 ──────────────────────────

NG_HEAT_CONTENT   = 0.0366   # MMBtu/m³  — EIA, SI footnote 6
METHANE_DENSITY   = 0.667    # kg/m³     — IPCC, SI footnote 7
METHANE_LEAK_RATE = 0.015    # 1.5%      — Alvarez et al. 2018, SI footnote 9
                              #             confirmed by zip sheet name
                              #             "consider methane leak (1.5)"
CH4_GWP_20YR      = 84       # dimensionless — IPCC AR5, SI footnotes 10-11
                              #                 confirmed by back-calculation
                              #                 from zip CH4_CO2 equi column

# ── Coal emission constants — Table S2.2 ─────────────────────────────────────

coalConstants = {
    "heatRate": 10.62,        # MMBtu/MWh — existing uncontrolled coal EGUs
    "emissionRates": {        # lb/MMBtu
        "SO2":  0.567,
        "NOx":  0.203,
        "VOC":  0.003,
        "PM25": 0.021,
        "CO2":  208.08        # /2000 = 0.10404 short tons/MMBtu ✓ CAMPD CO2 Rate
    }
}

# ── Gas emission constants — Table S2.2 ──────────────────────────────────────

gasConstants = {
    "heatRate": 7.649,        # MMBtu/MWh — EIA Table 8.2, SI Equation S2.4 text
                              # Note: Table S2.2 shows 7.69 but S2.4 text says 7.649
                              # Using 7.649 per equation text
    "emissionRates": {        # lb/MMBtu
        "SO2":  0.00059,
        "NOx":  0.011,
        "VOC":  0.0054,
        "PM25": 0.0079,
        "CO2":  117.08
    }
}

# ── Control efficiencies ──────────────────────────────────────────────────────
# SO2: Table S2.1, EPA IPM v6
# NOx, PM25: Holloway control table (upper bounds) — not in paper

controlConstants = {
    "SO2": {
        "wetFGD": {
            "removalEfficiency": 0.98,   # >100 MW — Table S2.1
            "type": "MRC",
            "targetPollutant": "SO2"
        },
        "dryFGD": {
            "removalEfficiency": 0.90,   # Table S2.1
            "type": "MRC",
            "targetPollutant": "SO2"
        },
        "SDA": {
            "removalEfficiency": 0.95,   # 50-100 MW — Table S2.1
            "type": "LCC",
            "targetPollutant": "SO2"
        },
    },
    "NOx": {
        "SCR": {
            "removalEfficiency": 0.90,   # Holloway table, upper bound
            "type": "LCC",
            "targetPollutant": "NOx"
        },
        "SNCR": {
            "removalEfficiency": 0.55,   # Holloway table, upper bound
            "type": "MRC",
            "targetPollutant": "NOx"
        },
    },
    "PM25": {
        "ESP": {
            "removalEfficiency": 0.95,   # Holloway table, upper bound
            "type": "LCC",
            "targetPollutant": "PM25"
        },
        "fabricFilter": {
            "removalEfficiency": 0.99,   # Holloway table, upper bound
            "type": "MRC",
            "targetPollutant": "PM25"
        },
    },
    "heatRatePenalty": 0.0163            # 1.63% — Table S2.1
}

# ── AC scrubber capital and O&M ───────────────────────────────────────────────
# Source: EPA Control Cost Manual — not in SI_XW_2020.pdf
# Placeholder until Control Cost Manual equations are implemented

CAP_SCRUBBER = {
    "wetFGD": 700,   # $/kW
    "SDA":    350    # $/kW
}

OM_SCRUBBER_FIXED = {
    "wetFGD": 22,    # $/kW/yr
    "SDA":    14     # $/kw/yr
}

# ── BPT values — Table S2.5 ──────────────────────────────────────────────────
# SO2:  health benefits from secondary PM2.5 (SO2 as precursor)
# NOx:  health benefits from secondary PM2.5 and ozone (NOx as precursor)
# VOC:  nationally uniform
# PM25: health benefits from directly emitted PM2.5
# SCC:  nationally uniform social cost of carbon
# SO2 = 0 for some states = no monetized secondary PM2.5 pathway (BenMAP result)

bptByState = {
    "AL": {"SO2": 0,      "NOx": 59400, "VOC": 2400, "PM25": 99500,  "SCC": 185},
    "AR": {"SO2": 78950,  "NOx": 57515, "VOC": 2400, "PM25": 64400,  "SCC": 185},
    "CT": {"SO2": 0,      "NOx": 81735, "VOC": 2400, "PM25": 0,      "SCC": 185},
    "IA": {"SO2": 90400,  "NOx": 45020, "VOC": 2400, "PM25": 77500,  "SCC": 185},
    "IL": {"SO2": 90250,  "NOx": 69850, "VOC": 2400, "PM25": 147800, "SCC": 185},
    "IN": {"SO2": 109300, "NOx": 77950, "VOC": 2400, "PM25": 127500, "SCC": 185},
    "KY": {"SO2": 101050, "NOx": 75070, "VOC": 2400, "PM25": 58050,  "SCC": 185},
    "LA": {"SO2": 70750,  "NOx": 39299, "VOC": 2400, "PM25": 96400,  "SCC": 185},
    "MD": {"SO2": 290000, "NOx": 92970, "VOC": 2400, "PM25": 328500, "SCC": 185},
    "MI": {"SO2": 91250,  "NOx": 57955, "VOC": 2400, "PM25": 153850, "SCC": 185},
    "MN": {"SO2": 81900,  "NOx": 47935, "VOC": 2400, "PM25": 79300,  "SCC": 185},
    "MO": {"SO2": 80750,  "NOx": 66390, "VOC": 2400, "PM25": 47000,  "SCC": 185},
    "MS": {"SO2": 0,      "NOx": 50780, "VOC": 2400, "PM25": 81400,  "SCC": 185},
    "NE": {"SO2": 49550,  "NOx": 29395, "VOC": 2400, "PM25": 23500,  "SCC": 185},
    "NH": {"SO2": 61200,  "NOx": 46475, "VOC": 2400, "PM25": 0,      "SCC": 185},
    "NV": {"SO2": 0,      "NOx": 31260, "VOC": 2400, "PM25": 174000, "SCC": 185},
    "OH": {"SO2": 86750,  "NOx": 88950, "VOC": 2400, "PM25": 134900, "SCC": 185},
    "OK": {"SO2": 0,      "NOx": 42600, "VOC": 2400, "PM25": 129600, "SCC": 185},
    "TX": {"SO2": 0,      "NOx": 44455, "VOC": 2400, "PM25": 189000, "SCC": 185},
    "WY": {"SO2": 27750,  "NOx": 19740, "VOC": 2400, "PM25": 13555,  "SCC": 185},
}

# ── State-specific energy constants — Table S2.4 ──────────────────────────────
# Source: EPA eGRID 2020, cited in SI footnote 2
# Confirmed against zip uncontrolled_cost_benefits sheet
# IL and MO each span two EMM regions in Table S2.4 — zip uses one row per state.
# Values here match the zip's single row per state.
# solarPct, windPct: fraction of state utility-scale generation from each source
# CF_NG, CF_solar, CF_wind: capacity factors (dimensionless)
# cost_aj_NG, cost_aj_wind, cost_aj_solar: regional cost adjustment factors

stateEnergyConstants = {
    "AL": {"solarPct": 0.0026, "windPct": 0.0,    "CF_NG": 0.648, "CF_solar": 0.243, "CF_wind": 0.147, "cost_aj_NG": 0.93, "cost_aj_wind": 0.96, "cost_aj_solar": 0.89},
    "AR": {"solarPct": 0.005,  "windPct": 0.0,    "CF_NG": 0.623, "CF_solar": 0.257, "CF_wind": 0.147, "cost_aj_NG": 0.93, "cost_aj_wind": 0.96, "cost_aj_solar": 0.89},
    "CT": {"solarPct": 0.0052, "windPct": 0.0003, "CF_NG": 0.677, "CF_solar": 0.182, "CF_wind": 0.293, "cost_aj_NG": 1.16, "cost_aj_wind": 1.06, "cost_aj_solar": 1.03},
    "IA": {"solarPct": 0.0004, "windPct": 0.5732, "CF_NG": 0.399, "CF_solar": 0.214, "CF_wind": 0.432, "cost_aj_NG": 0.97, "cost_aj_wind": 1.03, "cost_aj_solar": 0.95},
    "IL": {"solarPct": 0.0005, "windPct": 0.0936, "CF_NG": 0.41,  "CF_solar": 0.226, "CF_wind": 0.382, "cost_aj_NG": 1.06, "cost_aj_wind": 1.04, "cost_aj_solar": 1.05},
    "IN": {"solarPct": 0.004,  "windPct": 0.0698, "CF_NG": 0.742, "CF_solar": 0.201, "CF_wind": 0.33,  "cost_aj_NG": 1.04, "cost_aj_wind": 1.02, "cost_aj_solar": 1.0},
    "KY": {"solarPct": 0.0007, "windPct": 0.0,    "CF_NG": 0.732, "CF_solar": 0.167, "CF_wind": 0.147, "cost_aj_NG": 0.93, "cost_aj_wind": 0.96, "cost_aj_solar": 0.89},
    "LA": {"solarPct": 0.0004, "windPct": 0.0,    "CF_NG": 0.639, "CF_solar": 0.241, "CF_wind": 0.147, "cost_aj_NG": 0.93, "cost_aj_wind": 0.96, "cost_aj_solar": 0.89},
    "MD": {"solarPct": 0.0146, "windPct": 0.0149, "CF_NG": 0.527, "CF_solar": 0.19,  "CF_wind": 0.299, "cost_aj_NG": 1.21, "cost_aj_wind": 1.05, "cost_aj_solar": 1.05},
    "MI": {"solarPct": 0.0015, "windPct": 0.0632, "CF_NG": 0.587, "CF_solar": 0.212, "CF_wind": 0.322, "cost_aj_NG": 1.0,  "cost_aj_wind": 1.0,  "cost_aj_solar": 0.97},
    "MN": {"solarPct": 0.0288, "windPct": 0.2093, "CF_NG": 0.32,  "CF_solar": 0.196, "CF_wind": 0.366, "cost_aj_NG": 0.97, "cost_aj_wind": 1.03, "cost_aj_solar": 0.95},
    "MO": {"solarPct": 0.0014, "windPct": 0.0465, "CF_NG": 0.335, "CF_solar": 0.196, "CF_wind": 0.362, "cost_aj_NG": 1.06, "cost_aj_wind": 1.04, "cost_aj_solar": 1.05},
    "MS": {"solarPct": 0.0065, "windPct": 0.0,    "CF_NG": 0.665, "CF_solar": 0.227, "CF_wind": 0.147, "cost_aj_NG": 0.93, "cost_aj_wind": 0.96, "cost_aj_solar": 0.89},
    "NE": {"solarPct": 0.0015, "windPct": 0.248,  "CF_NG": 0.168, "CF_solar": 0.239, "CF_wind": 0.448, "cost_aj_NG": 0.97, "cost_aj_wind": 1.03, "cost_aj_solar": 0.95},
    "NH": {"solarPct": 0.0002, "windPct": 0.0315, "CF_NG": 0.438, "CF_solar": 0.186, "CF_wind": 0.26,  "cost_aj_NG": 1.16, "cost_aj_wind": 1.06, "cost_aj_solar": 1.03},
    "NV": {"solarPct": 0.1372, "windPct": 0.0073, "CF_NG": 0.464, "CF_solar": 0.291, "CF_wind": 0.24,  "cost_aj_NG": 1.01, "cost_aj_wind": 1.05, "cost_aj_solar": 0.99},
    "OH": {"solarPct": 0.0014, "windPct": 0.0189, "CF_NG": 0.813, "CF_solar": 0.219, "CF_wind": 0.328, "cost_aj_NG": 1.04, "cost_aj_wind": 1.02, "cost_aj_solar": 1.0},
    "OK": {"solarPct": 0.0008, "windPct": 0.3574, "CF_NG": 0.357, "CF_solar": 0.2,   "CF_wind": 0.377, "cost_aj_NG": 0.99, "cost_aj_wind": 1.02, "cost_aj_solar": 0.97},
    "TX": {"solarPct": 0.018,  "windPct": 0.1953, "CF_NG": 0.546, "CF_solar": 0.253, "CF_wind": 0.352, "cost_aj_NG": 0.91, "cost_aj_wind": 0.95, "cost_aj_solar": 0.87},
    "WY": {"solarPct": 0.0039, "windPct": 0.1312, "CF_NG": 0.328, "CF_solar": 0.231, "CF_wind": 0.371, "cost_aj_NG": 1.01, "cost_aj_wind": 1.03, "cost_aj_solar": 0.93},
}

SUPPORTED_STATES = set(bptByState.keys())