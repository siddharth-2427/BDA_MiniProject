from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ModelMetricsResponse(BaseModel):
    plant_id: int
    selected_model: str
    validation_rmse: Dict[str, float]
    test_metrics: Dict[str, Any]
    split_info: Dict[str, Any]

class TestPredictionsResponse(BaseModel):
    plant_id: int
    columns: List[str]
    rows: List[Dict[str, Any]]
