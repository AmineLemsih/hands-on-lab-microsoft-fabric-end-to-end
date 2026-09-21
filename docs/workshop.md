---
published: false
type: workshop
title: Product Hands-on Lab - Microsoft Fabric de bout en bout
short_title: Fabric de bout en bout
description: Un atelier guidé pour relier les données énergétiques des bâtiments fictifs de Contoso à une analyse, un agent conversationnel et une alerte avec Microsoft Fabric. Un parcours métiers sans programmation et des extensions pour les analystes.
level: beginner
navigation_numbering: true
navigation_levels: 3
authors: [Amine Lemsih]
contacts: ['@aminelemsih']
duration_minutes: 300
tags: fabric, onelake, lakehouse, dataflow gen2, pipeline, data agent, activator, real-time intelligence, csu, métiers
banner_url: assets/banner.jpg
audience: profils métiers, analystes, équipes data
sections_title:
  - Introduction
  - Prise en main
  - Ingestion
  - Exploration
  - Data agent
  - Alerte
  - 'Extension : Entrepôt et T-SQL'
  - 'Extension : Modèle sémantique Direct Lake'
  - 'Extension : Temps réel'
  - 'Bonus : Copilot dans Fabric'
  - Conclusion
---

# Product Hands-on Lab - Microsoft Fabric de bout en bout

## 0. Introduction

**Durée : 10 minutes.**

Contoso est une entreprise fictive. Elle possède des bureaux, des entrepôts, des usines et des agences. Elle veut comparer la consommation énergétique de ses bâtiments et repérer les situations à examiner.

Vous jouez le rôle d'un analyste métier. Vous partez de fichiers synthétiques. Vous préparez une analyse vérifiable, puis une alerte. Vous n'avez pas besoin de programmer dans le parcours métiers.

### Ce que vous allez construire

Le fil rouge se lit ainsi :

**Fichier annuel → nettoyage visuel → table commune aux analyses → question métier → réponse vérifiée → décision.**

**Dernier jour disponible → rapport fourni → seuil dépassé → notification Teams personnelle.**

Votre analyse et le rapport fourni utilisent le même schéma. Le rapport est déjà prêt dans l'espace commun : il ne dépend pas de la fin du travail de chaque participant.

![Fil rouge : du fichier énergétique à une réponse vérifiée et à une notification](assets/00-learning-path.png)

<div class="warning" data-title="Des données pour apprendre, pas pour déclarer">

> Tout est synthétique. Les facteurs carbone sont fictifs. Les résultats ne constituent ni un bilan carbone réel ni un reporting réglementaire. Une hausse de consommation indique une situation à examiner, pas sa cause.

</div>

### Modalités

| Parcours | Public et format | Sections | Temps réservé |
| --- | --- | --- | ---: |
| **Parcours métiers 3 h** | Analystes métier, chefs de projet, contrôle de gestion, RSE ; distanciel, 15 à 20 personnes | 0 à 5, puis 10 ; sauter les blocs « Comprendre » | 180 min |
| **Parcours complet 5 h** | Analystes et journée d'upskilling en présentiel | 0 à 8, puis 10 ; lire les cinq blocs « Comprendre » | 300 min |
| **Bonus Copilot** | Selon le temps disponible et les paramètres du tenant | 9 | Environ 15 min supplémentaires, hors des deux minutages |

Le minutage inclut les temps de contrôle. Les temps d'aide sont répartis par l'animateur. Les blocs « Contexte (optionnel) » restent dans le budget du module.

| Section | Activité | Métiers | Complet |
| --- | --- | ---: | ---: |
| 0 | Introduction | 10 min | 10 min |
| 1 | Prise en main | 20 min | 20 + 5 min |
| 2 | Ingestion | 35 min | 35 + 5 min |
| Pause | Après la section 2 | 15 min | 15 min |
| 3 | Exploration | 25 min | 25 + 5 min |
| 4 | Data agent | 30 min | 30 + 5 min |
| 5 | Alerte | 15 min | 15 + 5 min |
| 6 | Extension : Entrepôt et T-SQL | Sauter | 30 min |
| 7 | Extension : Modèle sémantique Direct Lake | Sauter | 25 min |
| Pause | Après la section 7 | Sans objet | 10 min |
| 8 | Extension : Temps réel | Sauter | 35 min |
| 9 | Bonus Copilot | Hors minutage | Hors minutage |
| 10 | Conclusion | 10 min | 10 min |
| Réserve | Aide, transitions et questions | 20 min | 15 min |
| **Total** | **Pauses comprises, sans le bonus** | **180 min** | **300 min** |

Sans les explications « Comprendre », les activités du tronc commun valent 145 minutes. Les extensions 6 à 8 ajoutent 90 minutes. Les cinq explications ajoutent 25 minutes. On ne compte pas les attentes techniques comme du contenu pédagogique.

### Architecture

Un **workspace**, ou espace de travail, regroupe les éléments Fabric et leurs droits d'accès. Une **capacité** est la ressource de calcul partagée par ces éléments. Un **tenant** est l'environnement de votre organisation.

| Emplacement | Éléments | Votre usage |
| --- | --- | --- |
| Espace commun, nom générique `ws-shared` | `lh_source`, fichiers et tables de référence ; `energy_report` et son modèle `sm_energy_report` | Lecture. L'animateur prépare et actualise les données. |
| Votre espace, nom générique `ws-lab-<email_local_part>` | `lh_lab`, `df_energy`, `pl_energy_daily`, `energy_agent`, `act_energy` | Création et modification de vos propres éléments. |
| Extensions, dans votre espace | `wh_energy`, `sm_energy_lab`, `es_sample`, `eh_sample`, `act_sample` | Entrepôt SQL, modèle d'analyse et flux d'exemple. |

**OneLake** est le stockage logique commun de Fabric. Un **lakehouse** organise des fichiers et des tables dans OneLake. Une **table Delta** est un ensemble de fichiers de données avec un journal assurant la cohérence des écritures.

