# Construire le rapport fourni

Le rapport `energy_report` est préparé par l'animateur, pas par les participants du parcours métiers. Aucun faux fichier `.pbix` ou `.pbip` n'est généré dans ce dépôt. Le dossier [energy_report](energy_report) est réservé à un **vrai projet Power BI** enregistré depuis Power BI Desktop.

## Résultat attendu

Une page et deux visuels, source `lh_source` dans le workspace commun indiqué par le lien de session :

| Visuel | Champs | Présentation |
| --- | --- | --- |
| Barres : **« consommation du dernier jour disponible par région »** | `sites.region`, mesure `latest_day_kwh` issue de `consumption_latest_day` | kWh, six régions, pas d'axe temporel, info-bulle `latest_available_date` |
| Courbe : **« consommation mensuelle 2025 »** | `consumption.month_start`, mesures `electricity_kwh` et `gas_kwh` | Axe chronologique ; séries renommées visuellement « Électricité » et « Gaz » ; kWh |

Les noms des mesures restent anglais. Les titres et libellés affichés sont français. Le modèle sémantique s'appelle `sm_energy_report` et utilise une connexion cloud à **identité fixe**. Le parcours recommandé du rapport est **Import** : il rend visible la dépendance à l'actualisation et convient au petit volume. L'extension 7 construit séparément un modèle Direct Lake en SSO.

## Préparation hors des dix minutes

Prévoir Power BI Desktop et une licence Power BI Pro pour l'auteur, les droits de publication dans l'espace commun et les règles d'authentification de l'organisation. Vérifier la disponibilité du format projet `.pbip` dans la version installée. <!-- TODO vérifier -->

Suivre [le guide des données](../data/README.md) pour préparer dans `lh_source` : la table `consumption` (consommation) nettoyée, 10 840 lignes avec `month_start` ; la table `consumption_latest_day` (consommation du dernier jour disponible), 30 lignes ; `sites`, 30 lignes ; `emission_factors`, une ligne.

Exécuter le notebook [setup_lh_source.ipynb](../setup/setup_lh_source.ipynb) attaché à `lh_source` : il prépare les quatre tables et initialise `consumption_latest_day` dans l'état `before`. Sa cellule 6 réalise la bascule `after` ; aucune combinaison de fichiers ni Dataflow de préparation supplémentaire n'est nécessaire.

Créer une connexion cloud `conn_energy_report` à identité fixe autorisée à lire le point de terminaison SQL de `lh_source`. Pour cette version Import, utiliser OAuth 2.0 avec une identité d'animation approuvée et stocker l'authentification dans le service, jamais dans le projet. Une identité de workspace est une variante possible si le connecteur et les paramètres tenant la prennent en charge. Aucune clé ni identité supplémentaire n'est provisionnée par le kit.

Le propriétaire du modèle doit pouvoir utiliser la connexion. Ne pas partager l'usage de la connexion avec tous les participants sans besoin : cela leur permettrait d'utiliser son identité dans leurs propres éléments. Ils n'ont besoin que de lire le rapport et le modèle communs.

## Construction et publication en dix minutes

Ce budget suppose les tables, les accès et la connexion préparés. L'actualisation initiale et les validations de tenant peuvent prendre plus longtemps ; ne pas les masquer dans le temps de construction.

### Minutes 0 à 3 : connecter et relier

1. Ouvrir Power BI Desktop.
2. Sélectionner « Obtenir des données ».
3. Choisir le connecteur « Base de données SQL Server ».
4. Saisir l'adresse du point de terminaison SQL de `lh_source` conservée dans les notes privées de session.
5. Saisir le nom de base correspondant à `lh_source` si demandé. <!-- TODO vérifier -->
6. Choisir « Importer ».
7. Se connecter avec le compte d'organisation autorisé.
8. Sélectionner `dbo.sites`.
9. Sélectionner `dbo.consumption`.
10. Sélectionner `dbo.consumption_latest_day`.
11. Charger les tables.
12. Ouvrir la vue « Modèle ».
13. Créer la relation `consumption.site_id` vers `sites.site_id`, plusieurs-vers-un, filtre simple depuis `sites`.
14. Créer la relation `consumption_latest_day.site_id` vers `sites.site_id`, plusieurs-vers-un, filtre simple depuis `sites`.
15. Vérifier les types Date et numériques.

