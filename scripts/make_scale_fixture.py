#!/usr/bin/env python3
import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SCALE_DIR = PROJECT_ROOT / "data" / "scale_test"
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"

def make_scale_fixture(replications=5):
    SCALE_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / "Plant_1_Generation_Data.csv"
    if not raw_path.exists():
        raw_path = FIXTURES_DIR / "generation_fixture.csv"

    print(f"[SCALE_FIXTURE] Generating synthetic scale test data ({replications}x replication)...")
    df = pd.read_csv(raw_path)

    dfs = []
    for i in range(replications):
        copy_df = df.copy()
        dfs.append(copy_df)

    scale_df = pd.concat(dfs, ignore_index=True)
    out_path = SCALE_DIR / f"SYNTHETIC_SCALE_TEST_Plant_1_Generation_{replications}x.csv"
    scale_df.to_csv(out_path, index=False)
    print(f"[SCALE_FIXTURE] Created {out_path.name} with {len(scale_df)} rows. (Labeled SYNTHETIC)")

if __name__ == "__main__":
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    make_scale_fixture(reps)
