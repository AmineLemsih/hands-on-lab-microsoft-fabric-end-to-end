# Captures à réaliser

Une capture par **écran utile** : nouvelle page, boîte de dialogue ou résultat significativement modifié. Pas une capture par clic. Les 72 écrans ci-dessous suivent les Labs 1 à 5 ; S3 et SharePoint sont des variantes, pas des obligations du parcours par défaut.

Format : PNG, **largeur 1600 px**, hauteur adaptée sans réduire le texte, interface française. Encadrer en **rouge** le contrôle ou le résultat à repérer ; garder assez de contexte pour reconnaître l'écran. Nom : `<lab>-<écran>-<sujet>.png`, sujet anglais. Ne pas présenter une image recomposée comme une capture d'un comportement testé.

Seul « Contoso » peut apparaître comme organisation. Masquer les adresses de compte, avatars, autres noms de tenant, UUID, URLs privées, IDs de capacité, connexions privées et canaux identifiants. Les noms génériques d'items restent visibles. Aucune clé ni aucun jeton ne doit être capturé.

## Schémas pédagogiques livrés

| Fichier | Usage | État |
| --- | --- | --- |
| `00-learning-path.svg` | Introduction, cinq étapes en chevrons | Livré, autonome, largeur 1600 px |
| `00-architecture.png` | Introduction, architecture | Livré, 1600 x 860 px, export du draw.io |
| `00-architecture.svg` | README et vue agrandie | Livré, icônes intégrées sans ressource externe |
| `10-recap.svg` | Conclusion, cinq acquis | Livré, autonome, largeur 1600 px |
| `banner.jpg` | Bannière optionnelle | 1280 x 640 px ; ne pas ajouter banner_url avant livraison |

Ces trois schémas ne sont pas des captures de Fabric. L'architecture a deux formats d'export et une source éditable dans [../architecture.drawio](../architecture.drawio). Les captures d'interface absentes restent commentées ; les règles d'anonymisation et de validation ci-dessous les concernent toujours.

## Lab 1 : 16 écrans

| Fichier | Sous-section / après l'étape | Écran et zone à encadrer |
| --- | --- | --- |
| `lab01-01-workspace.png` | Ouvrir votre espace / 5 | Workspace personnel, nom et Nouvel élément |
| `lab01-02-item-picker.png` | Ouvrir votre espace / 8 | Sélecteur d'items, Lakehouse |
| `lab01-03-lakehouse-dialog.png` | Ouvrir votre espace / 10 | Dialogue lh_lab, case schémas |
| `lab01-04-lakehouse-explorer.png` | Ouvrir votre espace / 11 | Explorer lh_lab, Tables et dbo |
| `lab01-05-shortcut-menu.png` | Créer les raccourcis / 3 | Menu dbo, Nouveau raccourci |
| `lab01-06-shortcut-source.png` | Créer les raccourcis / 4 | Source Microsoft OneLake |
| `lab01-07-onelake-catalog.png` | Créer les raccourcis / 6 | Catalogue, source lh_source |
| `lab01-08-reference-tables.png` | Créer les raccourcis / 10 | Tables sites et emission_factors cochées |
| `lab01-09-shortcut-review.png` | Créer les raccourcis / 12 | Résumé des deux raccourcis |
| `lab01-10-sites-preview.png` | Créer les raccourcis / 15 | Aperçu sites, colonnes et valeurs |
| `lab01-11-factors-preview.png` | Créer les raccourcis / 17 | Facteurs 2025 et deux coefficients fictifs |
| `lab01-12-shortcut-properties.png` | Créer les raccourcis / 19 | Propriétés, cible source sans UUID visible |
| `lab01-13-s3-source.png` | Variante : parcourir une source S3 (10 min, si disponible) / 5 | Variante S3, fichiers visibles dans lh_source |
| `lab01-14-files-menu.png` | Variante : parcourir une source S3 (10 min, si disponible) / 9 | Variante S3, nouveau raccourci dans Fichiers |
| `lab01-15-nested-target.png` | Variante : parcourir une source S3 (10 min, si disponible) / 13 | Variante S3, cible du raccourci, après validation réelle |
| `lab01-16-nested-preview.png` | Variante : parcourir une source S3 (10 min, si disponible) / 17 | Variante S3, mêmes fichiers dans lh_lab |

## Lab 2 : 20 écrans

