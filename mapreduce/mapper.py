#!/usr/bin/env python3
import sys

# Mapper reading raw generation CSV lines from standard input
# Header: DATE_TIME,PLANT_ID,SOURCE_KEY,DC_POWER,AC_POWER,DAILY_YIELD,TOTAL_YIELD
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("DATE_TIME"):
        continue
    
    parts = line.split(",")
    if len(parts) >= 5:
        date_time_str = parts[0].strip()
        plant_id = parts[1].strip()
        ac_power_str = parts[4].strip()
        
        # Extract YYYY-MM-DD or DD-MM-YYYY date portion
        date_part = date_time_str.split(" ")[0]
        # Standardize date format to YYYY-MM-DD if in DD-MM-YYYY format
        if "-" in date_part and len(date_part.split("-")[0]) == 2:
            d, m, y = date_part.split("-")
            date_part = f"{y}-{m}-{d}"
        
        try:
            ac_power = float(ac_power_str)
            print(f"{plant_id}|{date_part}\t{ac_power}")
        except ValueError:
            continue
