from fastapi import APIRouter
from app.services.hdfs import check_hdfs_health
from app.services.yarn import check_yarn_health
from app.services.hive import check_hive_health
from app.services.ml import check_ml_health

router = APIRouter()

@router.get("/health")
def get_system_health():
    hdfs_res = check_hdfs_health()
    yarn_res = check_yarn_health()
    hive_res = check_hive_health()
    ml_res = check_ml_health()
    
    overall_healthy = (
        hdfs_res.get("status") == "HEALTHY" and
        yarn_res.get("status") == "HEALTHY"
    )
    
    return {
        "status": "HEALTHY" if overall_healthy else "DEGRADED",
        "components": {
            "hdfs": hdfs_res,
            "yarn": yarn_res,
            "hive": hive_res,
            "ml": ml_res
        }
    }
