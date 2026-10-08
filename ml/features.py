import pandas as pd
import numpy as np
from typing import List, Tuple

FEATURE_COLUMNS = [
    "IRRADIATION",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "sin_time",
    "cos_time",
    "minute_of_day"
]

TARGET_COLUMN = "AC_POWER_KW"

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean feature input dataframe, ensuring required columns exist."""
    df = df.copy()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        
        # Calculate time features if missing
        if "minute_of_day" not in df.columns:
            df["minute_of_day"] = df["timestamp"].dt.hour * 60 + df["timestamp"].dt.minute
        if "sin_time" not in df.columns:
            df["sin_time"] = np.sin(df["minute_of_day"] * (2 * np.pi / 1440.0))
        if "cos_time" not in df.columns:
            df["cos_time"] = np.cos(df["minute_of_day"] * (2 * np.pi / 1440.0))
            
    # Check all feature columns are present
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
        
    return df
