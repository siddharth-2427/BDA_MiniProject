import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from ml.features import FEATURE_COLUMNS, TARGET_COLUMN, prepare_features
from ml.evaluate import compute_metrics

class NaiveTimeOfDayModel:
    """Baseline model: predicts mean AC power by minute_of_day from training set."""
    def __init__(self):
        self.means = {}
        self.global_mean = 0.0

    def fit(self, X: pd.DataFrame, y: pd.Series):
        df = X.copy()
        df["target"] = y
        self.means = df.groupby("minute_of_day")["target"].mean().to_dict()
        self.global_mean = float(y.mean()) if len(y) > 0 else 0.0

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return np.array([self.means.get(m, self.global_mean) for m in X["minute_of_day"]])

def split_chronologically(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Split dataset chronologically by date: ~70% train, ~15% val, ~15% test."""
    df = df.sort_values("timestamp").reset_index(drop=True)
    n = len(df)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    split_info = {
        "train_range": [str(train_df["timestamp"].min()), str(train_df["timestamp"].max())],
        "val_range": [str(val_df["timestamp"].min()), str(val_df["timestamp"].max())],
        "test_range": [str(test_df["timestamp"].min()), str(test_df["timestamp"].max())],
        "train_rows": len(train_df),
        "val_rows": len(val_df),
        "test_rows": len(test_df)
    }
    return train_df, val_df, test_df, split_info

def train_plant_model(data_df: pd.DataFrame, plant_id: int, output_dir: Path) -> Dict[str, Any]:
    """Train candidate regression models for a plant, evaluate on val/test, and register artifacts."""
    plant_data = data_df[data_df["plant_id"] == plant_id].copy()
    if len(plant_data) < 20:
        raise ValueError(f"Insufficient data for plant_id {plant_id}: {len(plant_data)} rows.")

    plant_data = prepare_features(plant_data)
    train_df, val_df, test_df, split_info = split_chronologically(plant_data)

    X_train, y_train = train_df[FEATURE_COLUMNS], train_df[TARGET_COLUMN]
    X_val, y_val = val_df[FEATURE_COLUMNS], val_df[TARGET_COLUMN]
    X_test, y_test = test_df[FEATURE_COLUMNS], test_df[TARGET_COLUMN]

    candidates = {
        "NaiveBaseline": NaiveTimeOfDayModel(),
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=50, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=50, random_state=42)
    }

    val_scores = {}
    fitted_models = {}

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        fitted_models[name] = model
        
        preds_val = model.predict(X_val)
        val_metrics = compute_metrics(y_val.to_numpy(), preds_val, X_val["IRRADIATION"].to_numpy())
        val_scores[name] = val_metrics["overall"]["rmse"]

    # Select best model based on validation RMSE
    best_model_name = min(val_scores, key=val_scores.get)
    best_model = fitted_models[best_model_name]

    # Evaluate all candidate models on Test Set for performance table
    test_metrics = {}
    for name, model in fitted_models.items():
        preds_test = model.predict(X_test)
        test_metrics[name] = compute_metrics(y_test.to_numpy(), preds_test, X_test["IRRADIATION"].to_numpy())

    # Final best model test prediction & test evaluation
    best_test_preds = best_model.predict(X_test)
    
    # Save artifacts
    plant_out_dir = output_dir / str(plant_id)
    plant_out_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(best_model, plant_out_dir / "model.joblib")

    metrics_payload = {
        "plant_id": plant_id,
        "selected_model": best_model_name,
        "validation_rmse": val_scores,
        "test_metrics": test_metrics
    }

    with open(plant_out_dir / "metrics.json", "w") as f:
        json.dump(metrics_payload, f, indent=2)

    with open(plant_out_dir / "split_info.json", "w") as f:
        json.dump(split_info, f, indent=2)

    feature_schema = {
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "ranges": {
            col: {
                "min": float(X_train[col].min()),
                "max": float(X_train[col].max())
            } for col in FEATURE_COLUMNS
        }
    }
    with open(plant_out_dir / "feature_schema.json", "w") as f:
        json.dump(feature_schema, f, indent=2)

    test_preds_df = pd.DataFrame({
        "timestamp": test_df["timestamp"].astype(str),
        "actual_kw": y_test.values,
        "predicted_kw": best_test_preds,
        "irradiation": X_test["IRRADIATION"].values
    })
    test_preds_df.to_csv(plant_out_dir / "test_predictions.csv", index=False)

    print(f"[ML_TRAIN] Plant {plant_id} model trained successfully. Selected model: {best_model_name}")
    return metrics_payload
