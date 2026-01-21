from fastapi import FastAPI

app = FastAPI(title="Incident Tracker")

@app.get("/health")
async def health():
    return {"status": "ok"}
