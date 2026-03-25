from schema import ScenarioInput, ScenarioResult, ReductionOutput, CostOutput
from fastapi import APIRouter

router = APIRouter()
@router.post("/scenario/run", response_model=ScenarioResult)
def runScenario(inputData: ScenarioInput):
    state = inputData.state
    sector = inputData.sector
    timelineYears = inputData.timelineYears

    reductions = ReductionOutput(
        SO2TonsPerYear = 4200,
        NOxTonsPerYear = 2800,
        VOCTonsPerYear = 640,
        CO2TonsPerYear = 9100000
    )

    cost = CostOutput(
        SO2 = 820,
        NOx = 1100,
        VOC = 950,
        CO2 = 42
    )

    summary = f"This scenario reduces {state} emissions significantly."

    return ScenarioResult(
        state = state,
        sector = sector,
        timelineYears = timelineYears,
        reductions = reductions,
        costPerTon = cost,
        summary = summary
    )