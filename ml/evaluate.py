import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, Any

def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, irradiation: np.ndarray = None) -> Dict[str, Any]:
    """Compute overall and daylight-only metrics (MAE, RMSE, R2)."""
    overall_mae = float(mean_absolute_error(y_true, y_pred))
    overall_rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    overall_r2 = float(r2_score(y_true, y_pred))
    
    metrics = {
        "overall": {
            "mae": round(overall_mae, 4),
            "rmse": round(overall_rmse, 4),
            "r2": round(overall_r2, 4),
            "sample_count": len(y_true)
        }
    }
    
    if irradiation is not None:
        daylight_mask = (irradiation > 0.001)
        if np.sum(daylight_mask) > 0:
            y_t_day = y_true[daylight_mask]
            y_p_day = y_pred[daylight_mask]
            
            daylight_mae = float(mean_absolute_error(y_t_day, y_p_day))
            daylight_rmse = float(np.sqrt(mean_squared_error(y_t_day, y_p_day)))
            daylight_r2 = float(r2_score(y_t_day, y_p_day)) if len(y_t_day) > 1 else 0.0
            
            metrics["daylight_only"] = {
                "mae": round(daylight_mae, 4),
                "rmse": round(daylight_rmse, 4),
                "r2": round(daylight_r2, 4),
                "sample_count": int(np.sum(daylight_mask))
            }
        else:
            metrics["daylight_only"] = {
                "mae": None, "rmse": None, "r2": None, "sample_count": 0
            }
            
    return metrics
