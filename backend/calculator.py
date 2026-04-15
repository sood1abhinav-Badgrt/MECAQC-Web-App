from mock_data import coalConstants, scrubberConstants, gasConstants, bptByState
from schema import ReductionOutput, ScenarioResult, CostOutput, PlantInput

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
    if input.capacity >  50 & input.capacity < 100:
        removalEffiency = .95
    elif input.capacity == 100:
        removalEffiency = .98
    heatRatePenalty = scrubberConstants["heatRatePenalty"]

    deltaEmissionsSO2 = (input.baselineSO2) * removalEfficiency 
    deltaEmissionsPM25 = (input.baselinePM25) * removalEfficiency 

    #Co-Pollutants
    deltaEmissionsNOx = (input.baselineNOx) * heatRatePenalty 
    deltaEmissionsCO2 = (input.baselineCO2) * heatRatePenalty
    deltaEmissionsVOC = (input.baselineVOC) * heatRatePenalty 

    return ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2,
        NOxChangePerYear = -deltaEmissionsNOx,
        PM25ChangePerYear = deltaEmissionsPM25,
        CO2ChangePerYear = -deltaEmissionsCO2,
        VOCChangePerYear = -deltaEmissionsVOC
    )