Ne pas relier directement les deux tables de faits entre elles. Ne pas importer le CSV annuel sale. `emission_factors` n'est pas nécessaire aux deux visuels demandés ; le calcul carbone est pratiqué dans le workshop.

### Minutes 3 à 5 : définir les mesures

Créer chaque mesure séparément dans la table concernée. Les fonctions et séparateurs ci-dessous suivent la syntaxe DAX standard ; si la configuration Desktop impose des séparateurs localisés, faire adapter le paramètre par l'animateur. <!-- TODO vérifier -->

```dax
electricity_kwh =
// Total des observations électriques disponibles.
SUM(consumption[kwh_elec])
```

```dax
gas_kwh =
// Total des observations de gaz disponibles.
SUM(consumption[kwh_gas])
```

```dax
latest_available_date =
// Date maximale du jeu, indépendante du filtre région.
CALCULATE(MAX(consumption_latest_day[date]), REMOVEFILTERS(sites))
```

```dax
latest_day_kwh =
// Préserver le filtre région tout en sélectionnant le dernier jour disponible.
VAR latest_date =
    CALCULATE(MAX(consumption_latest_day[date]), REMOVEFILTERS(sites))
RETURN
    CALCULATE(
        SUM(consumption_latest_day[kwh_elec]) + SUM(consumption_latest_day[kwh_gas]),
        consumption_latest_day[date] = latest_date
    )
```

Formater les mesures d'énergie à deux décimales ; formater la date comme date. Ne pas utiliser `TODAY()` : le jeu reste daté de 2025.

### Minutes 5 à 8 : créer les deux visuels

1. Ajouter un graphique en barres groupées.
2. Affecter `sites.region` à l'axe des catégories.
3. Affecter `latest_day_kwh` à l'axe des valeurs.
4. Ajouter `latest_available_date` aux info-bulles.
5. Définir le titre exact « consommation du dernier jour disponible par région ».
6. Afficher les unités en kWh sans abréviation masquant le seuil.
7. Ajouter un graphique en courbes.
8. Affecter `consumption.month_start` à l'axe, sans hiérarchie automatique de dates.
9. Ajouter `electricity_kwh` aux valeurs.
10. Ajouter `gas_kwh` aux valeurs.
11. Renommer ces deux séries **pour ce visuel seulement** en « Électricité » et « Gaz ».
12. Définir le titre « consommation mensuelle 2025 ».
13. Filtrer ce visuel sur `year = 2025`.
14. Vérifier le tri chronologique de janvier à décembre.

Ne pas appliquer un filtre relatif aujourd'hui ni ajouter un axe temporel aux barres. Un filtre ou une sélection de mois sur la courbe ne doit pas modifier l'alerte : désactiver son interaction avec les barres, ou expliquer clairement les filtres capturés. <!-- TODO vérifier -->

### Minutes 8 à 10 : publier et relier la connexion

1. Enregistrer le projet réel sous le nom `energy_report` dans `report/energy_report/`.
2. Sélectionner « Publier ».
3. Choisir le workspace commun de la session.
4. Ouvrir le workspace dans le service.
5. Renommer le modèle sémantique publié `sm_energy_report` si Desktop lui a donné le nom du rapport.
6. Ouvrir ses « Paramètres ».
7. Ouvrir « Connexions de passerelle et cloud ». <!-- TODO vérifier -->
8. Associer la source à `conn_energy_report`.
9. Vérifier que SSO est désactivé pour cette connexion et que l'identité fixe approuvée porte la lecture. <!-- TODO vérifier -->
10. Appliquer la configuration.

