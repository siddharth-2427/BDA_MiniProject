from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PipelineRunRequest(BaseModel):
    steps: Optional[List[str]] = None
    plant_ids: Optional[List[int]] = None

class JobResponse(BaseModel):
    job_id: str
    status: str  # PENDING, RUNNING, COMPLETED, FAILED
    step: str
    started_at: str
    finished_at: Optional[str] = None
    yarn_app_id: Optional[str] = None
    error: Optional[str] = None
    logs: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None

class PipelineStatusResponse(BaseModel):
    active_job_id: Optional[str] = None
    is_running: bool
    yarn_apps: List[Dict[str, Any]] = []
    completed_jobs: List[str] = []
