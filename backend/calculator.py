from mock_data import baselineEmissions, technologyEffectiveness, costPerTonDefaults
from schema import ReductionOutput, ScenarioResult, CostOutput

def calculateScenario(inputScenario):
    print("calculateScenario called")
    sector = inputScenario.sector
    baseline = baselineEmissions[sector]
    SO2Baseline = baseline["SO2"]
    NOxBaseline = baseline["NOx"]
    VOCBaseline = baseline["VOC"]
    CO2Baseline = baseline["CO2"]
    totalReductions = {
        "SO2": SO2Baseline,
        "NOx": NOxBaseline,
        "VOC": VOCBaseline,
        "CO2": CO2Baseline
    }   

   
    #timeFactor = inputScenario.timelineYears/ 10 #Choose 10 as a standard timeline base

    '''
    Right now we assume that each technology is stacked on each other
    Check to see what MECAQC actually uses
    '''
    for tech in inputScenario.technologies:
        
        totalReductions["SO2"] = totalReductions["SO2"] * technologyEffectiveness[tech.name]["SO2"] * (tech.scalePercent / 100) 
        
        totalReductions["NOx"] = totalReductions["NOx"] * technologyEffectiveness[tech.name]["NOx"] * (tech.scalePercent / 100) 
        

        totalReductions["VOC"] = totalReductions["VOC"] * technologyEffectiveness[tech.name]["VOC"] * (tech.scalePercent / 100)
        
        totalReductions["CO2"] = totalReductions["CO2"] * technologyEffectiveness[tech.name]["CO2"] * (tech.scalePercent / 100) 
    
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
