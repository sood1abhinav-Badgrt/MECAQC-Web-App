#Placeholder for data to test work
baselineEmissions = {
    "electricity": {"SO2": 12000, "NOx": 8000, "VOC": 1500, "CO2": 26000000},
    "transportation": {"SO2": 500, "NOx": 14000, "VOC": 9000, "CO2": 18000000},
    "industrial": {"SO2": 7000, "NOx": 6000, "VOC": 5000, "CO2": 12000000},
    "areaSources": {"SO2": 300, "NOx": 1200, "VOC": 11000, "CO2": 2000000}
}

technologyEffectiveness = {
    "coal_to_renewables": {"SO2": 0.85, "NOx": 0.55, "VOC": 0.10, "CO2": 0.90},
    "electric_vehicles": {"SO2": 0.05, "NOx": 0.60, "VOC": 0.45, "CO2": 0.70},
    "thermal_oxidizers": {"SO2": 0.00, "NOx": 0.05, "VOC": 0.80, "CO2": 0.02},
    "air_fuel_ratio_adjustment": {"SO2": 0.00, "NOx": 0.40, "VOC": 0.10, "CO2": 0.08}
}

costPerTonDefaults = {
    "SO2": 820,
    "NOx": 1100,
    "VOC": 950,
    "CO2": 42
}