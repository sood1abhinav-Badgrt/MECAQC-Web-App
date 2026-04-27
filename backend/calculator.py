from mock_data import *
from schema import *

def calculateAllScenarios(input: PlantInput) -> AllScenariosResult:
    if input.state not in SUPPORTED_STATES:
        raise ValueError(f"State '{input.state}' is not supported.")

    return AllScenariosResult(
        bau=calculateBAU(input),
        ac=calculateAC(input),
        gt=calculateGT(input),
        rt=calculateRT(input)
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
    om_rate = OM_COAL_FIXED_SMALL if input.capacity < 500 else OM_COAL_FIXED_LARGE
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
        netBenefits=NetBenefitOutput(
            totalBenefit=0.0,
            totalAnnualCost=tacBAU,
            netBenefit=-tacBAU
        )
    )


def calculateAC(input: PlantInput) -> ScenarioResult:
    if 50 <= input.capacity <= 100:
        scrubberType = "SDA"
        removalEfficiency = controlConstants["SO2"]["SDA"]["removalEfficiency"]
    else:
        scrubberType = "wetFGD"
        removalEfficiency = controlConstants["SO2"]["wetFGD"]["removalEfficiency"]

    heatRatePenalty = controlConstants["heatRatePenalty"]

    deltaEmissionsSO2  = input.baselineSO2  * removalEfficiency
    deltaEmissionsNOx  = -(input.baselineNOx  * heatRatePenalty)
    deltaEmissionsPM25 = -(input.baselinePM25 * heatRatePenalty)
    deltaEmissionsCO2  = -(input.baselineCO2  * heatRatePenalty)
    deltaEmissionsVOC  = 0.0 if scrubberType == "SDA" else -(input.baselineVOC * heatRatePenalty)

    reductions = ReductionOutput(
        SO2ChangePerYear=deltaEmissionsSO2,
        NOxChangePerYear=deltaEmissionsNOx,
        PM25ChangePerYear=deltaEmissionsPM25,
        VOCChangePerYear=deltaEmissionsVOC,
        CO2ChangePerYear=deltaEmissionsCO2
    )

    # TAC placeholder — EPA Control Cost Manual equations to be implemented
    costControl = 0.0
    tacAC = costControl + (HEAT_RATE_PENALTY * FUEL_COAL * input.heatInput)

    netBenefit = calculateNetBenefits(reductions, input.state, tacAC)
    totalBenefit = netBenefit + tacAC

    return ScenarioResult(
        scenario="AC",
        reductions=reductions,
        netBenefits=NetBenefitOutput(
            totalBenefit=totalBenefit,
            totalAnnualCost=tacAC,
            netBenefit=netBenefit
        )
    )


