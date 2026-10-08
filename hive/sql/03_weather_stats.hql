USE solar;

SELECT 
    plant_id,
    ROUND(MIN(AMBIENT_TEMPERATURE), 2) AS min_ambient_temp,
    ROUND(AVG(AMBIENT_TEMPERATURE), 2) AS avg_ambient_temp,
    ROUND(MAX(AMBIENT_TEMPERATURE), 2) AS max_ambient_temp,
    ROUND(MIN(MODULE_TEMPERATURE), 2) AS min_module_temp,
    ROUND(AVG(MODULE_TEMPERATURE), 2) AS avg_module_temp,
    ROUND(MAX(MODULE_TEMPERATURE), 2) AS max_module_temp,
    ROUND(AVG(IRRADIATION), 4) AS avg_irradiation,
    ROUND(MAX(IRRADIATION), 4) AS max_irradiation
FROM solar.features
GROUP BY plant_id
ORDER BY plant_id;