| Fichier | Sous-section / après l'étape | Écran et zone à encadrer |
| --- | --- | --- |
| `lab02-01-dataflow-picker.png` | Créer le flux / 4 | Sélecteur Dataflow Gen2 |
| `lab02-02-dataflow-name.png` | Créer le flux / 5 | Nom df_energy et éditeur initial |
| `lab02-03-regional-settings.png` | Créer le flux / 6 | Locale Anglais (États-Unis) |
| `lab02-04-web-connector.png` | Importer le fichier du dépôt / 2 | Connecteur Web ou Texte/CSV avec URL |
| `lab02-05-anonymous-connection.png` | Importer le fichier du dépôt / 4 | URL raw publique, authentification anonyme |
| `lab02-06-csv-preview.png` | Importer le fichier du dépôt / 9 | Aperçu CSV, virgule et UTF-8 |
| `lab02-07-sharepoint-connection.png` | Variante : avec vos propres fichiers / 5 | Variante SharePoint, compte d'organisation, URL masquée |
| `lab02-08-sharepoint-filter.png` | Variante : avec vos propres fichiers / 10 | Variante SharePoint, Name et Folder Path |
| `lab02-09-sharepoint-content.png` | Variante : avec vos propres fichiers / 14 | Variante SharePoint, CSV dans Power Query |
| `lab02-10-detected-types.png` | Nettoyer et typer / 5 | Types détectés des six colonnes |
| `lab02-11-type-errors.png` | Nettoyer et typer / 6 | Correction conditionnelle kwh_elec et erreurs invalid |
| `lab02-12-errors-removed.png` | Nettoyer et typer / 9 | Étapes de suppression des vides et erreurs |
| `lab02-13-month-start.png` | Nettoyer et typer / 16 | month_start de type Date |
| `lab02-14-destination-picker.png` | Écrire dans le lakehouse / 3 | Destination Lakehouse |
| `lab02-15-destination-table.png` | Écrire dans le lakehouse / 8 | lh_lab, dbo, consumption |
| `lab02-16-destination-mapping.png` | Écrire dans le lakehouse / 11 | Sept colonnes et Remplacer |
| `lab02-17-dataflow-run.png` | Écrire dans le lakehouse / 16 | Exécution réussie et lignes écrites |
| `lab02-18-pipeline-canvas.png` | Orchestrer et exécuter / 7 | pl_energy_daily, activité Dataflow |
| `lab02-19-pipeline-settings.png` | Orchestrer et exécuter / 11 | Paramètres de l'activité, df_energy |
| `lab02-20-pipeline-run.png` | Orchestrer et exécuter / 14 | Exécution manuelle réussie |

## Lab 3 : 12 écrans

| Fichier | Sous-section / après l'étape | Écran et zone à encadrer |
| --- | --- | --- |
| `lab03-01-sql-endpoint.png` | Ouvrir la requête visuelle / 3 | Point de terminaison SQL de lh_lab |
| `lab03-02-visual-canvas.png` | Ouvrir la requête visuelle / 10 | Trois tables sur le canevas |
| `lab03-03-sites-join.png` | Rapprocher les tables / 6 | Jointure externe gauche sur site_id |
| `lab03-04-sites-expansion.png` | Rapprocher les tables / 9 | Colonne region à développer |
| `lab03-05-sites-result.png` | Rapprocher les tables / 11 | Résultat après ajout de region |
| `lab03-06-factors-join.png` | Rapprocher les tables / 17 | Jointure externe gauche sur year |
| `lab03-07-factors-expansion.png` | Rapprocher les tables / 21 | Deux colonnes de facteurs |
| `lab03-08-joined-result.png` | Rapprocher les tables / 23 | Résultat des deux jointures |
| `lab03-09-group-dialog.png` | Regrouper les consommations / 7 | region/month_start, sommes et comptage |
| `lab03-10-grouped-result.png` | Regrouper les consommations / 8 | Résultat regroupé |
| `lab03-11-save-view.png` | Enregistrer la vue / 5 | Dialogue dbo.v_energy_monthly |
| `lab03-12-view-preview.png` | Enregistrer la vue / 8 | Vue et 72 couples région/mois |

## Lab 4 : 12 écrans

