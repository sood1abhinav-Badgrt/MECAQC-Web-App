from mock_data import baselineEmissions, technologyEffectiveness, costPerTonDefaults
from schema import ReductionOutput, ScenarioResult, CostOutput

def calculateScenario(inputScenario):
    if input.scenario == "BAU":
        return calculateBAU(input)
    elif input.scenario == "AC":
        return calculateAC(input)
    elif input.scenario == "GT":
        return calculateGT(input)
    elif input.scenario == "RT":
        return calculateRT(input)