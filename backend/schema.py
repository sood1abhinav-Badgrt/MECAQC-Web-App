from pydantic import BaseModel
from typing import List

class TechnologyInput(BaseModel):
    name: str
    scalePercent: float 

class ScenarioInput(BaseModel):
    state: str
    sector: str
    technologies: List[TechnologyInput]
    timelineYears: int

class ReductionOutput(BaseModel):
    SO2TonsPerYear:float
    NOxTonsPerYear:float
    VOCTonsPerYear:float
    CO2TonsPerYear:float

class CostOutput(BaseModel):
    SO2: float
    NOx: float
    VOC: float
    CO2: float

class ScenarioResult(BaseModel):
    state: str
    sector: str
    timelineYears: int
    reductions: ReductionOutput
    costPerTon: CostOutput
    summary: str