| Fichier | Sous-section / après l'étape | Écran et zone à encadrer |
| --- | --- | --- |
| `lab04-01-agent-picker.png` | Créer l'agent / 4 | Agent de données Fabric dans les éléments |
| `lab04-02-agent-name.png` | Créer l'agent / 6 | Création energy_agent |
| `lab04-03-source-catalog.png` | Créer l'agent / 8 | Source lh_lab dans le catalogue |
| `lab04-04-selected-tables.png` | Créer l'agent / 12 | Trois tables autorisées |
| `lab04-05-first-answer.png` | Poser les six questions avant configuration / 1 | Réponse Q1 avant instructions |
| `lab04-06-generated-query.png` | Poser les six questions avant configuration / 3 | Requête générée et source |
| `lab04-07-missing-period.png` | Poser les six questions avant configuration / 5 | Réponse Q6 et absence de 2024 |
| `lab04-08-instructions.png` | Ajouter les définitions métier / 3 | Instructions enregistrées |
| `lab04-09-example-download.png` | Ajouter un exemple sans écrire de code / 2 | Exemple Q1 public ouvert et copiable |
| `lab04-10-example-editor.png` | Ajouter un exemple sans écrire de code / 7 | Paire question/requête, source lh_lab |
| `lab04-11-example-validation.png` | Ajouter un exemple sans écrire de code / 9 | Validation réussie de l'exemple |
| `lab04-12-comparison.png` | Comparer après configuration / 6 | Résultat après instructions et contrôle |

## Lab 5 : 12 écrans

| Fichier | Sous-section / après l'étape | Écran et zone à encadrer |
| --- | --- | --- |
| `lab05-01-shared-report.png` | Ouvrir le rapport commun / 3 | energy_report en lecture |
| `lab05-02-before-state.png` | Ouvrir le rapport commun / 5 | Six régions sous 10 000 kWh |
| `lab05-03-alert-menu.png` | Définir votre règle / 1 | Menu du visuel, Définir une alerte |
| `lab05-04-alert-measure.png` | Définir votre règle / 4 | latest_day_kwh suivi par region |
| `lab05-05-alert-threshold.png` | Définir votre règle / 7 | Devient supérieur à 10000 |
| `lab05-06-alert-recipient.png` | Définir votre règle / 9 | Teams et destinataire anonymisé |
| `lab05-07-alert-workspace.png` | Définir votre règle / 11 | Workspace personnel comme destination |
| `lab05-08-activator-dialog.png` | Définir votre règle / 13 | Nouvel élément act_energy |
| `lab05-09-rule-active.png` | Définir votre règle / 16 | Règle enregistrée et active |
| `lab05-10-after-state.png` | Voir le déclenchement et ouvrir Activator / 3 | Bretagne au-dessus du seuil |
| `lab05-11-teams-message.png` | Voir le déclenchement et ouvrir Activator / 5 | Notification reçue, compte masqué |
| `lab05-12-rule-history.png` | Voir le déclenchement et ouvrir Activator / 10 | Condition et historique réel des actions |

## Compléments et extensions

| Fichier | Usage | Écran |
| --- | --- | --- |
| `lab05-13-rehearsal-notification.png` | Notes animateur uniquement | Notification de répétition datée, identifiée comme telle |
| `lab06-01-sql-results.png` | Lab 6 | Requêtes, volumes et vue |
| `lab06-02-pipeline-option.png` | Lab 6, contexte optionnel | Alternative par pipeline |
| `lab07-01-direct-lake-model.png` | Lab 7 | Relations et mesure total_kgco2e |
| `lab07-02-agent-semantic-model.png` | Lab 7 | Source sm_energy_lab et résultat DAX |
| `lab08-01-eventstream.png` | Lab 8 | Bicycles et destination Eventhouse |
| `lab08-02-kql-results.png` | Lab 8 | Champs mappés et requêtes KQL |
| `lab08-03-activator.png` | Lab 8 | Objet station et règle active |
| `bonus-01-copilot-dataflow.png` | Bonus | Transformation dans un flux distinct |
| `bonus-02-copilot-query.png` | Bonus | Question française et KQL proposé |

## Activer les captures livrées

Déposer chaque PNG réel dans ce dossier avec le nom attendu, puis exécuter depuis la racine :

```powershell
python tools/check_assets.py
python tools/check_assets.py --check --summary
```

La première commande liste les références, signale les fichiers présents/manquants, commente les captures absentes et décommente automatiquement celles dont le fichier existe et n'est pas vide. Elle ne génère ni image ni bannière. Les trois schémas restent actifs par exception explicite. La seconde commande contrôle sans écrire ; son code vaut 1 seulement si une référence doit changer.

Avant commit : vérifier le cadre rouge, la lisibilité à 1600 px, les textes alternatifs, l'écran réellement testé et l'anonymisation. Aucun fichier image vide ne doit être ajouté pour contourner ce contrôle.