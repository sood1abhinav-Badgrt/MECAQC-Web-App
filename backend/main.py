from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.scenarios import router as scenarioRouter

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scenarioRouter)