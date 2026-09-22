# Valeurs attendues du jeu Contoso

Généré par `python data/generate_data.py` à partir des CSV relus ; ne pas modifier à la main.
Les comptes et les sommes portent sur les observations réellement conservées, sans imputation.
Les seuils sont les paramètres du scénario ; les facteurs carbone restent fictifs.

| Identifiant | Valeur | Signification |
| --- | ---: | --- |
| site_count | 30 | sites dans le référentiel |
| factor_rows | 1 | lignes de facteurs |
| electricity_factor | 0,055 | kgCO2e par kWh électrique |
| gas_factor | 0,205 | kgCO2e par kWh de gaz |
| raw_rows | 10 950 | observations avant nettoyage |
| blank_rows | 55 | observations vides |
| invalid_rows | 55 | observations en erreur |
| rejected_rows | 110 | observations rejetées |
| clean_rows | 10 840 | observations conservées |
| raw_columns | 6 | colonnes du CSV annuel |
| clean_columns | 7 | colonnes après ajout de month_start |
| region_count | 6 | régions |
| monthly_groups | 72 | couples région/mois observés |
| active_sites | 27 | sites actifs au 1er janvier 2025 |
| peak_count | 6 | couples site/jour au-dessus du seuil d'anomalie |
| snapshot_rows | 30 | observations par instantané |
| electricity_kwh | 2 896 164,51 | kWh électriques observés en 2025 |
| gas_kwh | 1 686 455,14 | kWh de gaz observés en 2025 |
| total_kwh | 4 582 619,65 | kWh totaux observés en 2025 |
| carbon_kgco2e | 505 012,35 | kgCO2e fictifs en 2025 |
| top_region_kgco2e | 133 453,59 | kgCO2e fictifs : Hauts-de-France |
| top_month_kwh | 600 058,04 | kWh du mois maximal : 2025-12 |
| alert_threshold_kwh | 10 000 | seuil strict par région, instantané |
| anomaly_threshold_kwh | 20 000 | seuil strict par site/jour, historique |
| bretagne_before_kwh | 2 724,55 | kWh en Bretagne avant franchissement |
| bretagne_after_kwh | 36 724,55 | kWh en Bretagne après franchissement |
