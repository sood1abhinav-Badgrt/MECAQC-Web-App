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



    '''
    Right now we assume that each technology is stacked on each other
    Check to see what MECAQC actually uses
    '''
    SO2Baseline = baseline["SO2"]
    NOxBaseline = baseline["NOx"]
    VOCBaseline = baseline["VOC"]
    CO2Baseline = baseline["CO2"]
    timeFactor = inputScenario.timelineYears / 10 #10 is just a placeholder for now
    for tech in inputScenario.technologies:
        techReductionSO2 = SO2Baseline * technologyEffectiveness[tech.name]["SO2"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["SO2"] = min(SO2Baseline, totalReductions["SO2"] + techReductionSO2)

        techReductionNOx = NOxBaseline * technologyEffectiveness[tech.name]["NOx"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["NOx"] = min(NOxBaseline, totalReductions["NOx"] + techReductionNOx)
        
        techReductionVOC = VOCBaseline * technologyEffectiveness[tech.name]["VOC"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["VOC"] = min(VOCBaseline, totalReductions["VOC"] + techReductionVOC)
        
        techReductionCO2 = CO2Baseline * technologyEffectiveness[tech.name]["CO2"] * (tech.scalePercent / 100) * timeFactor
        totalReductions["CO2"] = min(CO2Baseline, totalReductions["CO2"] + techReductionCO2)
    
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
        summary = f"This {sector} scenario in {inputScenario.state} reduces " \
          f"SO2 by {totalReductions['SO2']} tons/year, " \
          f"NOx by {totalReductions['NOx']} tons/year, " \
          f"VOC by {totalReductions['VOC']} tons/year, and " \
          f"CO2 by {totalReductions['CO2']} tons/year."

    )
