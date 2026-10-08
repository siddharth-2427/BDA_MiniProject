import io
import pandas as pd
from typing import Dict, Any, Tuple, List

GENERATION_COLUMNS = {
    "DATE_TIME", "PLANT_ID", "SOURCE_KEY", "DC_POWER", "AC_POWER", "DAILY_YIELD", "TOTAL_YIELD"
}

WEATHER_COLUMNS = {
    "DATE_TIME", "PLANT_ID", "SOURCE_KEY", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"
}

SUPPORTED_DATE_FORMATS = [
    "%d-%m-%Y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S"
]

def parse_timestamps(series: pd.Series) -> Tuple[pd.Series, int]:
    """Parse timestamps across supported formats. Return parsed series and unparseable count."""
    parsed = pd.to_datetime(series, format="%d-%m-%Y %H:%M", errors="coerce")
    for fmt in SUPPORTED_DATE_FORMATS[1:]:
        null_mask = parsed.isna()
        if not null_mask.any():
            break
        parsed.loc[null_mask] = pd.to_datetime(series[null_mask], format=fmt, errors="coerce")
    
    unparseable_count = int(parsed.isna().sum())
    return parsed, unparseable_count

def validate_dataset_csv(content_bytes: bytes, file_name: str = "") -> Dict[str, Any]:
    """Validate uploaded CSV dataset against schema, timestamp, and numeric requirements."""
    errors: List[str] = []
    
    if not content_bytes or len(content_bytes.strip()) == 0:
        return {"valid": False, "errors": ["File is empty."]}
    
    try:
        df = pd.read_csv(io.BytesIO(content_bytes))
    except Exception as e:
        return {"valid": False, "errors": [f"Invalid CSV format: {str(e)}"]}
    
    if df.empty:
        return {"valid": False, "errors": ["CSV file contains no rows."]}
    
    cols = set(df.columns.str.strip())
    
    # Determine dataset type
    is_gen = GENERATION_COLUMNS.issubset(cols)
    is_weather = WEATHER_COLUMNS.issubset(cols)
    
    if not is_gen and not is_weather:
        missing_gen = list(GENERATION_COLUMNS - cols)
        missing_weather = list(WEATHER_COLUMNS - cols)
        errors.append(
            f"Unrecognized schema. Missing generation columns: {missing_gen} OR missing weather columns: {missing_weather}"
        )
        return {"valid": False, "errors": errors}
    
    dataset_type = "generation" if is_gen else "weather"
    
    # Timestamp validation
    _, unparseable = parse_timestamps(df["DATE_TIME"])
    if unparseable > 0:
        errors.append(f"Failed to parse DATE_TIME format for {unparseable} rows.")
    
    # Numeric column validations
    numeric_cols = (
        ["DC_POWER", "AC_POWER", "DAILY_YIELD", "TOTAL_YIELD"]
        if dataset_type == "generation"
        else ["AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "IRRADIATION"]
    )
    
    for col in numeric_cols:
        non_numeric = pd.to_numeric(df[col], errors="coerce").isna().sum()
        if non_numeric > 0:
            errors.append(f"Column '{col}' has {non_numeric} invalid non-numeric or missing values.")
            
    if errors:
        return {"valid": False, "dataset_type": dataset_type, "errors": errors}
    
    return {
        "valid": True,
        "dataset_type": dataset_type,
        "row_count": len(df),
        "column_count": len(df.columns),
        "plant_ids": [int(x) for x in df["PLANT_ID"].unique() if pd.notna(x)],
        "errors": []
    }
