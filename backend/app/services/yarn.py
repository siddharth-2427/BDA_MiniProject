import httpx
from typing import List, Dict, Any
from app.core.config import settings

def get_yarn_applications() -> List[Dict[str, Any]]:
    url = f"http://{settings.YARN_RESOURCEMANAGER_HOST}:{settings.YARN_RESOURCEMANAGER_PORT}/ws/v1/cluster/apps"
    try:
        resp = httpx.get(url, timeout=3.0)
        if resp.status_code == 200:
            data = resp.json()
            apps = data.get("apps", {})
            if apps and "app" in apps:
                return apps["app"]
        return []
    except Exception:
        return []

def check_yarn_health() -> Dict[str, Any]:
    url = f"http://{settings.YARN_RESOURCEMANAGER_HOST}:{settings.YARN_RESOURCEMANAGER_PORT}/ws/v1/cluster/info"
    try:
        resp = httpx.get(url, timeout=3.0)
        if resp.status_code == 200:
            return {"status": "HEALTHY", "info": resp.json()}
        return {"status": "UNHEALTHY", "status_code": resp.status_code}
    except Exception as e:
        return {"status": "UNREACHABLE", "error": str(e)}
