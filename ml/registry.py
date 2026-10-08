import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List

class ModelRegistry:
    def __init__(self, models_base_dir: Path):
        self.models_base_dir = models_base_dir

    def get_available_plants(self) -> List[int]:
        if not self.models_base_dir.exists():
            return []
        plants = []
        for p in self.models_base_dir.iterdir():
            if p.is_dir() and (p / "model.joblib").exists():
                try:
                    plants.append(int(p.name))
                except ValueError:
                    pass
        return sorted(plants)

    def load_plant_artifacts(self, plant_id: int) -> Dict[str, Any]:
        plant_dir = self.models_base_dir / str(plant_id)
        if not (plant_dir / "model.joblib").exists():
            raise FileNotFoundError(f"No trained model artifact found for plant {plant_id}.")

        model = joblib.load(plant_dir / "model.joblib")
        with open(plant_dir / "metrics.json") as f:
            metrics = json.load(f)
        with open(plant_dir / "feature_schema.json") as f:
            schema = json.load(f)
        with open(plant_dir / "split_info.json") as f:
            split_info = json.load(f)

        return {
            "model": model,
            "metrics": metrics,
            "schema": schema,
            "split_info": split_info,
            "plant_dir": plant_dir
        }

    def predict(self, plant_id: int, input_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        artifacts = self.load_plant_artifacts(plant_id)
        model = artifacts["model"]
        schema = artifacts["schema"]

        df = pd.DataFrame(input_rows)
        if "minute_of_day" not in df.columns and "timestamp" in df.columns:
            ts = pd.to_datetime(df["timestamp"])
            df["minute_of_day"] = ts.dt.hour * 60 + ts.dt.minute
        if "sin_time" not in df.columns:
            df["sin_time"] = np.sin(df["minute_of_day"] * (2 * np.pi / 1440.0))
        if "cos_time" not in df.columns:
            df["cos_time"] = np.cos(df["minute_of_day"] * (2 * np.pi / 1440.0))

        feature_cols = schema["feature_columns"]
        missing = [c for c in feature_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Input features missing required columns: {missing}")

        X = df[feature_cols]
        preds_kw = model.predict(X)
        preds_kw = np.clip(preds_kw, 0, None)  # Power cannot be negative

        total_kwh = float(np.sum(preds_kw) * 0.25)  # 15-minute interval kWh

        predictions = []
        for i, pred in enumerate(preds_kw):
            row_dict = {
                "index": i,
                "predicted_kw": round(float(pred), 2)
            }
            if "timestamp" in df.columns:
                row_dict["timestamp"] = str(df.iloc[i]["timestamp"])
            predictions.append(row_dict)

        return {
            "plant_id": plant_id,
            "predictions": predictions,
            "total_energy_kwh": round(total_kwh, 2),
            "disclaimer": "Predictions are weather-conditioned based on provided inputs; this is not a weather forecast."
        }
