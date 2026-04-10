from mock_data import baselineEmissions, scrubberConstants, gasConstants, renewableConstants, benefitPerTon
from schema import ReductionOutput, ScenarioResult, CostOutput

def calculateScenario(input):
    if input.scenario == "BAU":
        return calculateBAU(input)
    elif input.scenario == "AC":
        return calculateAC(input)
    elif input.scenario == "GT":
        return calculateGT(input)
    elif input.scenario == "RT":
        return calculateRT(input)

def calculateAC(input):
    removalEfficiency = scrubberConstants["wetScrubber"]["removalEfficiency"] #Should be .98 for now
    heatRatePenalty = scrubberConstants["heatRatePenalty"]
    deltaEmissionsSO2 = (baselineEmissions["SO2"]) * removalEfficiency * (input.coveragePercent / 100)
    deltaEmissionsPM = (baselineEmissions["PM25"]) * removalEfficiency * (input.coveragePercent / 100)

    #Co-Pollutants
    deltaEmissionsNOx = (baselineEmissions["NOx"]) * heatRatePenalty * (input.coveragePercent / 100)
    deltaEmissionsCO2 = (baselineEmissions["CO2"]) * heatRatePenalty * (input.coveragePercent / 100)

    return ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2,
        NOxChangePerYear = -deltaEmissionsNOx,
        PM25ChangePerYear = deltaEmissionsPM,
        CO2ChangePerYear = -deltaEmissionsCO2,
        VOCChangePerYear = 0.0
    )


