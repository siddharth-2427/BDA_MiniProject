import io
import csv
import subprocess
import time
from typing import Dict, Any, List
from app.core.config import settings

def execute_beeline_query(query_sql: str) -> Dict[str, Any]:
    start_time = time.time()
    jdbc_url = f"jdbc:hive2://{settings.HIVE_SERVER2_HOST}:{settings.HIVE_SERVER2_PORT}/solar"
    cmd = [
        "beeline",
        "-u", jdbc_url,
        "--outputformat=csv2",
        "--silent=true",
        "-e", query_sql
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        elapsed = time.time() - start_time
        if proc.returncode != 0:
            return {
                "headers": [], "rows": [],
                "execution_time_sec": elapsed,
                "error": proc.stderr
            }
        
        # Parse CSV output
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        if not lines:
            return {"headers": [], "rows": [], "execution_time_sec": elapsed}
        
        reader = csv.reader(lines)
        headers = next(reader, [])
        rows = list(reader)
        
        return {
            "headers": headers,
            "rows": rows,
            "execution_time_sec": round(elapsed, 2),
            "error": None
        }
    except Exception as e:
        return {
            "headers": [], "rows": [],
            "execution_time_sec": round(time.time() - start_time, 2),
            "error": str(e)
        }

def check_hive_health() -> Dict[str, Any]:
    res = execute_beeline_query("SHOW TABLES IN solar;")
    if res.get("error") is None:
        return {"status": "HEALTHY", "tables": res.get("rows", [])}
    return {"status": "UNHEALTHY", "error": res.get("error")}
