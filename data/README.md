# Données synthétiques Contoso

Ces données servent uniquement à l'apprentissage. Contoso est fictive. Les sites ne désignent aucun bâtiment réel. Les facteurs d'émission sont fictifs, même si leurs ordres de grandeur sont plausibles.

## Génération

Depuis la racine du dépôt, avec Python 3.11 ou ultérieur, sans dépendance externe :

```powershell
python data/generate_data.py
```

La graine vaut `2025`. Les six CSV sont écrits dans `data/csv/` et versionnés dans Git. Le corrigé Markdown y est également généré, mais reste ignoré. Relancer la même commande produit les mêmes valeurs. Le script relit les CSV, vérifie les volumes et calcule les six réponses attendues. Aucun téléchargement ni appel cloud. Les identifiants restent en anglais, même si le texte de l'atelier est traduit.

| Fichier généré | Volume hors en-tête | Usage |
| --- | ---: | --- |
| `sites.csv` | 30 | Référentiel des bâtiments |
| `emission_factors.csv` | 1 ligne, 2 facteurs | Facteurs annuels électricité et gaz |
| `consumption_2025.csv` | 10 950 | Nettoyage et analyse de l'année 2025 |
| `consumption_latest_day.csv` | 30 | Fichier actif, initialisé à l'état avant |
| `consumption_latest_day_before.csv` | 30 | Toutes les régions sous 10 000 kWh |
| `consumption_latest_day_after.csv` | 30 | Une région au-dessus de 10 000 kWh |
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

## Fichiers publics et préparation de lh_source

Les données synthétiques sont [consultables et téléchargeables dans le dépôt](https://github.com/AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/tree/main/data/csv). Le parcours participant utilise directement l'[URL raw du CSV annuel](https://raw.githubusercontent.com/AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/main/data/csv/consumption_2025.csv), authentification anonyme. Aucun fichier à envoyer séparément ni dépôt manuel dans le lakehouse n'est nécessaire.

Pour préparer la source commune, importer [setup_lh_source.ipynb](../setup/setup_lh_source.ipynb) dans Fabric, l'attacher à **lh_source**, schémas activés, puis exécuter les cellules 2 à 4. La [procédure d'import](../setup/README.md#préparer-lh_source-avec-le-notebook) détaille les clics. Le notebook vérifie son lakehouse par défaut avant toute écriture, télécharge les sources publiques, applique des types explicites et remplace les quatre tables de démonstration. Il ne configure ni permissions, ni modèle sémantique, ni rapport.

Il prépare `sites` (30 lignes), `emission_factors` (une ligne), `consumption` (10 840 lignes nettoyées, avec `month_start`) et `consumption_latest_day` (30 lignes dans l'état `before`). Le participant recrée lui-même `consumption` dans `lh_lab` depuis le CSV imparfait, sans exécuter ce notebook pendant le tronc commun.

**Accès OneLake obligatoire :** donner Viewer au groupe sur `ws-shared` **et partager explicitement `lh_source` avec ce groupe**. Activer l'option qui accorde `ReadAll`, « Lire toutes les données Apache Spark » / « Lire toutes les données OneLake » selon l'interface. <!-- TODO vérifier --> Le partage ajoute aussi `Read`. Il ne donne aucun droit d'écriture. Cela permet les raccourcis et Direct Lake sur OneLake en SSO. Si la sécurité OneLake est activée, faire valider également ses rôles de lecture. Tester avec un compte participant. [Permissions du lakehouse](https://learn.microsoft.com/fabric/data-engineering/lakehouse-sharing) ; [sécurité Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration).

Pour SharePoint, déposer uniquement `consumption_2025.csv` dans une bibliothèque accessible aux participants. Transmettre l'URL du **site** par la variable `sp_site` du lien de session. Le connecteur « Dossier SharePoint » attend l'URL du site, pas un lien de partage du CSV.

## Préparer les tables du rapport

Le notebook prépare déjà les tables du rapport. Il nettoie le fichier annuel avec les mêmes règles : suppression des observations vides et mal typées, sans imputation, puis ajout du premier jour du mois. Attendre leur synchronisation dans le point de terminaison SQL avant de connecter le rapport.

Contrôles avant de suivre [le guide du rapport](../report/README.md) : `consumption` = 10 840 lignes ; `consumption_latest_day` = 30 lignes ; `sites` = 30 ; `emission_factors` = 1. Le rapport est construit sur ces tables, jamais sur le CSV annuel sale.

## Simuler un franchissement de seuil

Le dernier jour disponible est **le dernier jour du jeu**, le 31 décembre 2025. Ce choix rend l'atelier réutilisable n'importe quelle année. Ne pas appliquer de filtre relatif « aujourd'hui » au rapport.

Les cellules 2 à 4 initialisent `consumption_latest_day` depuis `consumption_latest_day_before.csv`. Actualiser ensuite `sm_energy_report` et attendre que les règles Activator aient observé l'état sous le seuil.

Pendant la section 5, mettre `apply_after = True` dans la **cellule 6**, puis exécuter cette cellule seulement. Elle télécharge `consumption_latest_day_after.csv` et remplace uniquement `consumption_latest_day`. Remettre le paramètre à False, puis actualiser `sm_energy_report`. La Bretagne passe de **2 724,55 à 36 724,55 kWh**. Pour réinitialiser, réexécuter les cellules 2 à 4, puis actualiser le modèle.

Le seuil régional reste **10 000 kWh** ; Q4 conserve **20 000 kWh par site/jour**. Les fichiers annuels et les facteurs ne changent pas pendant la bascule. La version publiée de `consumption_latest_day.csv` reste initialisée à `before` ; ne pas commiter un état temporaire de répétition. Le notebook ne dépend pas de ce fichier actif et choisit explicitement `before` ou `after`.

Le visuel d'alerte n'a pas d'axe temporel. Une alerte qui a déjà observé un point d'un axe temporel peut ignorer une correction de ce même point. Tester la latence et le mode de franchissement avant la session ; garder une notification reçue en amont comme plan B.