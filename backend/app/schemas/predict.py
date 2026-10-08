from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PredictRowInput(BaseModel):
    timestamp: Optional[str] = None
    IRRADIATION: float
    AMBIENT_TEMPERATURE: float
    MODULE_TEMPERATURE: float
    minute_of_day: Optional[int] = None
    sin_time: Optional[float] = None
    cos_time: Optional[float] = None

class PredictRequest(BaseModel):
    plant_id: int
    rows: List[PredictRowInput]

class PredictionResultRow(BaseModel):
    index: int
    timestamp: Optional[str] = None
    predicted_kw: float

class PredictResponse(BaseModel):
    plant_id: int
    predictions: List[PredictionResultRow]
    total_energy_kwh: float
    disclaimer: str
