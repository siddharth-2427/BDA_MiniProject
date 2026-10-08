USE solar;

SELECT 
    plant_id,
    SUBSTR(date_str, 1, 7) AS year_month,
    COUNT(DISTINCT date_str) AS active_days,
    ROUND(SUM(daily_energy_kwh), 2) AS total_monthly_kwh,
    ROUND(AVG(daily_energy_kwh), 2) AS avg_daily_kwh
FROM solar.daily_energy
GROUP BY plant_id, SUBSTR(date_str, 1, 7)
ORDER BY plant_id, year_month;
