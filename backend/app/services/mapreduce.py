import os
import subprocess
from typing import Tuple, Optional
from app.core.config import settings

def submit_mapreduce_job() -> Tuple[int, str, str, Optional[str]]:
    script_path = os.path.join(settings.PROJECT_ROOT, "mapreduce", "run_job.sh")
    try:
        proc = subprocess.run(["bash", script_path], capture_output=True, text=True, timeout=300)
        yarn_app_id = None
        for line in proc.stderr.splitlines() + proc.stdout.splitlines():
            if "Running job:" in line or "Submitted application" in line:
                parts = line.split()
                for p in parts:
                    if p.startswith("job_") or p.startswith("application_"):
                        yarn_app_id = p.replace("job_", "application_")
                        break
        return proc.returncode, proc.stdout, proc.stderr, yarn_app_id
    except Exception as e:
        return -1, "", str(e), None
