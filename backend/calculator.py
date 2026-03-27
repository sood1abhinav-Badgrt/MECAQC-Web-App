from mock_data import baselineEmissions, technologyEffectiveness, costPerTonDefaults
from schema import ReductionOutput, ScenarioResult, CostOutput

def calculateScenario(inputScenario):
    sector = inputScenario.sector
    baseline = baselineEmissions[sector]
    totalReductions = {
        "SO2": 0,
        "NOx": 0,
        "VOC": 0,
        "CO2": 0
    }   

    SO2Baseline = baseline["SO2"]
    NOxBaseline = baseline["NOx"]
    VOCBaseline = baseline["VOC"]
    CO2Baseline = baseline["CO2"]
    timeFactor = inputScenario.timelineYears/ 10 #Choose 10 as a standard timeline base

    '''
    Right now we assume that each technology is applied to the base
    Check to see what MECAQC actually uses
    '''
    for tech in inputScenario.technologies:
        techSO2Reduction = SO2Baseline * technologyEffectiveness[tech.name]["SO2"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["SO2"] = totalReductions["SO2"] + techSO2Reduction
        
        techNOxReduction = NOxBaseline * technologyEffectiveness[tech.name]["NOx"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["NOx"] = totalReductions["NOx"] + techNOxReduction
        
        techVOCReduction = VOCBaseline * technologyEffectiveness[tech.name]["VOC"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["VOC"] = totalReductions["VOC"] + techVOCReduction
        
        techCO2Reduction = CO2Baseline * technologyEffectiveness[tech.name]["CO2"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["CO2"] = totalReductions["CO2"] + techCO2Reduction
    
    emissionReductionOutput = ReductionOutput(
        SO2TonsPerYear = totalReductions["SO2"],
        NOxTonsPerYear = totalReductions["NOx"],
        VOCTonsPerYear = totalReductions["VOC"],
        CO2TonsPerYear = totalReductions["CO2"]
    )

    return ScenarioResult(
        state = inputScenario.state,
        sector = inputScenario.sector,
        timelineYears = inputScenario.timelineYears,
        reductions = emissionReductionOutput,
        costPerTon = CostOutput(
            SO2 = costPerTonDefaults["SO2"],
            NOx = costPerTonDefaults["NOx"],
            VOC = costPerTonDefaults["VOC"],
            CO2 = costPerTonDefaults["CO2"]
        ),
        summary = "Verify that we returned the correct numbers."

    )
