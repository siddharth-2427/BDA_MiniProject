#!/usr/bin/env python3
import os
import sys
import zipfile
from pathlib import Path

DATA_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
KAGGLE_JSON   = Path.home() / ".kaggle" / "kaggle.json"      # legacy: username + key
KAGGLE_TOKEN  = Path.home() / ".kaggle" / "access_token"    # kaggle 2.x: KGAT_ token
DATASET_NAME = "anikannal/solar-power-generation-data"
EXPECTED_FILES = [
    "Plant_1_Generation_Data.csv",
    "Plant_1_Weather_Sensor_Data.csv",
    "Plant_2_Generation_Data.csv",
    "Plant_2_Weather_Sensor_Data.csv",
]

def main():
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if all files already exist
    all_exist = all((DATA_RAW_DIR / fname).exists() for fname in EXPECTED_FILES)
    if all_exist:
        print("[DATASET] All expected raw CSV files are already present in data/raw/:")
        for fname in EXPECTED_FILES:
            print(f"  - {fname}")
        return

    has_creds = KAGGLE_TOKEN.exists() or KAGGLE_JSON.exists()
    if has_creds:
        cred_path = KAGGLE_TOKEN if KAGGLE_TOKEN.exists() else KAGGLE_JSON
        print(f"[DATASET] Kaggle credentials found at {cred_path}. Downloading via Kaggle API...")
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            api.dataset_download_files(DATASET_NAME, path=str(DATA_RAW_DIR), unzip=True)
            print("[DATASET] Download and extraction complete.")
            return
        except Exception as e:
            print(f"[DATASET] Kaggle API download failed: {e}")
            print("[DATASET] Falling back to manual download instructions.")

    print("\n" + "="*70)
    print("MANUAL DATASET DOWNLOAD INSTRUCTIONS")
    print("="*70)
    print("1. Log in to Kaggle (https://www.kaggle.com).")
    print(f"2. Visit the dataset URL: https://www.kaggle.com/datasets/{DATASET_NAME}")
    print("3. Click 'Download' to download the ZIP file.")
    print("4. Extract the following 4 CSV files into your project's data/raw/ directory:")
    for fname in EXPECTED_FILES:
        print(f"   - {DATA_RAW_DIR / fname}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
