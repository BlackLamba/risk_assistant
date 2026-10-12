
from fastapi import FastAPI
from app.schemas import ProjectInput, RiskAssessment
from app.risk_engine import assess_project

app = FastAPI(
    title="AI Project Risk Assistant",
    description="Прототип поддержки решений при управлении IT-проектами",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Risk Assistant",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/assess", response_model=RiskAssessment)
def assess(project: ProjectInput):
    return assess_project(project)
