# All constants sourced from Wu et al. 2024, supplementary materials, and Tracey Holloway control table
# Emission rates from Table S2.2, BPT values from Table S2.5
# Control efficiencies: SO2 from Wu et al. 2024, NOx and PM25 from Holloway control table (upper bounds)

# Nationally uniform
HR_NG = 7.649                # MMBtu/MWh — EIA NGCC heat rate
HEAT_RATE_PENALTY = 0.0163   # 1.63% — applied to AC co-pollutants
DISCOUNT_RATE = 0.07         # 7%
ASSET_LIFE = 20              # years
ANNUALIZATION = 0.07 / (1 - (1.07 ** -20))  # = 0.09439

SCC_CO2 = 185.0              # $/ton — Social Cost of Carbon
BPT_VOC = 2400.0             # $/ton — nationally uniform

# Capital costs ($/kW) — 2020 EIA
CAP_NG    = 1084.0
CAP_SOLAR = 1331.0
CAP_WIND  = 1473.0

# O&M costs
OM_COAL_FIXED  = 29.15   # $/kW/yr
OM_NG_FIXED    = 12.15   # $/kW/yr
OM_NG_VAR      = 3.37    # $/MWh
OM_SOLAR_FIXED = 22.02   # $/kW/yr
OM_WIND_FIXED  = 39.55   # $/kW/yr

# Natural gas emission rates (lb/MMBtu)
ER_NG = {
    "so2":  0.0001,
    "nox":  0.1,
    "pm25": 0.0076,
    "voc":  0.0021,
    "co2":  116.9,   # lb/MMBtu
}

# Coal O&M and fuel — state-specific in real data
# For now use national averages
FUEL_COAL = 2.21    # $/MMBtu — 2020 national average
FUEL_NG   = 2.39    # $/MMBtu — 2020 national average

# AC scrubber control efficiency
ETA_SDA         = 0.95   # spray dryer absorber (50–100 MW)
ETA_WET_SCRUBBER = 0.98  # wet scrubber (>100 MW)


coalConstants = {
    "heatRate": 10.62,          # MMBtu/MWh, average for existing uncontrolled coal EGUs
    "emissionRates": {          # lb/MMBtu, from Table S2.2
        "SO2": 0.567,
        "NOx": 0.203,
        "VOC": 0.003,
        "PM25": 0.021,
        "CO2": 208.08
    }
}

gasConstants = {
    "heatRate": 7.649,          # MMBtu/MWh, EIA average for NGCC plants
    "emissionRates": {          # lb/MMBtu, from Table S2.2
        "SO2": 0.00059,
        "NOx": 0.011,
        "VOC": 0.0054,
        "PM25": 0.0079,
        "CO2": 117.08
    }
}

# SO2 controls from Wu et al. 2024
# NOx and PM25 controls from Holloway control table, upper bound removal efficiencies
# heatRatePenalty applies to all co-pollutants in SO2 controls per Wu et al. 2024
controlConstants = {
    "SO2": {
        "wetFGD": {
            "removalEfficiency": 0.98,      # Wu et al. 2024, MRC
            "type": "MRC",
            "targetPollutant": "SO2"
        },
        "dryFGD": {
            "removalEfficiency": 0.90,      # Wu et al. 2024, MRC
            "type": "MRC",
            "targetPollutant": "SO2"
        },
        "SDA": {
            "removalEfficiency": 0.95,      # Wu et al. 2024, LCC
            "type": "LCC",
            "targetPollutant": "SO2"
        },
    },
    "NOx": {
        "SCR": {
            "removalEfficiency": 0.90,      # Holloway table, upper bound, LCC
            "type": "LCC",
            "targetPollutant": "NOx"
        },
        "SNCR": {
            "removalEfficiency": 0.55,      # Holloway table, upper bound, MRC
            "type": "MRC",
            "targetPollutant": "NOx"
        },
    },
    "PM25": {
        "ESP": {
            "removalEfficiency": 0.95,      # Holloway table, upper bound, LCC
            "type": "LCC",
            "targetPollutant": "PM25"
        },
        "fabricFilter": {
            "removalEfficiency": 0.99,      # Holloway table, upper bound, MRC
            "type": "MRC",
            "targetPollutant": "PM25"
        },
    },
    "heatRatePenalty": 0.0163               # 1.63% co-pollutant increase, Wu et al. 2024
}

# BPT values in $/ton, from Table S2.5
# SO2 BPT: health benefits from secondary PM2.5 (SO2 as precursor)
# NOx BPT: health benefits from secondary PM2.5 and ozone (NOx as precursor)
# VOC BPT: uniform national value across all states
# PM25 BPT: health benefits from directly emitted PM2.5
# SCC: social cost of carbon, nationally uniform, $/ton CO2
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



SUPPORTED_STATES = set(bptByState.keys())