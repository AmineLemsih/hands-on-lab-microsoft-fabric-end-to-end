-- Q1 : consommation électrique observée pendant l'année civile 2025, en kWh.
SELECT ROUND(SUM(kwh_elec), 2) AS electricity_kwh
FROM dbo.consumption
WHERE [date] >= '2025-01-01' AND [date] < '2026-01-01';