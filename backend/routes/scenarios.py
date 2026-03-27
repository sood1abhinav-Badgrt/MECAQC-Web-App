from schema import ScenarioInput, ScenarioResult, ReductionOutput, CostOutput
from fastapi import APIRouter, Body
from calculator import calculateScenario

router = APIRouter()
@router.post("/scenario/run", response_model=ScenarioResult)
def runScenario(inputData: ScenarioInput = Body()):
    return calculateScenario(inputData)