Dans `lh_source`, la table `sites` (sites) décrit les bâtiments. La table `emission_factors` (facteurs d'émission) fournit deux coefficients par année. Vous créerez dans `lh_lab` la table `consumption` (consommation). La table `consumption_latest_day` (consommation du dernier jour disponible) est déjà préparée dans la source pour le rapport.

Un **raccourci OneLake** référence une table existante sans en créer une copie indépendante. **Dataflow Gen2** nettoie les données par des actions visuelles. Un **pipeline** enchaîne et planifie des activités. Un **data agent** transforme une question en requête sur les données autorisées. **Activator** surveille une condition et lance une action.

**Architecture textuelle :** `lh_source` référence → raccourcis dans `lh_lab` ; CSV → `df_energy` → `consumption` ; `pl_energy_daily` lance le flux ; SQL visuel et `energy_agent` lisent les tables. En parallèle, `lh_source` → `sm_energy_report` à identité fixe → `energy_report` → `act_energy` personnel → Teams.

![Architecture : source commune en lecture, espace personnel en écriture et alerte personnelle](assets/00-architecture.png)

### Prérequis participant

Votre animateur vous transmet une **fiche participant privée**. Elle contient les liens et les noms propres à votre session. Utilisez-la à chaque fois qu'un lien, un workspace ou un contact est demandé.

- Un navigateur récent, avec Fabric en français.
- Le compte professionnel indiqué sur votre fiche, déjà connecté au bon tenant.
- Un espace personnel avec le rôle **Membre**, sur une capacité Fabric payante active.
- Le rôle **Lecteur**, ou Viewer, dans l'espace commun.
- Le partage de `lh_source` au groupe avec `Read` et **`ReadAll`**, via l'option « Lire toutes les données Apache Spark » ou « Lire toutes les données OneLake ». <!-- TODO vérifier --> Viewer seul ne donne pas tous les accès OneLake nécessaires.
- L'accès en lecture à `energy_report` et à son modèle. Ce modèle commun utilise une **identité fixe** : une connexion autorisée porte l'accès à la source. Ce choix ne remplace pas votre ReadAll pour les raccourcis.
- Une licence adaptée aux exercices de votre fiche. Sous F64, ouvrir le rapport partagé nécessite Power BI Pro ou une licence compatible. F64 ne dispense pas de vérifier les droits et licences de création.
- L'accès Teams indiqué sur votre fiche, pour recevoir une notification personnelle.

**SSO**, ou authentification unique, signifie que le moteur utilise votre identité. Le modèle Direct Lake de l'extension 7 utilise SSO ; vous devez donc conserver la lecture de la cible des raccourcis dans `lh_source`.

<div class="important" data-title="Préparation obligatoire de l'alerte">

> L'animateur teste à J-7 le bouton « Définir une alerte » depuis le rapport commun avec un compte Viewer, sur la capacité cible, en choisissant un workspace personnel comme destination. <!-- TODO vérifier --> Les prérequis de capacité et d'édition diffèrent selon l'expérience Power BI disponible. Le test, pas la seule taille de capacité, autorise le déroulement individuel de la section 5. Aucune copie du rapport n'est prévue dans le parcours nominal.

</div>

### Conventions et aide

- Le texte est français. **Ne traduisez jamais les identifiants en anglais**, ni les noms de fichiers, tables ou colonnes.
- `lh_lab` et les autres noms d'items sont identiques pour chacun : les workspaces sont séparés. Les noms exacts des workspaces sont sur votre fiche.
- Les lakehouses, warehouses, tables et colonnes utilisent des lettres, chiffres et underscores, sans espace ni tiret. Les tirets de `ws-lab-...` concernent uniquement le nom du workspace.
- Une ligne numérotée correspond à une action. Les libellés d'interface sont entre « guillemets ». Certaines versions gardent un libellé anglais ; demandez son équivalent à l'animateur.
- Un encadré « Point de contrôle » indique le résultat attendu. Arrêtez-vous au contrôle avant de poursuivre.
- En parcours 3 h, laissez « Comprendre » replié. Le T-SQL replié est une variante facultative, jamais un prérequis du parcours métiers.

Pour demander de l'aide, indiquez la section et le numéro de l'étape dans le canal de votre fiche. Joignez le message d'erreur sans identifiant sensible. Ne publiez ni jeton, ni mot de passe, ni URL privée dans le dépôt GitHub. En présentiel, signalez votre blocage à l'animateur.

<details>
<summary>Contexte (optionnel) : les unités et le périmètre</summary>

Un **kWh** mesure une quantité d'énergie. Un **kW** mesure une puissance. Un **kgCO2e** exprime une masse de gaz à effet de serre ramenée à un équivalent CO2. Multiplier les kWh par un facteur en kgCO2e/kWh donne une estimation en kgCO2e.

Le fichier annuel couvre l'année civile 2025. Le « dernier jour disponible » est le 31 décembre 2025, pas aujourd'hui. Les deux énergies sont additionnables en kWh, mais elles n'ont pas le même facteur carbone. Les lignes supprimées au nettoyage sont des observations manquantes, pas des consommations égales à zéro.

</details>

### Auteur

**Amine Lemsih** : conception et rédaction de l'atelier. Contact : **@aminelemsih**. Les animateurs réutilisent le kit sans ajouter de contexte client au document public.

---

## 1. Prise en main

**Pourquoi c'est important pour Contoso**

Tous les sites doivent utiliser le même référentiel de bâtiments et les mêmes facteurs d'émission.  
Un raccourci évite les copies qui divergent entre équipes.

**Objectif :** créer votre lakehouse et accéder aux deux tables de référence sans les copier.

**Durée : 20 min de pratique ; 5 min « Comprendre » en parcours complet.**

### Ouvrir votre espace

1. Ouvrez le lien Fabric de votre fiche participant.
2. Connectez-vous avec le compte indiqué.
3. Sélectionnez « Espaces de travail ».
4. Ouvrez votre workspace personnel indiqué sur la fiche.
5. Vérifiez que vous n'êtes pas dans l'espace commun.
6. Sélectionnez « Nouvel élément ».
7. Recherchez « Lakehouse ».
8. Sélectionnez « Lakehouse ».
9. Saisissez `lh_lab` comme nom.
10. Laissez « Schémas de lakehouse » activé. <!-- TODO vérifier -->
11. Sélectionnez « Créer ».

![Lakehouse lh_lab dans le workspace personnel, avec les zones Tables et Fichiers](assets/01-lakehouse.png)

### Créer les raccourcis

1. Développez « Tables » dans `lh_lab`.
2. Ouvrez le menu du schéma `dbo`. <!-- TODO vérifier -->
3. Sélectionnez « Nouveau raccourci ».
4. Choisissez « Microsoft OneLake ».
5. Sélectionnez le workspace commun indiqué sur votre fiche.
6. Sélectionnez `lh_source`.
7. Sélectionnez « Suivant ».
8. Développez les tables du schéma `dbo` de la source.
9. Cochez `sites`.
10. Cochez `emission_factors`.
11. Sélectionnez « Suivant ».
12. Vérifiez les deux noms de raccourcis.
13. Sélectionnez « Créer ».
14. Ouvrez le raccourci `sites`.
15. Repérez `site_id`, `region` et `opening_date` dans l'aperçu.
16. Ouvrez le raccourci `emission_factors`.
17. Repérez l'année 2025 et les deux coefficients.
18. Ouvrez les propriétés d'un raccourci. <!-- TODO vérifier -->
19. Vérifiez que la cible reste `lh_source` dans l'espace commun.

Si l'assistant ne permet qu'une sélection, créez `sites`, puis répétez les mêmes étapes pour `emission_factors`.

![Deux raccourcis de tables vers lh_source et propriétés indiquant la cible commune](assets/01-onelake-shortcuts.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir `sites` et `emission_factors` sous `lh_lab`, avec l'indication de raccourci. Le référentiel contient 30 sites. Les facteurs contiennent une ligne pour 2025 et deux coefficients : 0,055 et 0,205. Vous n'avez lancé aucune activité de copie de ces tables.

</div>

### Si ça bloque

- **Source invisible :** vérifiez le tenant et le workspace de la fiche. L'animateur contrôle le rôle Viewer.
- **Table visible mais données refusées :** faites vérifier le partage explicite ReadAll de `lh_source` et la propagation des permissions.
- **Nom refusé ou schéma introuvable :** utilisez `lh_lab`, avec underscore. Ne créez pas un dossier `dbo` dans « Fichiers ». L'animateur adapte le chemin si le lakehouse source est sans schémas.

<details>
<summary>Comprendre : partager une référence, pas une copie (5 min)</summary>

Le raccourci stocke une référence vers la table source. Les moteurs consultent les données autorisées à cette cible. Les fichiers peuvent être mis en cache par les moteurs, mais il n'existe pas une seconde table métier indépendante à tenir à jour.

Utilisez ce mécanisme pour des référentiels ou des données gouvernées communes. Il ne remplace ni une sauvegarde ni un transfert de propriété. La suppression de la source ou le retrait des permissions peut casser la lecture du raccourci. Donner Membre dans votre workspace ne vous donne pas l'écriture sur la source commune.

</details>

---

## 2. Ingestion

**Pourquoi c'est important pour Contoso**

Les relevés énergétiques arrivent sous forme de fichiers imparfaits.  
Un nettoyage reproductible rend les analyses comparables d'un jour à l'autre.

**Objectif :** alimenter `consumption` avec un flux visuel et planifier son exécution quotidienne.

**Durée : 35 min de pratique ; 5 min « Comprendre » en parcours complet ; pause de 15 min ensuite.**

**Power Query** est l'éditeur de transformations visuelles utilisé par Dataflow Gen2. Une **destination** est la table dans laquelle le flux écrit son résultat.

### Créer le flux

1. Revenez à votre workspace personnel.
2. Sélectionnez « Nouvel élément ».
3. Recherchez « Dataflow Gen2 ».
4. Sélectionnez « Dataflow Gen2 ».
5. Nommez le flux `df_energy` dans le champ de nom proposé. <!-- TODO vérifier -->
6. Ouvrez « Obtenir des données ».

Choisissez **une seule variante**, celle indiquée sur votre fiche. Elles utilisent le même fichier `consumption_2025.csv`.

### Variante A : fichier dans lh_source

1. Recherchez le connecteur « Lakehouse ».
2. Sélectionnez ce connecteur.
3. Choisissez l'authentification « Compte d'organisation ».
4. Sélectionnez « Se connecter » si nécessaire.
5. Sélectionnez « Suivant ».
6. Développez le workspace commun de votre fiche dans le navigateur de données.
7. Développez `lh_source`.
8. Développez « Fichiers ». <!-- TODO vérifier -->
9. Sélectionnez `consumption_2025.csv`.
10. Ouvrez son contenu binaire si le navigateur le présente comme « Binary ». <!-- TODO vérifier -->
11. Choisissez le format « Texte/CSV » si demandé.
12. Définissez la virgule comme séparateur.
13. Définissez UTF-8 comme encodage.
14. Sélectionnez « Créer » ou « Transformer les données » selon l'assistant. <!-- TODO vérifier -->

![Sélection du CSV annuel dans les fichiers du lakehouse source](assets/02-lakehouse-source.png)

### Variante B : fichier dans SharePoint

1. Recherchez « Dossier SharePoint ».
2. Sélectionnez ce connecteur.
3. Saisissez l'URL du **site SharePoint** indiquée sur votre fiche, pas le lien de partage du fichier.
4. Choisissez « Compte d'organisation ».
5. Sélectionnez « Se connecter » si nécessaire.
6. Sélectionnez « Suivant ».
7. Ouvrez le filtre de la colonne `Name`.
8. Conservez uniquement `consumption_2025.csv`.
9. Ouvrez le filtre de `Folder Path`.
10. Conservez uniquement le dossier indiqué sur votre fiche.
11. Ouvrez la valeur binaire de la colonne `Content` de l'unique fichier retenu. <!-- TODO vérifier -->
12. Définissez la virgule comme séparateur.
13. Définissez UTF-8 comme encodage.
14. Ouvrez l'éditeur de transformation.

![Filtrage d'un seul fichier annuel dans le dossier SharePoint autorisé](assets/02-sharepoint-source.png)

### Nettoyer et typer

Vous devez travailler sur six colonnes : `site_id`, `date`, `year`, `kwh_elec`, `kwh_gas`, `avg_temp`. Si la première ligne contient encore leurs noms, appliquez « Utiliser la première ligne pour les en-têtes ».

1. Renommez la requête `consumption`.
2. Ouvrez « Accueil ».
3. Ouvrez « Supprimer les lignes ».
4. Choisissez « Supprimer les lignes vides ».
5. Sélectionnez `site_id`.
6. Choisissez le type « Texte ».
7. Sélectionnez `date`.
8. Choisissez le type « Date ».
9. Sélectionnez `year`.
10. Choisissez le type « Nombre entier ».
11. Sélectionnez `kwh_elec`.
12. Ajoutez `kwh_gas` à la sélection avec Ctrl.
13. Ajoutez `avg_temp` à la sélection avec Ctrl.
14. Ouvrez « Modifier le type ».
15. Choisissez « Utiliser les paramètres régionaux ». <!-- TODO vérifier -->
16. Choisissez « Nombre décimal ».
17. Choisissez « Anglais (États-Unis) » pour lire le point décimal du CSV.
18. Validez.
19. Sélectionnez les six colonnes.
20. Ouvrez « Supprimer les lignes ».
21. Choisissez « Supprimer les erreurs ».
22. Sélectionnez `date`.
23. Ouvrez « Ajouter une colonne ».
24. Ouvrez « Date ».
25. Ouvrez « Mois ».
26. Choisissez « Début du mois ». <!-- TODO vérifier -->
27. Renommez la colonne ajoutée `month_start`.
28. Vérifiez que son type est « Date ».

![Étapes de nettoyage, types des colonnes et colonne month_start](assets/02-cleaning.png)

<div class="important" data-title="Une erreur n'est pas une consommation nulle">

> Le fichier contient 55 enregistrements vides et 55 valeurs `invalid`. Ne remplacez pas ces erreurs par zéro. Les 110 observations sont exclues de l'analyse. Les lignes à zéro avant l'ouverture d'un site sont valides et restent présentes. L'aperçu Power Query peut être limité : ne confondez pas son nombre de lignes avec le volume complet.

</div>

### Écrire dans le lakehouse

1. Sélectionnez la requête `consumption`.
2. Ouvrez « Ajouter une destination de données ».
3. Choisissez « Lakehouse ».
4. Sélectionnez votre workspace personnel.
5. Sélectionnez `lh_lab`.
6. Sélectionnez le schéma `dbo`.
7. Choisissez une nouvelle table.
8. Saisissez `consumption`.
9. Choisissez la méthode de mise à jour « Remplacer ». <!-- TODO vérifier -->
10. Vérifiez la correspondance des sept colonnes.
11. Validez la destination.
12. Sélectionnez « Publier » ou « Enregistrer et exécuter » selon la version. <!-- TODO vérifier -->
13. Exécutez le flux si la publication ne l'a pas déjà lancé.
14. Ouvrez son historique d'actualisation.
15. Attendez l'état de réussite.
16. Contrôlez avec l'animateur les lignes écrites dans les détails de l'exécution. <!-- TODO vérifier -->
17. Ouvrez `lh_lab`.
18. Actualisez la liste de ses tables.
19. Ouvrez `consumption`.

![Destination dbo.consumption dans lh_lab en mode Remplacer](assets/02-destination.png)

### Orchestrer et planifier

1. Revenez à votre workspace personnel.
2. Sélectionnez « Nouvel élément ».
3. Choisissez « Pipeline de données ».
4. Saisissez `pl_energy_daily`.
5. Sélectionnez « Créer ».
6. Ouvrez « Activités ».
7. Ajoutez une activité « Dataflow ».
8. Sélectionnez cette activité.
9. Ouvrez ses « Paramètres ».
10. Sélectionnez votre workspace.
11. Sélectionnez `df_energy`.
12. Enregistrez le pipeline.
13. Sélectionnez « Exécuter ».
14. Vérifiez la réussite de l'activité.
15. Ouvrez « Planifier ». <!-- TODO vérifier -->
16. Activez la planification.
17. Choisissez la fréquence « Quotidienne ».
18. Renseignez l'heure de votre fiche.
19. Renseignez le fuseau horaire de votre fiche.
20. Renseignez la date de fin de votre fiche pour limiter les exécutions après l'atelier.
21. Enregistrez la planification.

![Pipeline avec activité Dataflow et planification quotidienne bornée](assets/02-pipeline-schedule.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir la table `consumption` avec sept colonnes et **10 840 lignes** après nettoyage, le flux et le pipeline réussis, et une planification quotidienne. Après la seconde exécution, il reste 10 840 lignes : le mode « Remplacer » ne cumule pas les chargements.

</div>

### Si ça bloque

- **Fichier refusé ou plusieurs fichiers importés :** vérifiez ReadAll pour la variante A ; vérifiez l'URL du site, `Name` et `Folder Path` pour la variante B.
- **Décimaux ou dates en erreur :** vérifiez la locale de conversion et l'ordre des étapes. Les valeurs `invalid` sont les seules erreurs de type attendues dans le jeu fourni.
- **Échec de destination ou doublons :** vérifiez `lh_lab` dans votre espace, les autorisations de la connexion et « Remplacer ». Ne relancez pas en boucle un flux qui échoue.

<details>
<summary>Comprendre : préparer les données et organiser le travail (5 min)</summary>

Dataflow Gen2 mémorise des transformations Power Query. À l'exécution, il relit la source et écrit le résultat. Le pipeline orchestre cette exécution ; il ne corrige pas lui-même le fichier.

Utilisez un flux pour des préparations récurrentes accessibles aux analystes. Utilisez un pipeline pour organiser plusieurs activités et leur calendrier. Le mode « Remplacer » convient au petit historique complet du lab. En production, il faut traiter les mises à jour incrémentales, les rejets, les responsabilités et le suivi des coûts. Une donnée absente n'est pas réparée par une planification.

</details>

<div class="info" data-title="Pause : 15 minutes">

> La pause commence maintenant. L'animateur annonce l'heure de reprise. Laissez les éléments ouverts ; ne supprimez rien.

</div>

---

## 3. Exploration

**Pourquoi c'est important pour Contoso**

Des kWh seuls ne permettent pas de comparer l'empreinte carbone des régions.  
Une analyse partagée doit appliquer les bons facteurs sans multiplier les observations.

**Objectif :** produire une vue de la consommation et des kgCO2e par région et par mois, sans écrire de requête.

**Durée : 25 min de pratique ; 5 min « Comprendre » en parcours complet.**

Le **point de terminaison SQL** expose les tables Delta du lakehouse pour leur lecture avec SQL, un langage de requête. Une **jointure** rapproche des tables par une clé commune. Une **vue** conserve une définition de requête, pas une nouvelle copie des résultats.

### Ouvrir la requête visuelle

1. Ouvrez `lh_lab`.
2. Ouvrez « Analyser les données avec ». <!-- TODO vérifier -->
3. Choisissez « Point de terminaison d'analytique SQL ». <!-- TODO vérifier -->
4. Actualisez l'explorateur.
5. Vérifiez la présence de `consumption`, `sites` et `emission_factors`.
6. Sélectionnez « Nouvelle requête visuelle ».
7. Nommez-la `q_energy_monthly`.
8. Faites glisser `consumption` sur le canevas.
9. Faites glisser `sites` sur le canevas.
10. Faites glisser `emission_factors` sur le canevas.

### Rapprocher les tables

1. Ouvrez le menu du bloc `consumption`.
2. Sélectionnez « Fusionner les requêtes ». <!-- TODO vérifier -->
3. Choisissez `sites` comme seconde table.
4. Sélectionnez `site_id` dans la première table.
5. Sélectionnez `site_id` dans la seconde table.
6. Choisissez la jointure « Externe gauche ».
7. Validez.
8. Ouvrez le bouton de développement de la colonne issue de `sites`.
9. Conservez seulement `region`.
10. Décochez l'option de préfixe du nom de colonne. <!-- TODO vérifier -->
11. Validez.
12. Ouvrez le menu du résultat fusionné.
13. Sélectionnez « Fusionner les requêtes ».
14. Choisissez `emission_factors` comme seconde table.
15. Sélectionnez `year` dans la première table.
16. Sélectionnez `year` dans la seconde table.
17. Choisissez « Externe gauche ».
18. Validez.
19. Développez la colonne issue de `emission_factors`.
20. Conservez `elec_kgco2e_per_kwh`.
21. Conservez aussi `gas_kgco2e_per_kwh`.
22. Décochez l'option de préfixe.
23. Validez.

La table des facteurs possède **une seule ligne par année**, avec deux colonnes de coefficients. Chaque observation doit donc rester une seule observation après la jointure. Ne joignez jamais les deux énergies comme deux lignes sans adapter le schéma.

![Jointures visuelles sur site_id puis year sans duplication des observations](assets/03-visual-joins.png)

### Calculer et regrouper

1. Sélectionnez `kwh_elec`.
2. Ajoutez `elec_kgco2e_per_kwh` à la sélection avec Ctrl.
3. Dans « Ajouter une colonne », ouvrez « Standard ». <!-- TODO vérifier -->
4. Choisissez « Multiplier » pour les deux colonnes sélectionnées. <!-- TODO vérifier -->
5. Renommez la colonne obtenue `elec_kgco2e`.
6. Sélectionnez `kwh_gas`.
7. Ajoutez `gas_kgco2e_per_kwh` à la sélection avec Ctrl.
8. Choisissez de nouveau « Multiplier » dans « Ajouter une colonne ».
9. Renommez le résultat `gas_kgco2e`.
10. Sélectionnez `elec_kgco2e`.
11. Ajoutez `gas_kgco2e` à la sélection avec Ctrl.
12. Choisissez « Ajouter » dans « Standard ». <!-- TODO vérifier -->
13. Renommez le résultat `kgco2e`.
14. Sélectionnez `kwh_elec`.
15. Ajoutez `kwh_gas` à la sélection avec Ctrl.
16. Choisissez « Ajouter » dans « Standard ».
17. Renommez le résultat `total_kwh`.
18. Sélectionnez « Regrouper par ».
19. Choisissez le mode « Avancé ».
20. Ajoutez `region` comme première clé.
21. Ajoutez `month_start` comme seconde clé.
22. Ajoutez l'agrégation `total_kwh`, opération « Somme », sur `total_kwh`.
23. Ajoutez l'agrégation `kgco2e`, opération « Somme », sur `kgco2e`.
24. Ajoutez `observation_count`, opération « Nombre de lignes ».
25. Validez.
26. Ouvrez le filtre de `kgco2e`.
27. Choisissez le tri décroissant pour examiner les résultats.

### Enregistrer la vue

1. Sélectionnez la dernière étape du résultat agrégé.
2. Vérifiez « Activer le chargement » dans son menu. <!-- TODO vérifier -->
3. Retirez l'étape de tri dans les étapes appliquées avant de créer la vue.
4. Sélectionnez « Enregistrer comme vue ».
5. Choisissez le schéma `dbo`.
6. Saisissez `v_energy_monthly`.
7. Confirmez l'enregistrement.
8. Actualisez l'explorateur.
9. Ouvrez la vue créée.

Le tri sert à l'exploration. Une vue SQL ne garantit pas l'ordre de ses lignes. Il sera choisi à la lecture ou dans le rapport. Toutes les transformations doivent pouvoir être traduites en SQL par l'éditeur ; l'animateur vérifie ce parcours visuel avant la session. <!-- TODO vérifier -->

![Vue v_energy_monthly avec région, mois, énergie, émissions et nombre d'observations](assets/03-monthly-view.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir `v_energy_monthly`, avec **72 couples région/mois** : six régions et douze mois. La somme des `observation_count` vaut 10 840. Les totaux ne doivent pas doubler après la jointure des facteurs. L'animateur dispose du corrigé calculé pour comparer les résultats.

</div>

### Si ça bloque

- **Table absente du point de terminaison SQL :** la synchronisation peut prendre du temps. Vérifiez d'abord la table ou le raccourci dans le lakehouse, puis actualisez l'explorateur.
- **Totaux doublés ou facteurs vides :** vérifiez les clés `site_id` et `year`, leurs types et l'unicité de `emission_factors.year`.
- **Vue impossible à enregistrer :** retirez le tri et repérez l'étape non traduisible. Faites intervenir l'animateur ; ne remplacez pas spontanément l'exercice métiers par du code.

<details>
<summary>Variante T-SQL (optionnelle, hors parcours métiers sans code)</summary>

Sur le **point de terminaison SQL** de `lh_lab`, ouvrez une nouvelle requête SQL. La variante utilise les mêmes tables et la même définition métier. Le schéma est `dbo`.

```sql
-- Créer ou remplacer la définition, sans copier les résultats.
CREATE OR ALTER VIEW dbo.v_energy_monthly AS
SELECT
    sites.region,
    consumption.month_start,
    COUNT_BIG(*) AS observation_count,
    SUM(consumption.kwh_elec + consumption.kwh_gas) AS total_kwh,
    SUM(consumption.kwh_elec * factors.elec_kgco2e_per_kwh
      + consumption.kwh_gas * factors.gas_kgco2e_per_kwh) AS kgco2e
FROM dbo.consumption AS consumption
LEFT JOIN dbo.sites AS sites
    ON sites.site_id = consumption.site_id
LEFT JOIN dbo.emission_factors AS factors
    ON factors.[year] = consumption.[year]
GROUP BY sites.region, consumption.month_start;
```

Exécutez cette seconde requête séparément :

```sql
-- Le tri est une propriété de la lecture, pas de la vue.
SELECT region, month_start, observation_count,
       ROUND(total_kwh, 2) AS total_kwh,
       ROUND(kgco2e, 2) AS kgco2e
FROM dbo.v_energy_monthly
ORDER BY kgco2e DESC, region, month_start;
```

</details>

<details>
<summary>Comprendre : une même donnée, plusieurs lectures (5 min)</summary>

Le point de terminaison SQL lit les tables Delta. Il peut conserver une définition de vue, mais ne permet pas d'écrire les relevés comme un warehouse. Le lakehouse et la vue ne sont donc pas deux bases contenant deux copies des consommations.

Utilisez la vue pour une logique de lecture partagée. Le calcul carbone dépend de la validité des clés et des coefficients. Le moteur ne sait pas qu'une jointure a doublé vos résultats. Une vue agrégée perd aussi le détail : le data agent doit conserver l'accès aux tables pour retrouver un jour anormal.

</details>

---

## 4. Data agent

**Pourquoi c'est important pour Contoso**

Les équipes métiers veulent interroger les données avec leurs propres mots.  
Les définitions et les contrôles évitent qu'une réponse plausible devienne une décision erronée.

**Objectif :** améliorer et vérifier les réponses de `energy_agent` à six questions métier.

**Durée : 30 min de pratique ; 5 min « Comprendre » en parcours complet.**

### Créer l'agent

1. Revenez à votre workspace personnel.
2. Sélectionnez « Nouvel élément ».
3. Recherchez « Agent de données Fabric ». <!-- TODO vérifier -->
4. Sélectionnez cet élément.
5. Saisissez `energy_agent`.
6. Sélectionnez « Créer ».
7. Choisissez `lh_lab` dans le catalogue des sources.
8. Sélectionnez « Ajouter ».
9. Cochez `consumption` dans l'explorateur de l'agent.
10. Cochez `sites`.
11. Cochez `emission_factors`.
12. Décochez les autres tables ou vues si elles sont proposées.

![Agent energy_agent avec les trois tables autorisées de lh_lab](assets/04-agent-sources.png)

### Poser les six questions avant configuration

1. Posez Q1 dans la zone de conversation.
2. Développez les étapes de la réponse. <!-- TODO vérifier -->
3. Repérez la source choisie et la requête générée, sans la modifier.
4. Notez le résultat et l'unité dans votre fiche de comparaison privée.
5. Répétez ces quatre actions pour Q2 à Q6, dans l'ordre.

| Question | Texte à poser |
| --- | --- |
| Q1 | Quelle est la consommation électrique totale observée en 2025, en kWh ? |
| Q2 | Quelle région émet le plus de kgCO2e en 2025, électricité et gaz réunis ? |
| Q3 | Quel mois de 2025 a la consommation totale la plus élevée, en kWh ? |
| Q4 | Quels couples site et jour dépassent 20 000 kWh, électricité et gaz réunis, en 2025 ? |
| Q5 | Combien de sites étaient actifs au 1er janvier 2025 ? |
| Q6 | De quel pourcentage nos émissions ont-elles baissé entre 2024 et 2025 ? |

Pour Q2, cherchez dans les étapes l'usage des deux facteurs. Pour Q4, vérifiez que le seuil s'applique à un **site et un jour**, pas à une somme régionale. Pour Q6, vérifiez que l'agent reconnaît l'absence de 2024.

### Ajouter les définitions métier

1. Ouvrez « Instructions de l'agent de données ». <!-- TODO vérifier -->
2. Collez les instructions en français ci-dessous.
3. Enregistrez les instructions.

> Répondez en français. Utilisez uniquement les tables sélectionnées de lh_lab. Indiquez la période, l'unité, les tables et les limites des résultats.
>
> Les consommations kwh_elec et kwh_gas sont des énergies journalières en kWh, pas des puissances. La consommation totale est leur somme. L'année est l'année civile, du 1er janvier inclus au 1er janvier suivant exclu. Pour ce jeu, seule 2025 est disponible.
>
> Un site est actif à une date si opening_date est antérieure ou égale à cette date. Aucune fermeture n'est modélisée. Comptez les sites depuis sites, sans compter plusieurs fois les relevés quotidiens. Ne confondez pas site actif et consommation non nulle.
>
> Reliez consumption.site_id à sites.site_id. Reliez consumption.year à emission_factors.year, unique par année. Utilisez elec_kgco2e_per_kwh pour l'électricité et gas_kgco2e_per_kwh pour le gaz. Additionnez les deux contributions en kgCO2e. Arrondissez après la somme. Les facteurs sont fictifs, ne pas utiliser pour un reporting réel.
>
> Les 110 observations rejetées au nettoyage sont absentes. Les totaux portent sur les observations conservées ; n'inventez pas leurs valeurs. Les six pics sont présents dans les données nettoyées. Pour une anomalie journalière, comparez la somme des deux énergies au seuil par couple site/date.
>
> Si une période ou une information manque, dites-le et demandez les données nécessaires. N'inventez pas de résultat pour 2024, de pourcentage de baisse, de cause de panne ou de facteur d'émission externe.

### Ajouter un exemple sans écrire de code

Un **exemple de requête** associe une question à une requête déjà vérifiée. Vous réutilisez ici une requête générée ; vous n'avez pas à l'écrire.

1. Posez de nouveau Q1 avec les instructions enregistrées.
2. Développez la requête générée.
3. Faites valider son résultat par l'animateur avec le corrigé.
4. Copiez la requête validée à l'aide du bouton de copie.
5. Ouvrez « Exemples de requêtes ». <!-- TODO vérifier -->
6. Sélectionnez la source `lh_lab`.
7. Sélectionnez « Ajouter un exemple ».
8. Saisissez Q1 comme question.
9. Collez la requête générée validée dans le champ de requête.
10. Lancez la validation de l'exemple. <!-- TODO vérifier -->
11. Enregistrez seulement si la validation réussit.

Ne prenez pas une requête qui échoue ou une réponse textuelle comme exemple SQL. Si Q1 n'est pas correcte, l'animateur la vérifie avec vous avant l'ajout.

### Comparer après configuration

1. Notez vos réponses initiales avant d'effacer la conversation.
2. Sélectionnez « Effacer la conversation ». <!-- TODO vérifier -->
3. Reposez Q1 à Q6.
4. Examinez les sources, requêtes et unités de chaque nouvelle réponse.
5. Complétez la comparaison privée.
6. Comparez avec le corrigé communiqué par l'animateur.

| Question | Résultat avant | Résultat après | Période et unité justes ? | Conforme au corrigé ? |
| --- | --- | --- | --- | --- |
| Q1 | À noter | À noter | À noter | À noter |
| Q2 | À noter | À noter | À noter | À noter |
| Q3 | À noter | À noter | À noter | À noter |
| Q4 | À noter | À noter | À noter | À noter |
| Q5 | À noter | À noter | À noter | À noter |
| Q6 | À noter | À noter | À noter | À noter |

![Comparaison avant/après avec instructions, exemple validé et requête consultable](assets/04-agent-comparison.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir les trois tables de l'agent, des instructions enregistrées et un exemple validé. Q4 doit retrouver six couples site/jour. Q5 doit compter 27 sites actifs au 1er janvier. Q6 doit signaler que le pourcentage est impossible à calculer sans 2024. Une erreur persistante est un résultat de test à documenter, pas à masquer.

</div>

### Si ça bloque

- **Élément agent absent :** l'animateur vérifie la capacité payante, la région et les paramètres tenant des data agents et de l'IA. Une capacité d'essai ne suffit pas à ce parcours.
- **Source vide ou refusée :** vérifiez la synchronisation SQL, les trois tables cochées et ReadAll sur la cible des raccourcis.
- **Réponse ou exemple incorrect :** vérifiez la requête et le schéma réels avec l'animateur. Testez les instructions en français avant diffusion. <!-- TODO vérifier --> Ne considérez jamais un texte assuré comme une preuve.

<details>
<summary>Comprendre : guider une réponse, pas garantir la vérité (5 min)</summary>

Le data agent s'appuie sur les schémas, les instructions et les exemples pour produire une requête. Le moteur de données exécute cette requête avec les autorisations applicables. Fabric gère le service d'IA intégré ; vous ne fournissez pas une clé Azure OpenAI dans ce lab.

Utilisez-le pour retrouver des faits et explorer des questions bien définies. Il ne remplace pas un contrôle des résultats, une définition d'indicateur ni une analyse causale. L'exemple aide pour certaines formes de questions ; il ne garantit pas les réponses suivantes. Des données absentes restent absentes, même après une meilleure instruction.

</details>

---

## 5. Alerte

**Pourquoi c'est important pour Contoso**

Une dérive peut rester invisible entre deux consultations du rapport.  
Une notification invite la bonne personne à examiner la situation au moment du dépassement.

**Objectif :** enregistrer une alerte personnelle sur le rapport partagé et observer son déclenchement.

**Durée : 15 min de pratique ; 5 min « Comprendre » en parcours complet.**

### Ouvrir le rapport commun

1. Ouvrez le lien du rapport indiqué sur votre fiche participant.
2. Vérifiez que le rapport est `energy_report` dans l'espace commun.
3. Repérez le visuel **« consommation du dernier jour disponible par région »**.
4. Vérifiez que le dernier jour disponible affiché est le 31 décembre 2025.
5. Vérifiez avec l'animateur que toutes les régions sont sous **20 000 kWh** dans l'état de départ.

Ne copiez pas le rapport. Vous restez lecteur dans l'espace commun. L'alerte, elle, sera enregistrée dans votre workspace personnel.

![Rapport partagé avec consommation du dernier jour disponible par région et courbe mensuelle](assets/05-energy-report.png)

### Définir votre règle

1. Ouvrez le menu « … » du visuel en barres.
2. Sélectionnez « Définir une alerte » ou « Ajouter une alerte ». <!-- TODO vérifier -->
3. Vérifiez la mesure `latest_day_kwh` dans le volet.
4. Vérifiez que la condition est évaluée pour chaque `region`.
5. Choisissez « Devient » dans la condition. <!-- TODO vérifier -->
6. Choisissez « Supérieur à ».
7. Saisissez `20000`.
8. Choisissez « Teams » comme canal de notification.
9. Choisissez votre propre compte comme destinataire.
10. Ouvrez « Sélectionner l'emplacement d'enregistrement ». <!-- TODO vérifier -->
11. Sélectionnez votre workspace personnel de la fiche.
12. Choisissez un nouvel élément Activator.
13. Nommez-le `act_energy`.
14. Confirmez l'emplacement.
15. Sélectionnez « Appliquer » ou « Créer » selon le volet. <!-- TODO vérifier -->
16. Vérifiez que l'alerte est active.

Le canal Teams de l'atelier sert à l'entraide. Il n'est **pas** le destinataire de cette alerte : vous vous envoyez un message personnel.

![Condition régionale de 20 000 kWh, notification Teams à soi et destination personnelle](assets/05-alert-settings.png)

<div class="warning" data-title="Si le bouton n'est pas disponible">

> Prévenez l'animateur. Ce chemin doit avoir été validé à J-7 avec les mêmes droits et la même capacité. La documentation décrit également une expérience demandant Edit sur le rapport. <!-- TODO vérifier --> Ne demandez pas l'écriture sur l'espace commun et ne créez pas une copie de votre propre initiative. L'animateur applique le plan B annoncé.

</div>

### Voir le déclenchement et ouvrir Activator

1. Signalez à l'animateur que votre règle est active.
2. Attendez sa confirmation que l'état sous le seuil a été observé.
3. Observez le changement du rapport après le remplacement du fichier par l'animateur et l'actualisation du modèle.
4. Ouvrez vos notifications Teams.
5. Repérez le message de dépassement pour la région concernée.
6. Revenez au volet d'alerte du rapport.
7. Ouvrez le menu de l'élément Activator.
8. Sélectionnez « Ouvrir dans Activator ». <!-- TODO vérifier -->
9. Ouvrez la règle dans `act_energy`.
10. Repérez la valeur observée, la condition, le destinataire et l'historique des actions. <!-- TODO vérifier -->

L'animateur remplace uniquement le fichier actif du dernier jour, recharge sa table puis actualise le modèle. Vous ne modifiez pas les données communes. Rafraîchir la page du navigateur n'actualise pas le modèle sémantique.

![Règle Activator personnelle, condition et historique d'action après franchissement](assets/05-activator-rule.png)

<div class="info" data-title="Sous le capot">

> Le même moteur Activator peut surveiller des flux temps réel et des événements Fabric. Selon la source, les permissions et les actions configurées, il peut envoyer un courriel, appeler un flux Power Automate ou déclencher un élément Fabric tel qu'un pipeline, sans code. Ce lab configure seulement une notification personnelle. La section 8 compare cette alerte sur rapport à une règle sur flux.

</div>

<div class="task" data-title="Point de contrôle">

> Vous devez voir `act_energy` dans **votre** workspace, une règle par région sur `latest_day_kwh`, le seuil de 20 000 kWh et votre compte comme destinataire. Après l'actualisation, une région franchit le seuil. La notification peut arriver après la fin du module : sa latence est mesurée à J-7. Si le plan B capture est utilisé, distinguez clairement la règle créée aujourd'hui de la notification reçue en répétition.

</div>

### Si ça bloque

- **Bouton absent ou destination refusée :** vérifiez le test J-7, le paramètre tenant autorisant les alertes et le rôle Membre dans votre workspace. La capacité F64 ne donne pas à elle seule de nouveaux droits.
- **Rapport inchangé :** l'animateur vérifie le remplacement du fichier, la réussite de `df_source_latest`, la table et l'actualisation de `sm_energy_report` avec son identité fixe.
- **Pas de notification :** vérifiez règle active, région, destinataire et observation des deux états. Les filtres du rapport sont capturés lors de la création de l'alerte ; les changer ensuite ne modifie pas la règle.

<details>
<summary>Comprendre : surveiller un état et déclencher une action (5 min)</summary>

Une règle combine des observations, une condition et une action. « Devient supérieur à » recherche un franchissement, pas simplement une valeur qui reste élevée. Le jeu avant/après crée ce changement de manière contrôlée.

Utilisez une alerte pour inviter à une vérification ou automatiser une réponse autorisée. Sur un rapport, le délai dépend de l'actualisation du modèle et de l'évaluation de la règle. Ce n'est pas la même latence qu'un événement reçu dans un flux. Une notification ne prouve pas une panne et ne doit pas engager une action irréversible sans contrôle adapté.

</details>

**Parcours métiers :** passez maintenant à la section 10, « Conclusion ». **Parcours complet :** poursuivez avec l'extension Entrepôt.

---

## 6. Extension : Entrepôt et T-SQL

**Pourquoi c'est important pour Contoso**

Certaines équipes souhaitent gérer leurs analyses avec des tables et des requêtes SQL.  
Un entrepôt leur fournit une surface d'écriture et de lecture adaptée à cette pratique.

**Objectif :** copier les données propres dans un warehouse et vérifier trois requêtes T-SQL.

**Durée : 30 min, parcours complet uniquement.**

Un **warehouse**, ou entrepôt, est un stockage analytique organisé en tables et piloté par SQL. **T-SQL** est le dialecte SQL utilisé par le warehouse Fabric. À partir de cette extension, des requêtes commentées sont fournies à copier-coller.

### Charger les tables par pipeline

1. Ouvrez votre workspace personnel.
2. Sélectionnez « Nouvel élément ».
3. Choisissez « Warehouse » ou « Entrepôt ». <!-- TODO vérifier -->
4. Saisissez `wh_energy`.
5. Sélectionnez « Créer ».
6. Revenez au workspace.
7. Créez un élément « Pipeline de données ».
8. Nommez-le `pl_energy_warehouse`.
9. Ajoutez une activité « Copier les données ».
10. Nommez l'activité `copy_consumption`.
11. Ouvrez l'onglet « Source ».
12. Sélectionnez le connecteur « Lakehouse ».
13. Sélectionnez `lh_lab` dans votre workspace.
14. Choisissez la table `dbo.consumption`.
15. Ouvrez « Destination ».
16. Sélectionnez `wh_energy`.
17. Choisissez « Créer automatiquement la table ». <!-- TODO vérifier -->
18. Saisissez `dbo` comme schéma.
19. Saisissez `consumption` comme table.
20. Ouvrez « Mappage ».
21. Sélectionnez « Importer les schémas ».
22. Vérifiez `date` et `month_start` de type Date.
23. Définissez les colonnes d'énergie et de température en `decimal(18,2)` dans la destination. <!-- TODO vérifier -->
24. Ouvrez « Paramètres ».
25. Activez la mise en zone intermédiaire, « Staging », si demandée. <!-- TODO vérifier -->
26. Choisissez « Espace de travail » comme stockage intermédiaire, sans créer de compte de stockage externe.
27. Enregistrez le pipeline.
28. Exécutez-le une première fois.
29. Vérifiez la réussite et les 10 840 lignes copiées.
30. Revenez aux paramètres de destination de l'activité.
31. Choisissez « Upsert » comme comportement d'écriture. <!-- TODO vérifier -->
32. Définissez `site_id` et `date` comme clés de correspondance.
33. Enregistrez.

**Upsert** met à jour une ligne dont la clé existe et insère une ligne nouvelle. Avec ce jeu fixe, une relance ne doit pas doubler les lignes. Ne relancez pas en mode « Insert » sans nettoyage de la destination.

1. Dupliquez l'activité sous le nom `copy_sites`.
2. Remplacez sa source par `dbo.sites` dans `lh_lab`.
3. Remplacez sa destination par `dbo.sites` dans `wh_energy`.
4. Réimportez son mappage.
5. Remplacez ses clés Upsert par `site_id` uniquement.
6. Dupliquez l'activité sous le nom `copy_emission_factors`.
7. Remplacez sa source par `dbo.emission_factors` dans `lh_lab`.
8. Remplacez sa destination par `dbo.emission_factors` dans `wh_energy`.
9. Réimportez son mappage.
10. Définissez les deux facteurs en `decimal(12,6)` pour préserver leur précision.
11. Remplacez ses clés Upsert par `year` uniquement.
12. Enregistrez le pipeline.
13. Exécutez le pipeline.
14. Vérifiez la réussite des trois activités.

Le chargement automatique avec Upsert et la sélection des clés doivent être testés sur la version du connecteur de la session. <!-- TODO vérifier --> Si cette combinaison n'est pas disponible, l'animateur prépare les tables de destination avant le lab ; n'improvisez pas une succession de chargements en ajout.

![Pipeline avec les trois tables copiées vers wh_energy et clés de mise à jour](assets/06-warehouse-pipeline.png)

### Exécuter trois requêtes guidées

1. Ouvrez `wh_energy`.
2. Sélectionnez « Nouvelle requête SQL ».
3. Collez la requête 1.
4. Sélectionnez « Exécuter ».
5. Comparez le nombre de lignes et la somme électrique au corrigé.

```sql
-- Requête 1 : contrôler le volume et les totaux observés en 2025.
SELECT COUNT_BIG(*) AS observation_count,
       ROUND(SUM(kwh_elec), 2) AS electricity_kwh,
       ROUND(SUM(kwh_gas), 2) AS gas_kwh
FROM dbo.consumption
WHERE [date] >= '2025-01-01' AND [date] < '2026-01-01';
```

Vous attendez **10 840 observations**, **2 896 164,51 kWh électriques** et **1 686 455,14 kWh de gaz**.

1. Ouvrez une seconde requête SQL.
2. Collez la requête 2.
3. Exécutez-la.
4. Comparez le classement régional à la réponse Q2 de l'agent.

```sql
-- Requête 2 : appliquer le facteur de chaque énergie pour la bonne année.
SELECT sites.region,
       ROUND(SUM(consumption.kwh_elec * factors.elec_kgco2e_per_kwh
               + consumption.kwh_gas * factors.gas_kgco2e_per_kwh), 2) AS total_kgco2e
FROM dbo.consumption AS consumption
JOIN dbo.sites AS sites ON sites.site_id = consumption.site_id
JOIN dbo.emission_factors AS factors ON factors.[year] = consumption.[year]
WHERE consumption.[date] >= '2025-01-01' AND consumption.[date] < '2026-01-01'
GROUP BY sites.region
ORDER BY total_kgco2e DESC, sites.region;
```

Les Hauts-de-France arrivent en tête, avec **133 453,59 kgCO2e fictifs**. Un résultat deux fois trop grand indique une erreur de données ou de jointure, pas une nouvelle découverte métier.

1. Ouvrez une troisième requête SQL.
2. Collez la requête 3.
3. Exécutez-la.
4. Comparez les six couples au corrigé de Q4.

```sql
-- Requête 3 : chercher les dépassements au grain site/jour, pas région/an.
SELECT consumption.site_id, sites.site_name, consumption.[date],
       consumption.kwh_elec + consumption.kwh_gas AS total_kwh
FROM dbo.consumption AS consumption
JOIN dbo.sites AS sites ON sites.site_id = consumption.site_id
WHERE consumption.[date] >= '2025-01-01' AND consumption.[date] < '2026-01-01'
  AND consumption.kwh_elec + consumption.kwh_gas > 20000
ORDER BY total_kwh DESC, consumption.site_id, consumption.[date];
```

### Conserver une vue

1. Ouvrez une nouvelle requête SQL dans `wh_energy`.
2. Collez cette définition.
3. Exécutez-la seule.
4. Actualisez l'explorateur.
5. Ouvrez `dbo.v_energy_monthly`.

```sql
-- Cette vue est dans le warehouse, distincte de celle du lakehouse.
CREATE OR ALTER VIEW dbo.v_energy_monthly AS
SELECT sites.region, consumption.month_start,
       SUM(consumption.kwh_elec + consumption.kwh_gas) AS total_kwh,
       SUM(consumption.kwh_elec * factors.elec_kgco2e_per_kwh
         + consumption.kwh_gas * factors.gas_kgco2e_per_kwh) AS kgco2e
FROM dbo.consumption AS consumption
JOIN dbo.sites AS sites ON sites.site_id = consumption.site_id
JOIN dbo.emission_factors AS factors ON factors.[year] = consumption.[year]
GROUP BY sites.region, consumption.month_start;
```

![Résultats SQL contrôlés et vue mensuelle dans le warehouse](assets/06-sql-results.png)

### Lakehouse ou warehouse ?

| Besoin | Choix à examiner |
| --- | --- |
| Fichiers variés, préparation de données, raccourcis OneLake, travail Spark | Lakehouse |
| Équipe SQL, tables analytiques, écritures T-SQL et transactions entre tables | Warehouse |
| Lire les tables du lakehouse en SQL sans les copier | Point de terminaison SQL du lakehouse |
| Partager des indicateurs Power BI | Modèle sémantique sur la source adaptée |

Dans cette extension, vous avez **copié** les tables pour apprendre l'entrepôt. Ce n'est pas une obligation de toute architecture Fabric.

<div class="task" data-title="Point de contrôle">

> Vous devez voir les trois tables et `v_energy_monthly` dans `wh_energy`. Les trois requêtes retrouvent les valeurs attendues. Après une relance du pipeline en Upsert, `consumption` conserve 10 840 lignes.

</div>

### Si ça bloque

- **Écriture SQL refusée :** vérifiez que vous êtes dans `wh_energy`, pas dans le point de terminaison SQL du lakehouse.
- **Copie en erreur :** contrôlez connexion, staging dans l'espace de travail, types de destination et disponibilité des raccourcis source.
- **Doublons ou Upsert refusé :** vérifiez les clés propres à chaque table. Upsert n'efface pas les doublons déjà créés par un chargement en ajout ; l'animateur remet la table de démonstration à zéro avant un nouvel essai.

<details>
<summary>Contexte (optionnel) : le choix appartient au besoin</summary>

Lakehouse et warehouse partagent OneLake, mais n'ont pas la même surface d'écriture. Choisissez en fonction des compétences, des formats et de la façon de gérer les données. Multiplier les copies augmente aussi les contrôles à maintenir.

</details>

---

## 7. Extension : Modèle sémantique Direct Lake

**Pourquoi c'est important pour Contoso**

Le même indicateur carbone doit garder sa définition d'un rapport à une conversation.  
Un modèle partagé rend explicites les relations, les unités et les calculs.

**Objectif :** créer un modèle Direct Lake sur `lh_lab` et l'interroger depuis le data agent.

**Durée : 25 min, parcours complet uniquement.**

Un **modèle sémantique** décrit les relations et les mesures utilisées pour analyser les données. **Direct Lake** permet au moteur Power BI de lire les tables Delta de OneLake sans construire une copie Import complète. Une **mesure DAX** est un calcul évalué selon les filtres de l'analyse.

### Créer explicitement le modèle

1. Ouvrez `lh_lab`.
2. Sélectionnez « Nouveau modèle sémantique ». <!-- TODO vérifier -->
3. Saisissez `sm_energy_lab`.
4. Choisissez votre workspace personnel.
5. Sélectionnez `consumption`.
6. Sélectionnez `sites`.
7. Sélectionnez `emission_factors`.
8. Créez le modèle.
9. Ouvrez le modèle en modification. <!-- TODO vérifier -->
10. Vérifiez le mode de stockage « Direct Lake » des tables.
11. Vérifiez avec l'animateur que le mode de connexion retenu pour ce modèle personnel utilise SSO. <!-- TODO vérifier -->

Ne sélectionnez pas `v_energy_monthly` : c'est une vue SQL, pas une table Delta physique. Une vue peut entraîner un chemin DirectQuery selon le type de modèle. **DirectQuery** interroge la source à chaque requête au lieu de charger ses colonnes en mémoire comme Direct Lake.

Il n'est pas nécessaire qu'un modèle par défaut existe dans le lakehouse. Vous venez d'en créer un explicitement. Les trois tables incluent les tables référencées par raccourci.

### Définir les relations

1. Ouvrez la vue « Modèle ».
2. Choisissez « Gérer les relations ». <!-- TODO vérifier -->
3. Créez une relation de `consumption.site_id` vers `sites.site_id`.
4. Choisissez la cardinalité « Plusieurs à un ».
5. Choisissez le filtrage « Simple », depuis `sites` vers `consumption`.
6. Laissez la relation active.
7. Enregistrez cette relation.
8. Créez une relation de `consumption.year` vers `emission_factors.year`.
9. Choisissez « Plusieurs à un ».
10. Choisissez le filtrage « Simple », depuis `emission_factors` vers `consumption`.
11. Laissez cette relation active.
12. Enregistrez.

S'il existe déjà une relation identique créée automatiquement, vérifiez-la au lieu d'en ajouter une seconde. `sites.site_id` et `emission_factors.year` doivent être uniques.

### Ajouter la mesure carbone

1. Sélectionnez `consumption` dans le modèle.
2. Choisissez « Nouvelle mesure ».
3. Collez la mesure ci-dessous.
4. Validez la formule.
5. Définissez son format numérique à deux décimales.
6. Ajoutez la description « Estimation fictive en kgCO2e, électricité et gaz, sur les observations disponibles ».
7. Enregistrez le modèle.

```dax
total_kgco2e =
// RELATED utilise la relation active vers l'unique ligne de facteurs de l'année.
SUMX(
    consumption,
    consumption[kwh_elec] * RELATED(emission_factors[elec_kgco2e_per_kwh])
        + consumption[kwh_gas] * RELATED(emission_factors[gas_kgco2e_per_kwh])
)
```

Le format d'affichage arrondit le résultat final. Ne remplacez pas cette expression par un arrondi des émissions de chaque observation.

![Modèle Direct Lake, relations à sens unique et mesure total_kgco2e](assets/07-direct-lake-model.png)

### Ajouter le modèle à l'agent

1. Ouvrez `energy_agent`.
2. Sélectionnez « Ajouter une source de données ».
3. Choisissez `sm_energy_lab`.
4. Sélectionnez « Ajouter ».
5. Complétez les instructions : « Pour les émissions agrégées, utilisez sm_energy_lab et la mesure total_kgco2e. Ne cumulez pas les résultats de ce modèle et de lh_lab : ils représentent les mêmes données. »
6. Enregistrez.
7. Démarrez une nouvelle conversation.
8. Reposez Q2 en précisant : « Utilisez uniquement sm_energy_lab et sa mesure total_kgco2e. »
9. Vérifiez la source et la requête DAX affichées dans les étapes.
10. Comparez la réponse à Q2 et à la requête SQL de la section 6.

Les exemples de requêtes SQL/KQL ne sont pas configurables pour une source modèle sémantique comme pour un lakehouse. Cela n'empêche pas l'agent de l'interroger. Ses mesures et métadonnées portent la définition métier.

![Le modèle sm_energy_lab comme source de l'agent et réponse carbone vérifiée](assets/07-agent-semantic-model.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir les deux relations plusieurs-vers-un et la mesure `total_kgco2e`. Le total 2025 vaut **505 012,35 kgCO2e fictifs**, et Q2 retrouve **133 453,59 kgCO2e** pour les Hauts-de-France. La trace de l'agent doit montrer le modèle choisi, pas une addition de deux sources.

</div>

### Si ça bloque

- **Relation impossible :** vérifiez les types des clés et l'absence de doublons du côté « un ».
- **Accès Direct Lake refusé :** contrôlez ReadAll sur `lh_source`, la cible des raccourcis et le propriétaire du modèle. En SSO, Membre de votre espace ne remplace pas la lecture de la source commune.
- **Mesure ou source absente :** vérifiez l'enregistrement du modèle et les permissions de lecture de l'agent. Ne confondez pas `sm_energy_lab` personnel avec `sm_energy_report`, le modèle commun à identité fixe.

<div class="info" data-title="Deuxième pause : 10 minutes">

> Cette pause appartient au parcours complet de 5 h. Reprenez ensuite à la section 8. Le bonus Copilot reste hors minutage.

</div>

---

## 8. Extension : Temps réel

**Pourquoi c'est important pour Contoso**

Un relevé quotidien ne suffit pas toujours pour comprendre une situation qui évolue rapidement.  
Le chemin événement, analyse, alerte prépare l'arrivée future de mesures plus fréquentes.

**Objectif :** observer un flux d'exemple, le requêter dans un Eventhouse et créer une règle Activator sur ce flux.

**Durée : 35 min, parcours complet uniquement.**

Un **Eventstream** reçoit et distribue des événements. Un **Eventhouse** héberge des bases optimisées pour les événements. **KQL**, ou Kusto Query Language, est le langage de requête utilisé ici.

<div class="important" data-title="Un échantillon technique, pas de l'énergie">

> Cette version utilise l'échantillon intégré « Bicycles ». Il décrit des stations de vélos. Ce ne sont pas des compteurs énergétiques Contoso et ses valeurs ne sont jamais des kWh. Vous apprenez un mécanisme réutilisable ; aucune jointure avec les consommations énergétiques n'est demandée.

</div>

### Créer les éléments et le flux

1. Revenez à votre workspace personnel.
2. Sélectionnez « Nouvel élément ».
3. Choisissez « Eventhouse ».
4. Saisissez `eh_sample`.
5. Créez l'élément.
6. Repérez sa base KQL, créée avec lui.
7. Revenez au workspace.
8. Créez un élément « Eventstream ».
9. Nommez-le `es_sample`.
10. Sélectionnez « Utiliser des données d'exemple ». <!-- TODO vérifier -->
11. Choisissez « Bicycles » dans les échantillons intégrés.
12. Nommez la source `sample_bicycles`.
13. Sélectionnez « Ajouter ».
14. Sélectionnez « Publier ».
15. Ouvrez l'aperçu des événements.
16. Repérez `Timestamp`, `BikepointID` et `No_Bikes` avec leur casse exacte. <!-- TODO vérifier -->

Le schéma des exemples intégrés peut évoluer. L'animateur le confirme à J-7. Si les champs diffèrent, adaptez leur mappage, pas leur sens. La documentation des [requêtes du tutoriel temps réel](https://learn.microsoft.com/fabric/real-time-intelligence/tutorial-5-query-data) illustre ces champs.

### Acheminer vers Eventhouse

1. Passez l'Eventstream en mode « Modifier ».
2. Sélectionnez « Ajouter une destination ».
3. Choisissez « Eventhouse ».
4. Nommez la destination `sample_storage`.
5. Choisissez le mode « Ingestion directe ». <!-- TODO vérifier -->
6. Sélectionnez votre workspace.
7. Sélectionnez `eh_sample`.
8. Sélectionnez sa base KQL.
9. Enregistrez la destination.
10. Reliez la sortie du flux à la destination si le lien n'est pas déjà présent.
11. Publiez l'Eventstream.
12. Ouvrez « Configurer » sur la destination. <!-- TODO vérifier -->
13. Créez la table `sample_events`.
14. Ouvrez le mappage des colonnes.
15. Mappez `Timestamp` vers `event_time`, type `datetime`.
16. Mappez `BikepointID` vers `station_id`, type `string`.
17. Mappez `No_Bikes` vers `bike_count`, type `long`.
18. Terminez l'assistant.
19. Ouvrez `sample_events` dans la base KQL.
20. Vérifiez que de nouvelles lignes arrivent.

![Eventstream avec source Bicycles et destination Eventhouse, sans source énergétique fictive](assets/08-eventstream-sample.png)

### Exécuter trois requêtes KQL

1. Ouvrez un « Jeu de requêtes KQL » dans votre workspace. <!-- TODO vérifier -->
2. Nommez-le `qs_sample`.
3. Connectez-le à la base de `eh_sample`.
4. Collez la requête 1.
5. Exécutez-la.
6. Vérifiez les trois colonnes et des valeurs non nulles.

```kql
// Requête 1 : examiner les derniers événements et vérifier le mappage.
sample_events
| project event_time, station_id, bike_count
| top 10 by event_time desc
```

1. Ouvrez un nouvel onglet du jeu de requêtes.
2. Collez la requête 2.
3. Exécutez-la.
4. Observez l'évolution sur les trente dernières minutes.

```kql
// Requête 2 : compter les événements, pas additionner des stocks de vélos.
sample_events
| where event_time > ago(30m)
| summarize event_count = count() by bin(event_time, 1m)
| order by event_time asc
| render timechart
```

1. Ouvrez un troisième onglet.
2. Collez la requête 3.
3. Exécutez-la.
4. Repérez les stations dont la dernière observation indique moins de cinq vélos.

```kql
// Requête 3 : ne garder que le dernier état récent de chaque station.
sample_events
| where event_time > ago(30m)
| summarize arg_max(event_time, bike_count) by station_id
| where bike_count < 5
| project station_id, event_time, bike_count
| order by bike_count asc, station_id
```

La troisième requête peut légitimement être vide. Une valeur de stock comme `bike_count` ne s'additionne pas sur toutes les observations pour déduire un total de vélos.

![Aperçu des événements, courbe du nombre d'événements et derniers états par station](assets/08-eventhouse-kql.png)

### Ajouter une règle sur le flux

1. Revenez au workspace.
2. Créez un élément « Activator » nommé `act_sample`.
3. Ouvrez `es_sample`.
4. Passez en mode « Modifier ».
5. Ajoutez une destination « Activator ». <!-- TODO vérifier -->
6. Nommez la destination `sample_alerts`.
7. Sélectionnez votre workspace.
8. Sélectionnez `act_sample`.
9. Enregistrez la destination.
10. Reliez-la à la sortie du flux.
11. Publiez.
12. Ouvrez `act_sample`.
13. Sélectionnez les événements reçus.
14. Créez un objet `station`, identifié par `BikepointID`. <!-- TODO vérifier -->
15. Choisissez `Timestamp` comme horodatage de l'événement.
16. Ajoutez la propriété numérique `bike_count` à partir de `No_Bikes`.
17. Créez une règle `low_bike_count`.
18. Choisissez une condition sur `bike_count` inférieur à `5`. <!-- TODO vérifier -->
19. Choisissez une notification Teams à votre propre compte.
20. Enregistrez la règle.
21. Démarrez-la.
22. Consultez les observations et l'historique des actions.

La destination Eventhouse a renommé ses colonnes par mappage. La destination Activator reçoit encore les champs du flux d'origine : c'est pourquoi elle utilise `BikepointID`, `Timestamp` et `No_Bikes` pour construire l'objet.

Si aucun événement ne satisfait la condition, l'animateur choisit avec vous un seuil de démonstration cohérent avec l'aperçu. Un bouton de test de notification, s'il est utilisé, vérifie le canal ; il ne prouve pas qu'un événement a franchi le seuil. <!-- TODO vérifier -->

![Règle Activator branchée sur le flux Bicycles avec identité de station et propriété numérique](assets/08-stream-activator.png)

### Relier les deux alertes

| Section 5 | Section 8 |
| --- | --- |
| Observe un résultat de modèle sémantique dans un rapport | Observe les événements d'un flux |
| Attend l'actualisation du modèle et l'évaluation | Dépend de l'arrivée et du traitement des événements |
| Objet suivi : région | Objet suivi : station |
| Valeur : kWh du dernier jour | Valeur : nombre de vélos de l'échantillon |
| Action : notification Teams personnelle | Même famille d'action et même moteur Activator |

<div class="task" data-title="Point de contrôle">

> Vous devez voir de nouvelles lignes dans `sample_events`, les résultats des trois requêtes et une règle active dans `act_sample`. Une notification n'est attendue que si la condition est satisfaite. Aucune valeur de cet échantillon n'entre dans le calcul carbone Contoso.

</div>

### Si ça bloque

- **Aucune ligne :** vérifiez la publication, les connexions du canevas et la fin de configuration de la destination Eventhouse.
- **Requête vide ou colonne absente :** contrôlez le mappage, la casse et l'horodatage. Si l'échantillon rejoue des dates anciennes, l'animateur adapte la fenêtre à la plage affichée ; n'effacez pas le filtre sans comprendre le périmètre.
- **Alerte muette ou répétitive :** vérifiez identité de station, propriété numérique, condition, règle démarrée et fréquence de notification. L'animateur arrête les règles et le flux après l'exercice pour éviter le bruit et les coûts.

---

## 9. Bonus : Copilot dans Fabric

**Pourquoi c'est important pour Contoso**

Une suggestion peut accélérer la préparation ou l'exploration d'une donnée.  
La responsabilité de vérifier les unités, les filtres et les résultats reste humaine.

**Objectif :** comparer une transformation et une requête proposées par Copilot à une intention métier explicite.

**Durée indicative : 15 min supplémentaires. Bonus, si le temps et les paramètres du tenant le permettent. Hors minutage des parcours 3 h et 5 h.**

**Copilot** est l'assistance générative intégrée à certaines expériences Fabric. Ce n'est ni le planificateur du pipeline ni une garantie de qualité des données. L'animateur vérifie sa disponibilité et les règles de traitement des données avant la session.

### Générer une transformation

1. Créez un nouveau Dataflow Gen2 nommé `df_energy_copilot` dans votre workspace.
2. Ajoutez une source « Lakehouse ».
3. Sélectionnez `lh_lab`.
4. Sélectionnez la table `consumption`, déjà nettoyée.
5. Ouvrez le volet « Copilot ». <!-- TODO vérifier -->
6. Demandez : « Ajoutez une colonne total_kwh qui additionne kwh_elec et kwh_gas. Conservez toutes les lignes et les colonnes existantes. »
7. Examinez les étapes proposées.
8. Vérifiez trois lignes de l'aperçu, dont une ligne à zéro.
9. Acceptez la proposition uniquement si elle correspond à la demande.
10. Enregistrez le brouillon sans destination de données.

Ne remplacez pas `df_energy` et ne choisissez pas `consumption` comme destination. Le bonus ne doit pas modifier la table utilisée par les autres exercices.

![Suggestion Copilot de total_kwh dans un flux distinct, sans écriture dans la table source](assets/09-copilot-transformation.png)

### Générer une requête en langage naturel

1. Ouvrez `qs_sample` créé à la section 8.
2. Ouvrez un nouvel onglet.
3. Ouvrez « Copilot » dans le jeu de requêtes. <!-- TODO vérifier -->
4. Demandez : « Dans sample_events, comptez les événements par minute sur les trente dernières minutes selon event_time, puis affichez une courbe. »
5. Examinez la proposition avant insertion.
6. Vérifiez qu'elle compte des événements et ne somme pas `bike_count`.
7. Insérez la proposition si elle est en lecture seule et conforme.
8. Exécutez-la.
9. Comparez-la à la requête 2 de la section 8 sur la même fenêtre.

![Question en français, KQL proposé et résultat comparé à une requête de référence](assets/09-copilot-query.png)

<div class="task" data-title="Point de contrôle">

> Vous devez voir une transformation conforme à la somme demandée et une requête limitée à la bonne table et à la bonne période. Vous devez pouvoir nommer au moins un contrôle effectué avant acceptation. Une fonction indisponible dans le tenant n'est pas un exercice échoué.

</div>

### Si ça bloque

- **Bouton absent :** vérifiez avec l'animateur les paramètres tenant, la région, la capacité et l'expérience concernée. Passez à la conclusion si les conditions ne sont pas réunies.
- **Suggestion incorrecte :** reformulez avec les noms exacts et un résultat attendu. N'acceptez pas une proposition pour simplement terminer le bonus.
- **Pas de données récentes :** vérifiez les dates de l'échantillon et la fenêtre de comparaison. Copilot ne crée pas les événements manquants.

---

## 10. Conclusion

**Pourquoi c'est important pour Contoso**

La valeur vient d'une chaîne comprise et contrôlée, pas d'une accumulation d'outils.  
Une prochaine expérimentation doit relier une décision métier à des données et à un responsable.

**Objectif :** retenir les usages pertinents et choisir un prochain cas d'application.

**Durée : 10 min dans les deux parcours.**

### Le chemin parcouru

| Étape | Ce que vous avez constaté |
| --- | --- |
| Partager | Les raccourcis réutilisent un référentiel autorisé. |
| Préparer | Le flux nettoie ; le pipeline orchestre ; les rejets restent documentés. |
| Analyser | Les clés, unités et facteurs contrôlent la qualité des résultats. |
| Questionner | Les instructions aident l'agent ; les résultats doivent être vérifiés. |
| Agir | Une règle observe une condition ; son action et sa latence doivent être testées. |
| Approfondir, parcours complet | Warehouse, Direct Lake et Eventhouse répondent à des besoins différents. |

![Récapitulatif des éléments créés et de leurs rôles dans le fil rouge](assets/10-recap.png)

1. Choisissez une décision métier que vous pourriez améliorer avec ce chemin.
2. Identifiez une source de données disponible et son responsable.
3. Notez un contrôle de qualité indispensable.
4. Notez une permission à faire valider.
5. Partagez votre prochaine étape dans le canal indiqué sur votre fiche.

### Et chez vous ?

Commencez par un périmètre limité : quelques bâtiments, une période, deux sources connues et un responsable de la décision. Définissez l'unité, les règles de nettoyage et le calcul attendu avant de demander une réponse à un agent. Remplacez les facteurs fictifs par des facteurs adaptés et documentés. Choisissez ensuite une alerte qui invite à une vérification utile, avec un destinataire et un délai acceptables.

L'animateur adapte ce paragraphe oralement ou dans les supports privés de la session. Aucun nom de client, lien de tenant ou objectif confidentiel ne doit être ajouté au workshop public.

### Fermer l'atelier

1. Enregistrez votre travail en cours.
2. Notez vos questions restantes dans votre fiche privée.
3. Signalez à l'animateur les pipelines, alertes et flux créés.
4. Attendez sa confirmation de prise en charge du nettoyage.
5. Fermez les onglets quand la collecte des travaux est terminée.

**Ne supprimez rien vous-même.** L'animateur arrête les planifications, les alertes et les flux, puis supprime les workspaces de la session à partir de son journal. Il gère la capacité selon l'accord de l'organisation. Un espace commun préexistant n'est pas supprimé automatiquement.

<div class="task" data-title="Point de contrôle">

> Vous devez voir votre travail enregistré et avoir transmis les éléments à arrêter. Vous savez distinguer données observées, données manquantes et réponses à vérifier. Les captures du brouillon et les tests tenant restent des prérequis de diffusion, pas des preuves de fonctionnement déjà réalisées.

</div>

### Si ça bloque

- **Travail non enregistré :** vérifiez l'état de sauvegarde avant de fermer l'onglet.
- **Question sans réponse :** transmettez section, étape et message d'erreur à l'animateur sans secret ni lien privé public.
- **Doute sur une suppression :** ne cliquez pas sur « Supprimer ». Seul l'animateur applique le nettoyage prévu.

### Takeaways

- [Découvrir Microsoft Fabric](https://learn.microsoft.com/fr-fr/fabric/get-started/microsoft-fabric-overview).
- [Créer un lakehouse : exercice Microsoft Learn](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/01-lakehouse.html).
- [Découvrir et connecter les données OneLake : exercice](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/25-discover-onelake.html).
- [Créer un Dataflow Gen2](https://learn.microsoft.com/fr-fr/fabric/data-factory/create-first-dataflow-gen2).
- [Analyser un warehouse : exercice](https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/06-data-warehouse.html).
- [Créer et configurer un data agent](https://learn.microsoft.com/fr-fr/fabric/data-science/how-to-create-data-agent).
- [Alertes Power BI et Activator](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/data-activator/activator-get-data-power-bi).
- [Sécurité de Direct Lake, SSO et identité fixe](https://learn.microsoft.com/fr-fr/fabric/fundamentals/direct-lake-security-integration).
- [Tutoriel Real-Time Intelligence](https://learn.microsoft.com/fr-fr/fabric/real-time-intelligence/tutorial-introduction).
- [Catalogue des exercices Microsoft Learn Fabric](https://microsoftlearning.github.io/mslearn-fabric/).
- [Mother Of All Workshops](https://aka.ms/moaw).

Ces ressources sont des prolongements. Les exercices de ce document ont été réécrits pour Contoso ; certains liens de référence sont en anglais.

### Contribuer

Signalez un libellé périmé, un résultat incohérent ou une difficulté reproductible dans les [issues du dépôt](https://github.com/aminelemsih/hands-on-lab-microsoft-fabric-end-to-end/issues). Proposez les corrections par demande de tirage. Utilisez uniquement des exemples synthétiques et des captures anonymisées. Conservez les identifiants anglais, l'attribution à Amine Lemsih et la licence CC BY-SA 4.0 du contenu.