import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.datasets import validate_dataset_csv
from app.schemas.datasets import ValidationResponse
from app.core.config import settings
from app.services.hdfs import run_hdfs_cmd

router = APIRouter()

@router.post("/datasets/validate", response_model=ValidationResponse)
async def validate_dataset(file: UploadFile = File(...)):
    content = await file.read()
    result = validate_dataset_csv(content, file.filename)
    return result

@router.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):
    content = await file.read()
    val_res = validate_dataset_csv(content, file.filename)
    if not val_res["valid"]:
        raise HTTPException(status_code=400, detail={"message": "Invalid dataset CSV", "errors": val_res["errors"]})
    
    batch_id = str(uuid.uuid4())[:8]
    dataset_type = val_res["dataset_type"]
    plant_ids = val_res.get("plant_ids", [4135001])
    plant_id = plant_ids[0] if plant_ids else 4135001
    
    # Save locally to raw data folder first
    local_raw_path = Path(settings.DATA_DIR) / "raw" / f"UPLOAD_{batch_id}_{file.filename}"
    local_raw_path.parent.mkdir(parents=True, exist_ok=True)
    with open(local_raw_path, "wb") as f:
        f.write(content)
        
    # Stage under HDFS /solar/raw/<dataset_type>/plant_id=<plant_id>/<batch_id>/
    hdfs_dest = f"/solar/raw/{dataset_type}/plant_id={plant_id}/{batch_id}/{file.filename}"
    run_hdfs_cmd(["-mkdir", "-p", f"/solar/raw/{dataset_type}/plant_id={plant_id}/{batch_id}"])
    code, stdout, stderr = run_hdfs_cmd(["-put", "-f", str(local_raw_path), hdfs_dest])
    
    return {
        "status": "SUCCESS",
        "batch_id": batch_id,
        "dataset_type": dataset_type,
        "plant_id": plant_id,
        "local_path": str(local_raw_path),
        "hdfs_path": hdfs_dest,
        "rows": val_res["row_count"]
    }

@router.get("/datasets")
def list_datasets():
    raw_dir = Path(settings.DATA_DIR) / "raw"
    files_list = []
    if raw_dir.exists():
        for f in raw_dir.glob("*.csv"):
            files_list.append({
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "modified": f.stat().st_mtime
            })
    return {"raw_datasets": files_list}
