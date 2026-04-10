#Placeholder for data to test work
baselineEmissions ={
    "SO2": 12000,   # tons/year (from CAMPD 2020)
    "NOx": 8000,
    "PM25": 2000,
    "VOC": 1500,
    "CO2": 26000000
}
scrubberConstants = {
    "SDA": {"removalEfficiency": 0.95},    # plants that produce 50-100MW of electricty
    "wetScrubber": {"removalEfficiency": 0.98},  # plants that produce 100MW+ of electricty
    "heatRatePenalty": 0.0163     # 1.63% increases co-pollutants
}

gasConstants = {
    "heatRateNG": 7.649,        # MMBtu/MWh
    "emissionRates": {           # lb/MMBtu
        "SO2": 0.001,
        "NOx": 0.1,
        "PM25": 0.005,
        "VOC": 0.005,
        "CO2": 116.9
    },
    "methaneLeakageRate": 0.023,
    "methaneGWP": 84
}

renewableConstants = {
    "emissionReductionRate": 1.0   # 100% reduction in direct emissions
}

benefitPerTon = {
    "SO2": 38000,
    "NOx": 7600,
    "PM25": 38000,
    "VOC": 950,
    "CO2": 51
}