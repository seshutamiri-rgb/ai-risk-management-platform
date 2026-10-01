
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.routes.risk_routes import router as risk_router
from backend.app.routes.project_routes import router as project_router
from backend.app.routes.snowflake_routes import router as snowflake_router
from backend.app.routes.ai_risk_routes import router as ai_risk_router
from backend.app.routes.graph_routes import router as graph_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

# Allow the local frontend to communicate with FastAPI.
# These origins are for local development only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8082",  
        "http://127.0.0.1:8787",
        "http://localhost:8787",      
    ],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(risk_router)
app.include_router(project_router)
app.include_router(snowflake_router)
app.include_router(ai_risk_router)
app.include_router(graph_router)