import os
from pathlib import Path
from app.services.datasets import validate_dataset_csv

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "tests" / "fixtures"

def test_valid_generation_fixture():
    fixture_path = FIXTURES_DIR / "generation_fixture.csv"
    with open(fixture_path, "rb") as f:
        content = f.read()
    result = validate_dataset_csv(content, "generation_fixture.csv")
    assert result["valid"] is True
    assert result["dataset_type"] == "generation"
    assert result["row_count"] == 10
    assert len(result["errors"]) == 0

def test_valid_weather_fixture():
    fixture_path = FIXTURES_DIR / "weather_fixture.csv"
    with open(fixture_path, "rb") as f:
        content = f.read()
    result = validate_dataset_csv(content, "weather_fixture.csv")
    assert result["valid"] is True
    assert result["dataset_type"] == "weather"
    assert result["row_count"] == 5
    assert len(result["errors"]) == 0

def test_empty_file_rejected():
    result = validate_dataset_csv(b"", "empty.csv")
    assert result["valid"] is False
    assert "File is empty." in result["errors"]

def test_missing_column_rejected():
    bad_csv = b"DATE_TIME,PLANT_ID,SOURCE_KEY\n15-05-2020 06:00,4135001,KEY1\n"
    result = validate_dataset_csv(bad_csv, "missing_cols.csv")
    assert result["valid"] is False
    assert any("Unrecognized schema" in err for err in result["errors"])

def test_bad_timestamp_rejected():
    bad_ts_csv = (
        b"DATE_TIME,PLANT_ID,SOURCE_KEY,DC_POWER,AC_POWER,DAILY_YIELD,TOTAL_YIELD\n"
        b"INVALID_DATE,4135001,KEY1,0.0,0.0,0.0,1000.0\n"
    )
    result = validate_dataset_csv(bad_ts_csv, "bad_ts.csv")
    assert result["valid"] is False
    assert any("DATE_TIME format" in err for err in result["errors"])
