from pydantic import BaseModel

class PlantInput(BaseModel):
    state: str
    capacity: int           # MW
    annualGeneration: float # MWh
    heatInput: float        # MMBtu/yr
    baselineSO2: float      # tons/yr
    baselineNOx: float      # tons/yr
    baselinePM25: float     # tons/yr
    baselineVOC: float      # tons/yr
    baselineCO2: float      # tons/yr

class ReductionOutput(BaseModel):
    SO2ChangePerYear: float
    NOxChangePerYear: float
    PM25ChangePerYear: float
    VOCChangePerYear: float
    CO2ChangePerYear: float

class NetBenefitOutput(BaseModel):
    totalBenefit: float      # Σ(BPT × Δe)
    totalAnnualCost: float   # TAC
    netBenefit: float        # totalBenefit - totalAnnualCost

class ScenarioResult(BaseModel):
    scenario: str
    reductions: ReductionOutput
    netBenefits: NetBenefitOutput  # replaces both CostOutput and float

class AllScenariosResult(BaseModel):
    bau: ScenarioResult
    ac: ScenarioResult
    gt: ScenarioResult
    rt: ScenarioResult