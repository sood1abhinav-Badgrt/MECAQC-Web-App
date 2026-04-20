from schema import PlantInput, AllScenariosResult
from fastapi import APIRouter
from calculator import calculateAllScenarios

router = APIRouter()
@router.post("/scenario/run", response_model=AllScenariosResult)
def runScenario(inputData: PlantInput):
    return calculateAllScenarios(inputData)