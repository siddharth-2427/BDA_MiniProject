from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class OverviewResponse(BaseModel):
    total_energy_kwh: float
    peak_power_kw: float
    total_rows_stored: int
    active_plants: List[int]
    best_model_r2: Optional[float] = None
    date_range: Optional[List[str]] = None

class AnalyticsQueryResponse(BaseModel):
    query_name: str
    headers: List[str]
    rows: List[List[Any]]
    execution_time_sec: float
