from fastapi import FastAPI
from routes.scenarios import router as scenarioRouter

app = FastAPI()

@app.get("/health")
def health():
    return {"status" : "ok"}

app.include_router(scenarioRouter)