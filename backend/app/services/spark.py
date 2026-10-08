import subprocess
from typing import Tuple, Optional

def submit_spark_job(script_path: str, args: list) -> Tuple[int, str, str, Optional[str]]:
    """Submit a PySpark job to YARN via spark-submit and capture logs and YARN app ID."""
    cmd = [
        "spark-submit",
        "--master", "yarn",
        "--deploy-mode", "client",
        script_path
    ] + args
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        yarn_app_id = None
        for line in proc.stderr.splitlines():
            if "Submitted application" in line or "impl.YarnClientImpl: Submitted application" in line:
                parts = line.split()
                for p in parts:
                    if p.startswith("application_"):
                        yarn_app_id = p
                        break
        return proc.returncode, proc.stdout, proc.stderr, yarn_app_id
    except Exception as e:
        return -1, "", str(e), None
