from fastapi import FastAPI

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
