from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.schemas.predict import PredictRequest, PredictResponse
from ml.registry import ModelRegistry
from app.core.config import settings

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict_solar_generation(request: PredictRequest):
    registry = ModelRegistry(Path(settings.MODELS_DIR))
    try:
        input_rows = [row.dict() for row in request.rows]
        result = registry.predict(request.plant_id, input_rows)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
