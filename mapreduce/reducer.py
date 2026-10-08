#!/usr/bin/env python3
import sys

current_key = None
total_ac_power = 0.0

# Reducer summing AC_POWER per key (plant_id|date) and converting to kWh (sum * 0.25)
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    
    key, val_str = parts
    try:
        ac_power = float(val_str)
    except ValueError:
        continue
    
    if current_key == key:
        total_ac_power += ac_power
    else:
        if current_key:
            daily_energy_kwh = total_ac_power * 0.25
            print(f"{current_key}\t{daily_energy_kwh:.4f}")
        current_key = key
        total_ac_power = ac_power

if current_key:
    daily_energy_kwh = total_ac_power * 0.25
    print(f"{current_key}\t{daily_energy_kwh:.4f}")
