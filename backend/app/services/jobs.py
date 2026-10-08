import os
import json
import time
import uuid
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from app.core.config import settings

class JobManager:
    def __init__(self):
        self.state_dir = Path(settings.STATE_DIR) / "jobs"
        self.logs_dir = Path(settings.STATE_DIR) / "logs"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.active_job_id: Optional[str] = None
        self._lock = threading.Lock()

    def create_job(self, step_name: str) -> Dict[str, Any]:
        with self._lock:
            if self.active_job_id is not None:
                # Check if currently active job is actually running
                active_job = self.get_job(self.active_job_id)
                if active_job and active_job.get("status") == "RUNNING":
                    raise ValueError("A pipeline job is already in progress.")

            job_id = str(uuid.uuid4())[:8]
            self.active_job_id = job_id

            job_data = {
                "job_id": job_id,
                "step": step_name,
                "status": "RUNNING",
                "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "finished_at": None,
                "yarn_app_id": None,
                "error": None,
                "metrics": {}
            }
            self.save_job(job_data)
            return job_data

    def save_job(self, job_data: Dict[str, Any]):
        job_file = self.state_dir / f"{job_data['job_id']}.json"
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=2)

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        job_file = self.state_dir / f"{job_id}.json"
        if not job_file.exists():
            return None
        with open(job_file) as f:
            return json.load(f)

    def update_job_status(
        self,
        job_id: str,
        status: str,
        yarn_app_id: Optional[str] = None,
        error: Optional[str] = None,
        metrics: Optional[Dict[str, Any]] = None
    ):
        with self._lock:
            job = self.get_job(job_id)
            if job:
                job["status"] = status
                if yarn_app_id:
                    job["yarn_app_id"] = yarn_app_id
                if error:
                    job["error"] = error
                if metrics:
                    job["metrics"].update(metrics)
                if status in ["COMPLETED", "FAILED"]:
                    job["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    if self.active_job_id == job_id:
                        self.active_job_id = None
                self.save_job(job)

    def append_log(self, job_id: str, log_line: str):
        log_file = self.logs_dir / f"{job_id}.log"
        with open(log_file, "a") as f:
            f.write(f"{log_line}\n")

    def get_logs(self, job_id: str, tail: int = 50) -> List[str]:
        log_file = self.logs_dir / f"{job_id}.log"
        if not log_file.exists():
            return []
        with open(log_file) as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-tail:]]

job_manager = JobManager()
