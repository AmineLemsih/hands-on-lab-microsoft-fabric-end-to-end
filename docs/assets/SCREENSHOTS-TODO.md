# Captures à réaliser

Aucune image n'est générée dans ce kit. Les références ci-dessous sont des placeholders volontaires du workshop. Conserver les noms anglais, y compris dans une traduction. La bannière doit mesurer idéalement 1280 x 640 pixels, selon le template MOAW.

Faire les captures dans un environnement de démonstration autorisé, interface française, avec uniquement les données synthétiques. Masquer les adresses de compte, avatars identifiants, tenant, IDs, URLs, connexions et canaux privés. Ne pas transformer une capture de répétition en preuve d'un test de la session en cours.

| Fichier à fournir dans ce dossier | Section | Ce qu'on doit voir |
| --- | --- | --- |
| `banner.jpg` | En-tête | Bannière de l'atelier à fournir par l'auteur ; titre, aucune identité client |
| `00-learning-path.png` | 0, fil rouge | Du fichier nettoyé à la réponse vérifiée ; branche rapport vers notification |
| `00-architecture.png` | 0, architecture | Espace commun en lecture, espace personnel en écriture, raccourcis, rapport et Activator |
| `01-lakehouse.png` | 1, création | `lh_lab` dans le workspace personnel ; zones Tables et Fichiers |
| `01-onelake-shortcuts.png` | 1, raccourcis | `sites` et `emission_factors` marqués comme raccourcis, cible `lh_source` |
| `02-lakehouse-source.png` | 2, variante A | Sélection d'un CSV dans les Fichiers du lakehouse commun |
| `02-sharepoint-source.png` | 2, variante B | Un seul `consumption_2025.csv` retenu par nom et dossier ; URL masquée |
| `02-cleaning.png` | 2, préparation | Suppression des vides et erreurs, types et `month_start` Date |
| `02-destination.png` | 2, destination | `lh_lab`, `dbo.consumption`, sept colonnes, méthode Remplacer |
| `02-pipeline-schedule.png` | 2, orchestration | Activité Dataflow et réussite de l'exécution manuelle ; nom de fichier conservé |
| `03-visual-joins.png` | 3, jointures | Clés `site_id` et `year`, colonnes développées, pas de multiplication des lignes |
| `03-monthly-view.png` | 3, résultat | `v_energy_monthly`, région, mois, kWh, kgCO2e et nombre d'observations |
| `04-agent-sources.png` | 4, sources | `energy_agent`, `lh_lab`, exactement les trois tables sélectionnées |
| `04-agent-comparison.png` | 4, contrôle | Instructions et exemple validés, avant/après, requête générée et unités |
| `05-energy-report.png` | 5, lecture | Les deux visuels du rapport commun, six régions sous le seuil et date du jeu |
| `05-alert-settings.png` | 5, configuration | Seuil par région, mesure `latest_day_kwh`, destinataire personnel anonymisé et workspace personnel |
| `05-activator-rule.png` | 5, règle | `act_energy`, observations avant/après, franchissement et action horodatée |
| `05-alert-notification.png` | Notes animateur, plan B | Notification Teams réellement reçue en répétition ; date et caractère « répétition » explicites |
| `06-warehouse-pipeline.png` | 6, copie | Trois activités vers `wh_energy`, mappage et clés Upsert propres à chaque table |
| `06-sql-results.png` | 6, requêtes | Volumes corrects, classement régional, six pics et vue mensuelle |
| `07-direct-lake-model.png` | 7, modèle | Trois tables, Direct Lake, deux relations simples, mesure `total_kgco2e` |
| `07-agent-semantic-model.png` | 7, agent | Source `sm_energy_lab`, requête DAX et résultat vérifié |
| `08-eventstream-sample.png` | 8, flux | Source intégrée Bicycles et destination Eventhouse ; aucune étiquette énergie |
| `08-eventhouse-kql.png` | 8, analyse | `event_time`, `station_id`, `bike_count`, trois résultats KQL |
| `08-stream-activator.png` | 8, règle | Objet station, propriété numérique, condition et notification personnelle |
| `09-copilot-transformation.png` | 9, bonus | `df_energy_copilot`, demande de `total_kwh`, proposition sans destination destructive |
| `09-copilot-query.png` | 9, bonus | Question française, KQL proposé, fenêtre de temps et résultat comparé |
| `10-recap.png` | 10, conclusion | Synthèse des éléments et de leurs rôles, sans liens ni IDs privés |

Les deux schémas de section 0 sont à produire manuellement par l'auteur ou à capturer depuis un support autorisé ; aucun rendu graphique n'est fabriqué automatiquement ici. Le fil rouge textuel reste lisible sans eux.

## Contrôle avant publication

- [ ] Chaque image correspond à la version de l'interface testée à J-7.
- [ ] Tous les identifiants techniques restent anglais.
- [ ] Les images n'introduisent aucune donnée ou identité client.
- [ ] Les textes alternatifs restent descriptifs.
- [ ] Le texte des captures est lisible au format du workshop.
- [ ] La notification du plan B est identifiée comme une répétition.
- [ ] Aucun fichier image vide ou fictif n'est ajouté pour faire disparaître un lien cassé.