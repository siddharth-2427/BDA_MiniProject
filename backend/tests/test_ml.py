import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from ml.evaluate import compute_metrics
from ml.features import prepare_features
from ml.train import train_plant_model
from ml.registry import ModelRegistry

def test_compute_metrics():
    y_true = np.array([10.0, 20.0, 30.0, 0.0])
    y_pred = np.array([12.0, 18.0, 31.0, 0.0])
    irr = np.array([0.5, 0.8, 0.9, 0.0])
    
    metrics = compute_metrics(y_true, y_pred, irr)
    assert "overall" in metrics
    assert "daylight_only" in metrics
    assert metrics["overall"]["sample_count"] == 4
    assert metrics["daylight_only"]["sample_count"] == 3
    assert metrics["overall"]["r2"] > 0.9

def test_ml_train_and_predict_flow(tmp_path):
    # Generate synthetic training dataframe
    timestamps = pd.date_range("2020-05-15 00:00", periods=100, freq="15min")
    irr = np.where((timestamps.hour >= 6) & (timestamps.hour <= 18), 0.8, 0.0)
    ac_power = irr * 500.0 + np.random.normal(0, 10, size=100)
    ac_power = np.clip(ac_power, 0, None)
    
    df = pd.DataFrame({
        "timestamp": timestamps,
        "plant_id": 4135001,
        "IRRADIATION": irr,
        "AMBIENT_TEMPERATURE": 25.0,
        "MODULE_TEMPERATURE": 30.0,
        "AC_POWER_KW": ac_power,
        "minute_of_day": timestamps.hour * 60 + timestamps.minute,
        "sin_time": np.sin((timestamps.hour * 60 + timestamps.minute) * (2 * np.pi / 1440.0)),
        "cos_time": np.cos((timestamps.hour * 60 + timestamps.minute) * (2 * np.pi / 1440.0))
    })
    
    result = train_plant_model(df, 4135001, tmp_path)
    assert result["plant_id"] == 4135001
    assert "selected_model" in result
    
    registry = ModelRegistry(tmp_path)
    plants = registry.get_available_plants()
    assert 4135001 in plants
    
    pred_input = [
        {
            "timestamp": "2020-05-16 12:00:00",
            "IRRADIATION": 0.85,
            "AMBIENT_TEMPERATURE": 26.0,
            "MODULE_TEMPERATURE": 35.0,
            "minute_of_day": 720,
            "sin_time": 0.0,
            "cos_time": -1.0
        }
    ]
    res = registry.predict(4135001, pred_input)
    assert res["plant_id"] == 4135001
    assert len(res["predictions"]) == 1
    assert res["total_energy_kwh"] >= 0.0
