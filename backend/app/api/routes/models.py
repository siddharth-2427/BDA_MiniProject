import json
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException
from ml.registry import ModelRegistry
from ml.train import train_plant_model
from app.core.config import settings

router = APIRouter()

@router.get("/models")
def list_trained_models():
    registry = ModelRegistry(Path(settings.MODELS_DIR))
    plants = registry.get_available_plants()
    return {"trained_plants": plants}

@router.get("/models/{plant_id}/metrics")
def get_model_metrics(plant_id: int):
    registry = ModelRegistry(Path(settings.MODELS_DIR))
    try:
        artifacts = registry.load_plant_artifacts(plant_id)
        return {
            "plant_id": plant_id,
            "metrics": artifacts["metrics"],
            "split_info": artifacts["split_info"],
            "feature_schema": artifacts["schema"]
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/models/{plant_id}/test-predictions")
def get_test_predictions(plant_id: int):
    plant_dir = Path(settings.MODELS_DIR) / str(plant_id)
    preds_file = plant_dir / "test_predictions.csv"
    if not preds_file.exists():
        raise HTTPException(status_code=404, detail=f"No test predictions found for plant {plant_id}.")
    
    df = pd.read_csv(preds_file)
    return {
        "plant_id": plant_id,
        "total_rows": len(df),
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records")
    }

@router.post("/models/train")
def trigger_model_retraining(plant_id: int = 4135001):
    dev_sample_dir = Path(settings.DATA_DIR) / "dev_sample"
    gen_files = list(dev_sample_dir.glob("*Generation*.csv"))
    weather_files = list(dev_sample_dir.glob("*Weather*.csv"))
    
    if not gen_files or not weather_files:
        raise HTTPException(status_code=400, detail="No feature dataset available to train models.")
        
    gen_df = pd.read_csv(gen_files[0])
    weather_df = pd.read_csv(weather_files[0])
    
    gen_df["timestamp"] = pd.to_datetime(gen_df["DATE_TIME"], errors="coerce")
    weather_df["timestamp"] = pd.to_datetime(weather_df["DATE_TIME"], errors="coerce")
    
    gen_plant = gen_df.groupby(["PLANT_ID", "timestamp"])["AC_POWER"].sum().reset_index()
    gen_plant.rename(columns={"AC_POWER": "AC_POWER_KW", "PLANT_ID": "plant_id"}, inplace=True)
    
    weather_plant = weather_df.groupby(["PLANT_ID", "timestamp"]).agg({
        "IRRADIATION": "mean",
        "AMBIENT_TEMPERATURE": "mean",
        "MODULE_TEMPERATURE": "mean"
    }).reset_index()
    weather_plant.rename(columns={"PLANT_ID": "plant_id"}, inplace=True)
    
    joined = pd.merge(gen_plant, weather_plant, on=["plant_id", "timestamp"], how="inner")
    joined["minute_of_day"] = joined["timestamp"].dt.hour * 60 + joined["timestamp"].dt.minute
    joined["sin_time"] = np.sin(joined["minute_of_day"] * (2 * np.pi / 1440.0))
    joined["cos_time"] = np.cos(joined["minute_of_day"] * (2 * np.pi / 1440.0))
    
    metrics = train_plant_model(joined, plant_id, Path(settings.MODELS_DIR))
    return {"status": "SUCCESS", "plant_id": plant_id, "metrics": metrics}
