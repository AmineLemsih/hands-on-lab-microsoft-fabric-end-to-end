# Données synthétiques Contoso

Ces données servent uniquement à l'apprentissage. Contoso est fictive. Les sites ne désignent aucun bâtiment réel. Les facteurs d'émission sont fictifs, même si leurs ordres de grandeur sont plausibles.

## Génération

Depuis la racine du dépôt, avec Python 3.11 ou ultérieur, sans dépendance externe :

```powershell
python data/generate_data.py
```

La graine vaut `2025`. Les sept fichiers sont écrits dans `data/out/`, exclu de Git. Relancer la même commande produit les mêmes fichiers. Le script relit les CSV, vérifie les volumes et calcule les six réponses attendues. Aucun téléchargement ni appel cloud. Les identifiants restent en anglais, même si le texte de l'atelier est traduit.

| Fichier généré | Volume hors en-tête | Usage |
| --- | ---: | --- |
| `sites.csv` | 30 | Référentiel des bâtiments |
| `emission_factors.csv` | 1 ligne, 2 facteurs | Facteurs annuels électricité et gaz |
| `consumption_2025.csv` | 10 950 | Nettoyage et analyse de l'année 2025 |
| `consumption_latest_day.csv` | 30 | Fichier actif, initialisé à l'état avant |
| `consumption_latest_day_before.csv` | 30 | Toutes les régions sous 20 000 kWh |
| `consumption_latest_day_after.csv` | 30 | Une région au-dessus de 20 000 kWh |
| `questions_expected_answers.md` | 6 questions | Corrigé numérique et totaux régionaux avant/après |

Format CSV : UTF-8 avec BOM, séparateur virgule, point décimal, dates ISO `YYYY-MM-DD`. Dans Power Query français, convertir les décimaux avec les paramètres régionaux « Anglais (États-Unis) ». Les régions restent des noms géographiques français. Les codes d'activité restent en anglais.

## Dictionnaire

### Sites

| Colonne | Type cible | Définition |
| --- | --- | --- |
| `site_id` | Texte | Clé unique, de `S001` à `S030` |
| `site_name` | Texte | Nom fictif, « Contoso site 01 », etc. |
| `region` | Texte | Une des six régions françaises retenues |
| `activity` | Texte | `office` : bureau ; `warehouse` : entrepôt ; `factory` : usine ; `branch` : agence |
| `area_m2` | Entier | Surface simulée en mètres carrés |
| `opening_date` | Date | Premier jour d'activité du site |

Les sites S028, S029 et S030 ouvrent respectivement les 15 mars, 1er juillet et 1er octobre 2025. Les 27 autres sont déjà actifs le 1er janvier 2025. Aucun site ne ferme. Avant ouverture, les consommations sont nulles au sens numérique : `0`, pas une valeur manquante.

### Facteurs d'émission

