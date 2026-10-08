import os
import pytest
import pandas as pd
from pathlib import Path

from ml.train import train_plant_model
from ml.registry import ModelRegistry

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEV_SAMPLE_DIR = PROJECT_ROOT / "data" / "dev_sample"
TEST_MODELS_DIR = PROJECT_ROOT / "state" / "e2e_models"

def test_e2e_dev_sample_pipeline():
    # 1. Verify dev sample files exist
    gen_files = list(DEV_SAMPLE_DIR.glob("*Generation*.csv"))
    weather_files = list(DEV_SAMPLE_DIR.glob("*Weather*.csv"))
    assert len(gen_files) > 0, "Dev sample generation CSV is missing."
    assert len(weather_files) > 0, "Dev sample weather CSV is missing."

    # 2. Read and prepare features locally
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
    joined["sin_time"] = pd.Series(0.0, index=joined.index)
    joined["cos_time"] = pd.Series(1.0, index=joined.index)

    # 3. Train plant model
    metrics = train_plant_model(joined, 4135001, TEST_MODELS_DIR)
    assert metrics["plant_id"] == 4135001
    assert "selected_model" in metrics

    # 4. Model Registry & Prediction serving test
    registry = ModelRegistry(TEST_MODELS_DIR)
    plants = registry.get_available_plants()
    assert 4135001 in plants

    pred_res = registry.predict(4135001, [
        {
            "timestamp": "2020-05-15 12:00:00",
            "IRRADIATION": 0.5,
            "AMBIENT_TEMPERATURE": 25.0,
            "MODULE_TEMPERATURE": 30.0,
            "minute_of_day": 720,
            "sin_time": 0.0,
            "cos_time": -1.0
        }
    ])
    assert pred_res["plant_id"] == 4135001
    assert len(pred_res["predictions"]) == 1
    assert pred_res["total_energy_kwh"] >= 0.0
