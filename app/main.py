from fastapi import FastAPI

app = FastAPI(
    title="Team Incident Tracker",
    description="Multi-tenant internal incident management tool",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Team Incident Tracker API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}