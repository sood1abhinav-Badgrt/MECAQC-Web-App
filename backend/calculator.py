from mock_data import coalConstants, gasConstants, controlConstants, bptByState, SUPPORTED_STATES
from schemas import ReductionOutput, ScenarioResult, CostOutput, PlantInput, AllScenariosResult

def calculateAllScenarios(input: PlantInput) -> AllScenariosResult:
    if input.state not in SUPPORTED_STATES:
        raise ValueError(f"State '{input.state}' is not supported.")
    
    return AllScenariosResult(
        bau = calculateBAU(input),
        ac = calculateAC(input),
        gt = calculateGT(input),
        rt = calculateRT(input)
    )

def calculateNetBenefits(reductions: ReductionOutput, state: str, tac: float) -> float:
    bpt = bptByState[state]
    benefits = 0.0
    benefits += bpt["SO2"]  * reductions.SO2ChangePerYear
    benefits += bpt["NOx"]  * reductions.NOxChangePerYear
    benefits += bpt["PM25"] * reductions.PM25ChangePerYear
    benefits += bpt["VOC"]  * reductions.VOCChangePerYear
    benefits += bpt["SCC"]  * reductions.CO2ChangePerYear
    return benefits - tac

def calculateBAU(input: PlantInput) -> ScenarioResult:
    reductions = ReductionOutput(
        SO2ChangePerYear=0.0,
        NOxChangePerYear=0.0,
        PM25ChangePerYear=0.0,
        VOCChangePerYear=0.0,
        CO2ChangePerYear=0.0
    )

    tac = 0.0
    return ScenarioResult(
        scenario="BAU",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tac),
        netBenefits=0.0
    )

def calculateAC(input: PlantInput) -> ScenarioResult:
    # Auto-assign scrubber by capacity per Wu et al. 2024
    if 50 <= input.capacity <= 100:
        scrubberType = "SDA"
        removalEfficiency = controlConstants["SO2"]["SDA"]["removalEfficiency"]
    else:
        scrubberType = "wetFGD"
        removalEfficiency = controlConstants["SO2"]["wetFGD"]["removalEfficiency"]

    heatRatePenalty = controlConstants["heatRatePenalty"]

    # SO2 goes down — direct target of scrubber
    deltaEmissionsSO2 = input.baselineSO2 * removalEfficiency

    # Co-pollutants go up — heat rate penalty increases all other emissions
    deltaEmissionsNOx = -(input.baselineNOx * heatRatePenalty)
    deltaEmissionsPM25 = -(input.baselinePM25 * heatRatePenalty)
    deltaEmissionsCO2  = -(input.baselineCO2  * heatRatePenalty)


    if(scrubberType == "SDA"):
        deltaEmissionsVOC  = 0
    else: #ScrubberType is Wet FGD
        deltaEmissionsVOC  = -(input.baselineVOC  * heatRatePenalty)

    reductions = ReductionOutput(
        SO2ChangePerYear=deltaEmissionsSO2,
        NOxChangePerYear=deltaEmissionsNOx,
        PM25ChangePerYear=deltaEmissionsPM25,
        VOCChangePerYear=deltaEmissionsVOC,
        CO2ChangePerYear=deltaEmissionsCO2
    )

    tac = 0.0  # placeholder — EPA Control Cost Manual equations to be implemented
    
    return ScenarioResult(
        scenario="AC",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tac),
        netBenefits=calculateNetBenefits(reductions, input.state, tac)
    )

def calculateGT(input: PlantInput) -> ScenarioResult:
    hr  = gasConstants["heatRate"]
    er  = gasConstants["emissionRates"]

    # Delta = what coal emits minus what equivalent gas plant would emit
    # Positive = reduction, negative = increase
    reductions = ReductionOutput(
        SO2ChangePerYear  = input.baselineSO2  - (input.annualGeneration * hr * er["SO2"])  / 2000,
        NOxChangePerYear  = input.baselineNOx  - (input.annualGeneration * hr * er["NOx"])  / 2000,
        PM25ChangePerYear = input.baselinePM25 - (input.annualGeneration * hr * er["PM25"]) / 2000,
        VOCChangePerYear  = input.baselineVOC  - (input.annualGeneration * hr * er["VOC"])  / 2000,
        CO2ChangePerYear  = input.baselineCO2  - (input.annualGeneration * hr * er["CO2"])  / 2000
    )

    tac = 0.0  # placeholder — GT cost equations to be implemented
    
    return ScenarioResult(
        scenario="GT",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tac),
        netBenefits=calculateNetBenefits(reductions, input.state, tac)
    )

def calculateRT(input: PlantInput) -> ScenarioResult:
    # Renewables have zero operational emissions — 100% reduction of all pollutants
    reductions = ReductionOutput(
        SO2ChangePerYear=input.baselineSO2,
        NOxChangePerYear=input.baselineNOx,
        PM25ChangePerYear=input.baselinePM25,
        VOCChangePerYear=input.baselineVOC,
        CO2ChangePerYear=input.baselineCO2
    )

    tac = 0.0  # placeholder — RT cost equations to be implemented

    return ScenarioResult(
        scenario="RT",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tac),
        netBenefits=calculateNetBenefits(reductions, input.state, tac)
    )