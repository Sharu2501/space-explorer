from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.space_router import router

app = FastAPI(
    title="🚀 Space Explorer API",
    description="API DevOps - Données spatiales NASA (APOD + Astéroïdes)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/", summary="Health check")
async def root():
    return {"status": "ok", "message": "Space Explorer API is running 🚀"}