def calculateGT(input: PlantInput) -> ScenarioResult:
    ec = stateEnergyConstants[input.state]

    # S2.3 — replacement gas capacity (MW)
    capacityGT = input.annualGeneration / (ec["CF_NG"] * 8760)

    # S2.9 — emission reductions per pollutant (short tons/yr)
    er = gasConstants["emissionRates"]
    hr = gasConstants["heatRate"]
    deltaEmissionsSO2  = input.baselineSO2  - (input.annualGeneration * hr * er["SO2"])  / 2000
    deltaEmissionsNOx  = input.baselineNOx  - (input.annualGeneration * hr * er["NOx"])  / 2000
    deltaEmissionsPM25 = input.baselinePM25 - (input.annualGeneration * hr * er["PM25"]) / 2000
    deltaEmissionsVOC  = input.baselineVOC  - (input.annualGeneration * hr * er["VOC"])  / 2000
    deltaEmissionsCO2  = input.baselineCO2  - (input.annualGeneration * hr * er["CO2"])  / 2000

    reductions = ReductionOutput(
        SO2ChangePerYear=deltaEmissionsSO2,
        NOxChangePerYear=deltaEmissionsNOx,
        PM25ChangePerYear=deltaEmissionsPM25,
        VOCChangePerYear=deltaEmissionsVOC,
        CO2ChangePerYear=deltaEmissionsCO2
    )

    # S2.5 — incremental TAC (new system cost minus BAU)
    # Spreadsheet formulas (Uncontrolled_NG_Emissions, cols 53-55):
    #   Capex = CAP_NG * cost_aj_NG * capacityGT * 1000 * annualization
    #   O&M   = (OM_NG_FIXED * capacityGT * 1000 + OM_NG_VAR * annualGeneration) * cost_aj_NG
    #   Fuel  = FUEL_NG * heatRate * annualGeneration * cost_aj_NG
    tacBAU = calculateBAU(input).netBenefits.totalAnnualCost
    capex  = CAP_NG * ec["cost_aj_NG"] * capacityGT * 1000 * ANNUALIZATION
    om     = (OM_NG_FIXED * capacityGT * 1000 + OM_NG_VAR * input.annualGeneration) * ec["cost_aj_NG"]
    fuel   = FUEL_NG * hr * input.annualGeneration * ec["cost_aj_NG"]
    tacGT  = capex + om + fuel - tacBAU

    print(f"[GT] capacityGT: {capacityGT:.4f} MW")
    print(f"[GT] capex:      {capex:,.2f}  (target: 2,696,797)")
    print(f"[GT] om:         {om:,.2f}  (target: 895,144)")
    print(f"[GT] fuel:       {fuel:,.2f}  (target: 2,846,244)")
    print(f"[GT] tacBAU:     {tacBAU:,.2f}  (target: 22,474,283)")
    print(f"[GT] tacGT:      {tacGT:,.2f}  (target: -16,036,097)")

    netBenefit   = calculateNetBenefits(reductions, input.state, tacGT)
    totalBenefit = netBenefit + tacGT

    print(f"[GT] netBenefit: {netBenefit:,.2f}  (target: 52,294,614)")

    return ScenarioResult(
        scenario="GT",
        reductions=reductions,
        netBenefits=NetBenefitOutput(
            totalBenefit=totalBenefit,
            totalAnnualCost=tacGT,
            netBenefit=netBenefit
        )
    )


def calculateRT(input: PlantInput) -> ScenarioResult:
    ec = stateEnergyConstants[input.state]

    solarPct = ec["solarPct"]
    windPct  = ec["windPct"]
    totalPct = solarPct + windPct

    # S2.6, S2.7 — replacement capacity (MW)
    if totalPct == 0:
        capacitySolar = input.annualGeneration / (ec["CF_solar"] * 8760)
        capacityWind  = 0.0
    else:
        capacitySolar = input.annualGeneration * (solarPct / totalPct) / (ec["CF_solar"] * 8760)
        capacityWind  = input.annualGeneration * (windPct  / totalPct) / (ec["CF_wind"]  * 8760)

    tacBAU = calculateBAU(input).netBenefits.totalAnnualCost
    tacRT = (
        (CAP_SOLAR * ec["cost_aj_solar"] * capacitySolar * 1000
        + CAP_WIND * ec["cost_aj_wind"] * capacityWind * 1000) * ANNUALIZATION
        + (OM_SOLAR_FIXED * capacitySolar * 1000 + OM_WIND_FIXED * capacityWind * 1000)
        - tacBAU
    )

    # Renewables — 100% reduction of all pollutants
    reductions = ReductionOutput(
        SO2ChangePerYear=input.baselineSO2,
        NOxChangePerYear=input.baselineNOx,
        PM25ChangePerYear=input.baselinePM25,
        VOCChangePerYear=input.baselineVOC,
        CO2ChangePerYear=input.baselineCO2
    )

    netBenefit   = calculateNetBenefits(reductions, input.state, tacRT)
    totalBenefit = netBenefit + tacRT

    return ScenarioResult(
        scenario="RT",
        reductions=reductions,
        netBenefits=NetBenefitOutput(
            totalBenefit=totalBenefit,
            totalAnnualCost=tacRT,
            netBenefit=netBenefit
        )
    )