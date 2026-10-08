USE solar;

SELECT 
    plant_id,
    ROUND(FLOOR(IRRADIATION * 10) / 10.0, 1) AS irradiance_bin_start,
    COUNT(*) AS sample_count,
    ROUND(AVG(AC_POWER_KW), 2) AS avg_ac_power_kw,
    ROUND(CORR(IRRADIATION, AC_POWER_KW), 4) AS correlation_irradiance_ac
FROM solar.features
WHERE is_daylight = 1
GROUP BY plant_id, ROUND(FLOOR(IRRADIATION * 10) / 10.0, 1)
ORDER BY plant_id, irradiance_bin_start;
