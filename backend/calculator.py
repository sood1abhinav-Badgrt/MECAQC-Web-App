from mock_data import coalConstants, gasConstants, controlConstants, bptByState, SUPPORTED_STATES, OM_COAL_FIXED, FUEL_COAL, CAP_SCRUBBER, ANNUALIZATION, OM_SCRUBBER_FIXED
from schema import PlantInput, ReductionOutput, NetBenefitOutput, ScenarioResult, AllScenariosResult

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

    #Calculating the cost for the business as usual approach
    tacBAU = 0.0

    om_rate = 0.0
    if(input.capacity < 500):
        om_rate = OM_COAL_FIXED_SMALL
    else:
        om_rate = OM_COAL_FIXED_LARGE

    om_cost = (om_rate * input.capacity * 1000) + (OM_COAL_VAR * input.annualGeneration)   
    fuelCost = FUEL_COAL * input.heatInput
    tacBAU = om_cost + fuelCost     

    reductions = ReductionOutput(
        SO2ChangePerYear=0.0,
        NOxChangePerYear=0.0,
        PM25ChangePerYear=0.0,
        VOCChangePerYear=0.0,
        CO2ChangePerYear=0.0
    )

    return ScenarioResult(
        scenario="BAU",
        reductions=reductions,
        netBenefits = NetBenefitOutput(
            totalBenefit = 0.0,
            totalAnnualCost = tacBAU, 
            netBenefit = -tacBAU
        )
    )

def calculateAC(input: PlantInput) -> ScenarioResult:
    
    # Auto-assign scrubber by capacity per Wu et al. 2024
    if 50 <= input.capacity <= 100:
        scrubberType = "SDA"
        removalEfficiency = controlConstants["SO2"]["SDA"]["removalEfficiency"] #.95
    else:
        scrubberType = "wetFGD"
        removalEfficiency = controlConstants["SO2"]["wetFGD"]["removalEfficiency"] #.98
  

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

    tacAC = 0.0  # placeholder — EPA Control Cost Manual equations to be implemented
    costControl = 0.0 # still needs to be implemented
    tacAC = costControl + (HEAT_RATE_PENALTY * FUEL_COAL * input.heatInput)

    
    return ScenarioResult(
        scenario="AC",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tacAC),
        netBenefits=calculateNetBenefits(reductions, input.state, tacAC)
    )

def calculateGT(input: PlantInput) -> ScenarioResult:
    ec = stateEnergyConstants[input.state]

    # S2.3 — replacement gas capacity (MW)
    capacityGT = input.annualGeneration / (ec["CF_NG"] * 8760)

    # S2.4 — gas heat input (MMBtu/yr)
    heatInputNG = gasConstants["heatRate"] * input.annualGeneration



    # S2.9 — emission reductions (short tons/yr)
    # Δe = ecoal - (annualGeneration × HR_NG × ER_NG) / 2000
    # emissions by coal - (annual generation * heatrate of natural gas and emissions rate of natural gas) / 2000
    deltaEmissionsSO2 = input.baselineSO2 - (input.annualGeneration * gasConstants["heatRate"] * emissionRates["heatRate"]) / 2000
    deltaEmissionsNOx = input.baselineNOx - (input.annualGeneration * gasConstants["heatRate"] * emissionRates["heatRate"]) / 2000
    deltaEmissionsPM25 = input.baselinePM25 - (input.annualGeneration * gasConstants["heatRate"] * emissionRates["heatRate"]) / 2000
    deltaEmissionsVOC = input.baselineVOC - (input.annualGeneration * gasConstants["heatRate"] * emissionRates["heatRate"]) / 2000
    deltaEmissionsCO2 = input.baselineCO2 - (input.annualGeneration * gasConstants["heatRate"] * emissionRates["heatRate"]) / 2000

    reductions = ReductionOutput(
        SO2ChangePerYear = deltaEmissionsSO2
        NOxChangePerYear = deltaEmissionsNOx
        PM25ChangePerYear = deltaEmissionsPM25
        VOCChangePerYear = deltaEmissionsVOC
        CO2ChangePerYear = deltaEmissionsCO2
    )

    # S2.11 — methane leak CO2 offset (short tons)
    co2_offset = (
        (heatInput_ng / NG_HEAT_CONTENT)
        * METHANE_DENSITY
        / 1000
        * METHANE_LEAK_RATE
        * CH4_GWP_20YR
        * 1.1023                     # metric tons → short tons
    )

    # S2.12 — dollar value of methane offset
    methane_penalty = co2_offset * SCC_CO2  

    # S2.5 — incremental TAC
    tacGT = (
        (CAP_NG * ec["cost_aj_NG"] * capacity_gt * 1000 * ANNUALIZATION)
        + (OM_NG_FIXED * ec["cost_aj_NG"] * capacity_gt * 1000)
        + (OM_NG_VAR * input.annualGeneration)
        + (FUEL_NG * heatInput_ng)
        - tacBAU
    )
    
    return ScenarioResult(
        scenario="GT",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tacGT),
        netBenefits=calculateNetBenefits(reductions, input.state, tacGT)
    )

def calculateRT(input: PlantInput) -> ScenarioResult:
    ec = = stateEnergyConstants[input.state]
    solarPCT = ec["SolarPct"]
    windPCT = ec["windPct"]
    totalPCT = solarPCT + windPCT

    # S2.6, S2.7 — replacement capacity (MW)
    # edge case: AL, AR, KY, LA, MS have windPct = 0 → 100% solar
    if total_pct == 0:
        capacity_solar = input.annualGeneration / (ec["CF_solar"] * 8760)
        capacity_wind  = 0.0
    else:
        capacity_solar = input.annualGeneration * (solar_pct / total_pct) / (ec["CF_solar"] * 8760)
        capacity_wind  = input.annualGeneration * (wind_pct  / total_pct) / (ec["CF_wind"]  * 8760)

    tacRT = (
        (CAP_SOLAR * ec["cost_aj_solar"] * capacity_solar * 1000
        + CAP_WIND * ec["cost_aj_wind"] * capacity_wind  * 1000) * ANNUALIZATION
        + (OM_SOLAR_FIXED * capacity_solar * 1000 + OM_WIND_FIXED * capacity_wind * 1000)
        - tacBAU
    )


    # Renewables have zero operational emissions — 100% reduction of all pollutants
    reductions = ReductionOutput(
        SO2ChangePerYear=input.baselineSO2,
        NOxChangePerYear=input.baselineNOx,
        PM25ChangePerYear=input.baselinePM25,
        VOCChangePerYear=input.baselineVOC,
        CO2ChangePerYear=input.baselineCO2
    )

    tacRT = (
        (CAP_SOLAR * ec["cost_aj_solar"] * capacity_solar * 1000
        + CAP_WIND * ec["cost_aj_wind"] * capacity_wind  * 1000) * ANNUALIZATION
        + (OM_SOLAR_FIXED * capacity_solar * 1000 + OM_WIND_FIXED * capacity_wind * 1000)
        - tacBAU
    )

    return ScenarioResult(
        scenario="RT",
        reductions=reductions,
        cost=CostOutput(totalAnnualCost=tacRT),
        netBenefits=calculateNetBenefits(reductions, input.state, tacRT)
    )