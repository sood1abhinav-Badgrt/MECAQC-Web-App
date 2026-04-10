from pydantic import BaseModel
from typing import List


class ScenarioInput(BaseModel):
    state: str
    scenario: str
    coveragePercent: float
    timelineYears: int

class ReductionOutput(BaseModel):
    SO2TonsPerYear:float
    NOxTonsPerYear:float
    VOCTonsPerYear:float
    CO2TonsPerYear:float
    PMTonsPerYear:float

class CostOutput(BaseModel):
    totalAnnualCost: float


class ScenarioResult(BaseModel):
    state: str
    scenario: str
    timelineYears: int
    reductions: ReductionOutput
    cost: CostOutput
    netBenefits: float
    summary: str