Faire ensuite une actualisation du modèle et attendre sa réussite avant d'inviter les participants. En Import, le service utilise l'identité de la connexion pour charger les données ; les lecteurs ne passent pas leur identité à la source. Le ReadAll accordé sur `lh_source` reste nécessaire pour **leurs autres exercices**, indépendamment du rapport.

Référence : [connexions cloud partageables et identité fixe](https://learn.microsoft.com/power-bi/connect-data/service-connect-cloud-data-sources). Si l'animateur choisit ultérieurement Direct Lake pour le rapport fourni, vérifier [l'identité fixe pour les requêtes et l'actualisation](https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration), et répéter intégralement les tests d'alerte.

## Recette du rapport et de l'alerte

1. Se connecter avec un compte participant Viewer dans `ws-shared`, Membre dans son workspace, ReadAll sur `lh_source`.
2. Ouvrir `energy_report` depuis le lien privé.
3. Vérifier les six barres de l'état avant et la date du 31 décembre 2025.
4. Vérifier les deux séries mensuelles et les totaux annuels du corrigé.
5. Tester « Définir une alerte » sur les barres depuis ce compte lecteur. <!-- TODO vérifier -->
6. Enregistrer `act_energy` dans le workspace personnel, jamais dans `ws-shared`.
7. Tester la notification Teams personnelle avec un vrai franchissement avant/après.

La documentation [Activator sur rapport](https://learn.microsoft.com/fabric/real-time-intelligence/data-activator/activator-get-data-power-bi) décrit actuellement un chemin en édition. La disponibilité depuis un rapport partagé en lecture et la condition F64 ou supérieure doivent être vérifiées sur le tenant cible, **à J-7**, avant de garantir le lab individuel. <!-- TODO vérifier --> Prévoir une montée temporaire PAYG en F64 approuvée, puis refaire le test. Ne pas confondre les anciennes alertes de tuiles de dashboard avec les alertes Activator sur visuel de rapport.

Si la capacité n'est pas le blocage, F64 ne remplace pas des droits Edit. Ne pas ouvrir l'écriture sur le workspace commun. Annoncer une démonstration/capture ou valider séparément un autre mode de livraison. La copie par participant n'est pas le parcours par défaut.

## Faire partir l'alerte en section 5

Avant la session, exécuter les cellules 2 à 4 du notebook, puis actualiser le modèle. Toutes les régions sont alors sous 10 000 kWh, le seuil régional de l'alerte.

Après activation des règles et observation de cet état, passer `apply_after` à True dans la cellule 6 et exécuter uniquement cette cellule. Après réussite, remettre False, actualiser `sm_energy_report`, puis vérifier les barres. **Bretagne : 2 724,55 → 36 724,55 kWh**. Les autres régions ne changent pas. La mesure conserve le même nom et la même date de jeu.

Mesurer à J-7 l'intervalle entre la fin d'actualisation et la notification. Ne pas promettre une réception immédiate ou un délai fixe de 15 minutes. Conserver une capture de notification reçue en amont et de l'historique de règle. Le bouton de test d'action, s'il existe, ne remplace pas un test de franchissement réel.

## Versionner un vrai projet sans données client

Le dossier [energy_report](energy_report) ne contient pour le moment qu'un `.gitkeep`. Après construction réelle, il peut recevoir le `.pbip` et les dossiers Report/SemanticModel associés. Examiner chaque fichier avant commit : retirer ou paramétrer endpoints, noms de tenant, identifiants de connexion et liens privés selon une procédure testée. Tant que cela n'est pas fait, garder le projet **hors du dépôt public**. Les formats `.pbix` et les caches `.pbi/` sont ignorés ; un `.pbip` n'est pas automatiquement exempt de métadonnées sensibles.