USE solar;

SELECT 
    plant_id,
    COUNT(DISTINCT date_str) AS total_operational_days,
    ROUND(SUM(daily_energy_kwh), 2) AS total_generation_kwh,
    ROUND(MAX(peak_power_kw), 2) AS peak_recorded_kw,
    ROUND(AVG(daily_energy_kwh), 2) AS avg_daily_generation_kwh,
    ROUND(SUM(daily_energy_kwh) / (COUNT(DISTINCT date_str) * 24 * MAX(peak_power_kw)), 4) AS capacity_utilization_ratio
FROM solar.daily_energy
GROUP BY plant_id
ORDER BY plant_id;
