#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEV_DIR = PROJECT_ROOT / "data" / "dev_sample"
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"

RAW_FILES = [
    "Plant_1_Generation_Data.csv",
    "Plant_1_Weather_Sensor_Data.csv",
    "Plant_2_Generation_Data.csv",
    "Plant_2_Weather_Sensor_Data.csv",
]

def make_dev_sample():
    DEV_DIR.mkdir(parents=True, exist_ok=True)
    raw_found = any((RAW_DIR / fname).exists() for fname in RAW_FILES)

    if raw_found:
        print("[DEV_SAMPLE] Slicing first 3 days from raw dataset files...")
        for fname in RAW_FILES:
            raw_path = RAW_DIR / fname
            if raw_path.exists():
                df = pd.read_csv(raw_path)
                # Take first 3 days (approx 3 * 24 * 4 = 288 rows per inverter/source)
                sample_df = df.head(1000).copy()
                out_path = DEV_DIR / f"DEV_SAMPLE_{fname}"
                sample_df.to_csv(out_path, index=False)
                print(f"  Created dev sample: {out_path.name} ({len(sample_df)} rows)")
    else:
        print("[DEV_SAMPLE] Raw data not found. Creating dev sample from test fixtures...")
        gen_fixture = FIXTURES_DIR / "generation_fixture.csv"
        weather_fixture = FIXTURES_DIR / "weather_fixture.csv"

        if gen_fixture.exists():
            shutil.copy(gen_fixture, DEV_DIR / "DEV_SAMPLE_Plant_1_Generation_Data.csv")
            shutil.copy(gen_fixture, DEV_DIR / "DEV_SAMPLE_Plant_2_Generation_Data.csv")
            print("  Copied generation test fixture to dev sample.")

        if weather_fixture.exists():
            shutil.copy(weather_fixture, DEV_DIR / "DEV_SAMPLE_Plant_1_Weather_Sensor_Data.csv")
            shutil.copy(weather_fixture, DEV_DIR / "DEV_SAMPLE_Plant_2_Weather_Sensor_Data.csv")
            print("  Copied weather test fixture to dev sample.")

if __name__ == "__main__":
    make_dev_sample()
