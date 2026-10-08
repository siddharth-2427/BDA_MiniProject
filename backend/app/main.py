import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import health, datasets, pipeline, analytics, models, predict

setup_logging()

app = FastAPI(
    title="Renewable Energy Generation Prediction API",
    description="Big Data weather analytics & solar generation predictive service.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local dev frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router inclusions
app.include_router(health.router, tags=["Health"])
app.include_router(datasets.router, tags=["Datasets"])
app.include_router(pipeline.router, tags=["Pipeline"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(models.router, tags=["Models"])
app.include_router(predict.router, tags=["Predict"])

@app.get("/")
def root():
    return {
        "service": "Solar Power Generation Prediction API",
        "status": "ONLINE",
        "documentation": "/docs"
    }