La table `emission_factors` (facteurs d'émission) contient les coefficients de conversion.

| Colonne | Type cible | Définition |
| --- | --- | --- |
| `year` | Entier | Clé unique : `2025` |
| `elec_kgco2e_per_kwh` | Décimal | `0.055` kgCO2e par kWh électrique |
| `gas_kgco2e_per_kwh` | Décimal | `0.205` kgCO2e par kWh de gaz |
| `source` | Texte | « fictif, ne pas utiliser pour un reporting réel » |

Le format est volontairement large : **une ligne par année, deux colonnes de facteurs**. Cela permet une seule jointure sur `year` et une relation plusieurs-vers-un dans Power BI. Une table de deux lignes par énergie jointe seulement sur l'année doublerait les consommations. Ne pas modifier cette granularité sans adapter tout l'atelier.

### Consommations

La table `consumption` (consommation) reçoit l'historique nettoyé. La table `consumption_latest_day` (consommation du dernier jour disponible) reçoit l'instantané. Les quatre CSV de consommation ont le même schéma.

| Colonne | Type cible | Définition |
| --- | --- | --- |
| `site_id` | Texte | Référence à `sites.site_id` |
| `date` | Date | Jour civil de l'observation |
| `year` | Entier | Référence à `emission_factors.year` |
| `kwh_elec` | Décimal | Énergie électrique journalière en kWh, pas une puissance en kW |
| `kwh_gas` | Décimal | Énergie du gaz journalière en kWh |
| `avg_temp` | Décimal | Température moyenne simulée en degrés Celsius |

Dans le lab 2, ajouter `month_start`, de type **Date**, avec le premier jour du mois. Ne pas utiliser seulement un nom de mois, qui se trierait alphabétiquement.

Les jours d'hiver demandent davantage de chauffage. Les week-ends consomment moins. Un bruit aléatoire à graine fixe évite des courbes parfaitement régulières. Ce n'est ni un modèle physique ni une estimation financière.

### Qualité et anomalies

Le fichier annuel représente initialement 30 sites x 365 jours. Le script remplace 55 observations par des enregistrements dont tous les champs sont vides et rend 55 autres observations non convertibles (`invalid` dans `kwh_elec`). Total : 110 / 10 950 = **1,0046 %**, arrondi au plus proche de 1 %.

Le nettoyage de référence supprime les lignes vides puis les lignes en erreur après typage. Il reste **10 840 lignes** et des observations manquantes. Ne pas remplacer les erreurs par zéro. Les totaux du corrigé portent sur les seules observations conservées, pas sur une année reconstruite.

Six pics dépassent chacun 20 000 kWh au total. Ils ne sont jamais corrompus par les défauts de qualité :

| Site | Date |
| --- | --- |
| S003 | 2025-01-15 |
| S007 | 2025-03-12 |
| S012 | 2025-06-18 |
| S018 | 2025-08-21 |
| S024 | 2025-11-14 |
| S030 | 2025-12-31 |

Une anomalie n'est pas une preuve de panne. Les données ne permettent pas d'en déduire une cause.

## Déposer les fichiers dans lh_source

À réaliser par l'animateur avant la session, avec un accès en écriture au workspace commun indiqué sur la fiche participant. Les noms `ws-shared` et `lh_source` sont des noms génériques.

1. Ouvrir le workspace commun.
2. Ouvrir `lh_source`.
3. Sélectionner « Fichiers ».
4. Choisir « Charger des fichiers » dans le menu de chargement. <!-- TODO vérifier -->
5. Sélectionner `sites.csv`, `emission_factors.csv`, `consumption_2025.csv` et `consumption_latest_day.csv` dans `data/out/`.
6. Lancer le chargement.
7. Vérifier les quatre noms de fichiers dans « Fichiers ».
8. Créer un Dataflow Gen2 de préparation `df_source_references` dans le workspace commun.
9. Ajouter le connecteur « Lakehouse ».
10. Naviguer vers les fichiers de `lh_source`.
11. Importer `sites.csv` comme requête `sites`.
12. Définir les types indiqués dans le dictionnaire.
13. Affecter la destination `lh_source`, schéma `dbo`, table `sites`, méthode « Remplacer ».
14. Ajouter une seconde requête depuis `emission_factors.csv`.
15. Définir les types indiqués dans le dictionnaire, avec la bonne locale décimale.
16. Affecter la destination `lh_source`, schéma `dbo`, table `emission_factors`, méthode « Remplacer ».
17. Publier le flux.
18. Exécuter le flux.
19. Vérifier les **tables Delta**, pas seulement les fichiers : 30 sites et une ligne de facteurs.
20. Vérifier que les deux tables sont visibles dans le point de terminaison SQL.
21. Tester leur lecture avec un compte participant.

Ne pas déposer les versions `before` et `after` dans le dossier ingéré par un connecteur qui combine les fichiers : cela triplerait les observations. Garder ces deux fichiers localement pour le remplacement du seul fichier actif.

Pour un lakehouse sans schémas créé antérieurement, ne pas ajouter un faux niveau de dossier `dbo` dans « Tables ». Le point de terminaison SQL expose les noms sous `dbo` ; tester les chemins réellement affichés avant la session.

**Accès OneLake obligatoire :** donner Viewer au groupe sur `ws-shared` **et partager explicitement `lh_source` avec ce groupe**. Activer l'option qui accorde `ReadAll`, « Lire toutes les données Apache Spark » / « Lire toutes les données OneLake » selon l'interface. <!-- TODO vérifier --> Le partage ajoute aussi `Read`. Il ne donne aucun droit d'écriture. Cela permet les raccourcis et Direct Lake sur OneLake en SSO. Si la sécurité OneLake est activée, faire valider également ses rôles de lecture. Tester avec un compte participant. [Permissions du lakehouse](https://learn.microsoft.com/fabric/data-engineering/lakehouse-sharing) ; [sécurité Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration).

Le parcours de navigation d'un fichier binaire CSV dans le connecteur Lakehouse doit être répété en français avant diffusion. Si cette navigation n'est pas disponible dans le tenant, retenir **la variante SharePoint du lab 2**. Ne pas remplacer l'exercice par une URL publique ou un connecteur inventé. <!-- TODO vérifier -->

Pour SharePoint, déposer uniquement `consumption_2025.csv` dans une bibliothèque accessible aux participants. Mettre l'URL du **site** et le chemin du fichier dans la fiche participant privée. Le connecteur « Dossier SharePoint » attend l'URL du site, pas un lien de partage du CSV.

## Préparer les tables du rapport

Dans `lh_source`, préparer également la table **nettoyée** `consumption` en appliquant le lab 2, y compris la colonne `month_start`, avec `lh_source` comme destination. Préparer `consumption_latest_day` dans un flux séparé `df_source_latest` depuis **le fichier actif** `consumption_latest_day.csv`, avec les mêmes types, sans cumul des chargements.

Contrôles avant de suivre [le guide du rapport](../report/README.md) : `consumption` = 10 840 lignes ; `consumption_latest_day` = 30 lignes ; `sites` = 30 ; `emission_factors` = 1. Le rapport est construit sur ces tables, jamais sur le CSV annuel sale.

## Simuler un franchissement de seuil

Le dernier jour disponible est **le dernier jour du jeu**, le 31 décembre 2025. Ce choix rend l'atelier réutilisable n'importe quelle année. Ne pas appliquer de filtre relatif « aujourd'hui » au rapport.

```powershell
Copy-Item data/out/consumption_latest_day_before.csv data/out/consumption_latest_day.csv -Force
```

Cette version retire le pic de S030 **de l'instantané seulement**. Remplacer le CSV actif dans `lh_source`, exécuter `df_source_latest` qui remplace la table `consumption_latest_day`, puis actualiser le modèle sémantique du rapport. Attendre qu'Activator ait observé l'état sous le seuil. Tous les participants créent leur règle avant de poursuivre.

```powershell
Copy-Item data/out/consumption_latest_day_after.csv data/out/consumption_latest_day.csv -Force
```

Pendant la section 5, remplacer uniquement le fichier actif et refaire la même chaîne d'actualisation. Les fichiers historiques restent identiques. Le seuil de démonstration est **20 000 kWh par région**, comparaison strictement supérieure ; ce n'est pas un seuil métier recommandé. Le script garantit que toutes les régions sont sous le seuil avant et exactement une au-dessus après. Le corrigé donne les totaux exacts des deux états.

Le script génère les deux variantes en une exécution. `--latest-state after` initialise éventuellement le fichier actif à l'état après ; le défaut `before` est celui à utiliser avant la session. Une nouvelle génération écrase les sorties, y compris le fichier actif.

Le visuel d'alerte n'a pas d'axe temporel. Une alerte qui a déjà observé un point d'un axe temporel peut ignorer une correction de ce même point. Tester la latence et le mode de franchissement avant la session ; garder une notification reçue en amont comme plan B.