import subprocess
from typing import List, Dict, Any
from app.core.config import settings

def run_hdfs_cmd(args: List[str]) -> tuple[int, str, str]:
    cmd = ["hdfs", "dfs"] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return -1, "", str(e)

def check_hdfs_health() -> Dict[str, Any]:
    cmd = ["hdfs", "dfsadmin", "-report"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            return {"status": "HEALTHY", "output": proc.stdout[:500]}
        return {"status": "UNHEALTHY", "error": proc.stderr}
    except Exception as e:
        return {"status": "UNREACHABLE", "error": str(e)}

def list_hdfs_dir(path: str = "/solar") -> List[Dict[str, Any]]:
    code, stdout, stderr = run_hdfs_cmd(["-ls", "-R", path])
    if code != 0:
        return []
    
    files = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("Found"):
            continue
        parts = line.split(maxsplit=7)
        if len(parts) >= 8:
            files.append({
                "permissions": parts[0],
                "replication": parts[1],
                "owner": parts[2],
                "group": parts[3],
                "size_bytes": int(parts[4]) if parts[4].isdigit() else 0,
                "modified": f"{parts[5]} {parts[6]}",
                "path": parts[7]
            })
    return files
