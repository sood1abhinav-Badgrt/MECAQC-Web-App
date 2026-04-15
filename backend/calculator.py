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

    reductionOutputAC = ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2,
        NOxChangePerYear = -deltaEmissionsNOx,
        PM25ChangePerYear = deltaEmissionsPM25,
        CO2ChangePerYear = -deltaEmissionsCO2,
        VOCChangePerYear = -deltaEmissionsVOC
    )

    #Calculating Benefits
    state = input.state
    netBenefits = 0
    netBenefits += (bptByState[state]["SO2"] * reductionOutputAC.SO2ChangePerYear)
    netBenefits += (bptByState[state]["CO2"] * reductionOutputAC.CO2ChangePerYear)
    netBenefits += (bptByState[state]["NOx"] * reductionOutputAC.NOxChangePerYear)
    netBenefits += (bptByState[state]["PM25"] * reductionOutputAC.PM25ChangePerYear)
    netBenefits += (bptByState[state]["VOC"] * reductionOutputAC.VOCChangePerYear)

    #Total Annual Cost for switching to Add on Control
    '''costControlSO2 = 
    tacAC = ]

    netBenefits = netBenefits - '''

def calcualteGT(input):
    deltaEmissionsSO2 = input.baselineSO2 - (input.annualGeneration * gasConstants["heatRate"] * gasConstants["emissionRates"]["SO2"]) / 2000
    deltaEmissionsNOx = input.baselineNOx - (input.annualGeneration * gasConstants["heatRate"] * gasConstants["emissionRates"]["NOx"]) / 2000
    deltaEmissionsVOC = input.baselineVOC - (input.annualGeneration * gasConstants["heatRate"] * gasConstants["emissionRates"]["VOC"]) / 2000
    deltaEmissionsPM25 = input.baselinePM25 - (input.annualGeneration * gasConstants["heatRate"] * gasConstants["emissionRates"]["PM25"]) / 2000
    deltaEmissionsCO2 = input.baselineCO2 - (input.annualGeneration * gasConstants["heatRate"] * gasConstants["emissionRates"]["CO2"]) / 2000           
    
    reductionOutputGT = ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2,
        NOxChangePerYear = deltaEmissionsNOx,
        PM25ChangePerYear = deltaEmissionsPM25,
        CO2ChangePerYear = deltaEmissionsCO2,
        VOCChangePerYear = deltaEmissionsVOC
    )

def calculateRT(input):
    deltaEmissionsSO2 = input.baselineSO2
    deltaEmissionsNOx = input.baselineNOx
    deltaEmissionsPM25 = input.baselinePM25
    deltaEmissionsVOC = input.baselineVOC
    deltaEmissionsCO2 = input.baselineCO2

    reductionOutputRT = ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2,
        NOxChangePerYear = deltaEmissionsNOx,
        PM25ChangePerYear = deltaEmissionsPM25,
        CO2ChangePerYear = deltaEmissionsCO2,
        VOCChangePerYear = deltaEmissionsVOC
    )












