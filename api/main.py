from fastapi import FastAPI
from api.routes import router
from storage.db import init_db
from api.websocket import router as websocket_router
from prometheus_client import generate_latest
from fastapi.responses import Response

app = FastAPI(
    title="Multi-Agent Workflow System"
)

init_db()

app.include_router(router)

app.include_router(websocket_router)

@app.get("/")
def home():

    return {
        "message": "Workflow API Running"
    }

@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )