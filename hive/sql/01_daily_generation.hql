USE solar;

SELECT 
    plant_id,
    date_str,
    ROUND(daily_energy_kwh, 2) AS daily_energy_kwh,
    ROUND(peak_power_kw, 2) AS peak_power_kw
FROM solar.daily_energy
ORDER BY plant_id, date_str;
