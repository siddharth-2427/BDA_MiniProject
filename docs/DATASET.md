# Dataset Documentation

## Primary Dataset Information
- **Source**: Kaggle "Solar Power Generation Data"
- **URL**: `https://www.kaggle.com/datasets/anikannal/solar-power-generation-data`
- **Licence**: CC0: Public Domain
- **Description**: Collected from two solar power plants in India over a period of 34 days (15-minute sampling interval).

## Expected Files
1. `Plant_1_Generation_Data.csv`
2. `Plant_1_Weather_Sensor_Data.csv`
3. `Plant_2_Generation_Data.csv`
4. `Plant_2_Weather_Sensor_Data.csv`

## Column Specifications
### Solar Generation Data
- `DATE_TIME`: Timestamp of observation.
- `PLANT_ID`: Unique plant identification number (e.g. 4135001, 4136001).
- `SOURCE_KEY`: Inverter ID key.
- `DC_POWER`: Direct current power generated (kW).
- `AC_POWER`: Alternating current power generated (kW).
- `DAILY_YIELD`: Cumulative daily energy yield (counter). Never sum directly!
- `TOTAL_YIELD`: Total cumulative energy yield (counter). Never sum directly!

### Weather Sensor Data
- `DATE_TIME`: Timestamp of observation.
- `PLANT_ID`: Unique plant identification number.
- `SOURCE_KEY`: Weather sensor key.
- `AMBIENT_TEMPERATURE`: Ambient air temperature (°C).
- `MODULE_TEMPERATURE`: Solar panel module temperature (°C).
- `IRRADIATION`: Solar irradiance (kW/m²).

> [!NOTE]
> The dataset does **not** include humidity, cloud cover, or wind speed columns. The pipeline and UI explicitly document this limitation.

## Known Data Quirks & Handling
- **Timestamp Formatting**: Generation timestamps use `dd-MM-yyyy HH:mm` or `yyyy-MM-dd HH:mm:ss`, while weather timestamps use `yyyy-MM-dd HH:mm:ss`. Explicit strict parsing handles both.
- **Inverter Gaps**: Missing timestamps and inverter outages are preserved without artificial interpolation.
- **Energy Calculation**: Total energy (kWh) = $\sum (\text{AC\_POWER in kW}) \times 0.25\text{ h}$.
