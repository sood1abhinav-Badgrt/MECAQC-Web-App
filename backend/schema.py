from pydantic import BaseModel
from typing import List

class PlantInput(BaseModel):
    state: str
    capacity: int #MW
    annualGeneration: float #MWh
    baselineSO2: float #tons/yr emissions
    baselineNOx: float #tons/yr emissions
    baselinePM25: float #tons/yr emissions
    baselineVOC: float #tons/yr emissions
    baselineCO2: float #tons/yr emissions

class ReductionOutput(BaseModel):
    SO2ChangePerYear: float
    NOxChangePerYear: float
    PM25ChangePerYear: float
    VOCChangePerYear: float
    CO2ChangePerYear: float

class CostOutput(BaseModel):
    totalAnnualCost: float

class ScenarioResult(BaseModel):
    scenario: str
    reductions: ReductionOutput
    cost: CostOutput
    netBenefits: float

class AllScenariosResult(BaseModel):
    bau: ScenarioResult
    ac: ScenarioResult
    gt: ScenarioResult
    rt: ScenarioResult

