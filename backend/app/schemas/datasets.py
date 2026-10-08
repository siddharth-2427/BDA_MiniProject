from pydantic import BaseModel
from typing import List, Optional, Any

class ValidationResponse(BaseModel):
    valid: bool
    dataset_type: Optional[str] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    plant_ids: Optional[List[int]] = None
    errors: List[str] = []

class BatchStatusResponse(BaseModel):
    batch_id: str
    status: str
    created_at: str
    files: List[str]
    total_rows: int
