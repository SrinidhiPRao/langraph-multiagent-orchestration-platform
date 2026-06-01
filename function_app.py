import azure.functions as func
from api.routes import router
from api.websocket import router as websocket_router
from storage.db import init_db
from prometheus_client import generate_latest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

fastapi_app = FastAPI(title="Multi-Agent Workflow System")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
fastapi_app.include_router(router)
fastapi_app.include_router(websocket_router)


@fastapi_app.get("/")
def home():
    return {"message": "Workflow API Running"}


@fastapi_app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


app = func.AsgiFunctionApp(app=fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
