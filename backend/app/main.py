from fastapi import FastAPI

from app.api.v1.endpoints.tasks import router as tasks_router

app = FastAPI(
    title="Project ATLAS API",
    description="Autonomous Task & Lifestyle AI System",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "project-atlas-api"}


@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {"message": "Welcome to Project ATLAS API", "version": "v1"}


app.include_router(tasks_router, prefix="/api/v1/tasks")
