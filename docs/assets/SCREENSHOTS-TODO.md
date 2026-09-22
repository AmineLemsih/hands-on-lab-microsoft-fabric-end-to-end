# Captures à réaliser

Une capture par **écran utile** : nouvelle page, boîte de dialogue ou résultat significativement modifié. Pas une capture par clic. Les indications *[capture : …]* placées dans [le workshop](../workshop.md) font foi : elles suivent les étapes et les points de contrôle des Labs 1 à 5. S3 et SharePoint sont des variantes, pas des obligations du parcours par défaut.

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

Ces trois schémas ne sont pas des captures de Fabric. L'architecture a deux formats d'export et une source éditable dans [../architecture.drawio](../architecture.drawio). Les Labs 1 à 5 utilisent des indications de capture visibles ; les extensions et le complément de répétition conservent leurs références commentées tant que les fichiers sont absents.

## Capturer en déroulant les Labs 1 à 5

Les emplacements sont intégrés dans les pages, au plus près de l'écran ou du contrôle concerné. Ils remplacent l'ancien catalogue fondé sur les numéros de clics : utilisez le libellé de l'indication, pas un ancien numéro d'étape.

| Lab | Indications de capture | Contenu |
| --- | ---: | --- |
| Lab 1 | 15 | Création, raccourcis, références et variante S3 |
| Lab 2 | 24 | Connexion, nettoyage, destination, pipeline et variante SharePoint |
| Lab 3 | 12 | Canevas, jointures, regroupement et vue |
| Lab 4 | 14 | Agent, réponses avant/après, instructions et exemple |
| Lab 5 | 11 | Rapport, règle, bascule coordonnée, Teams et historique |
| **Total** | **76** | Variantes et écrans de contrôle compris |

Après avoir réalisé et anonymisé un écran, ajoutez son PNG ici, puis remplacez la ligne *[capture : …]* correspondante par une référence Markdown :

```markdown
![Lakehouse lh_lab, zones Tables et Fichiers](assets/lab01-05-lakehouse-explorer.png)
```

Gardez l'indentation de la ligne quand elle appartient à une étape numérotée. Le nom suit `<lab>-<écran>-<sujet>.png`, avec un numéro d'écran stable par lab et un sujet anglais. Une capture doit montrer le résultat réellement obtenu ; signalez un écart plutôt que fabriquer l'état attendu.

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

La première commande traite les références Markdown déjà insérées : elle signale les fichiers présents/manquants, commente les captures absentes et décommente celles dont le fichier existe et n'est pas vide. Elle ne transforme pas les indications *[capture : …]* en liens et ne génère ni image ni bannière. Les trois schémas restent actifs par exception explicite. La seconde commande contrôle sans écrire ; son code vaut 1 seulement si une référence doit changer.

Avant commit : vérifier le cadre rouge, la lisibilité à 1600 px, les textes alternatifs, l'écran réellement testé et l'anonymisation. Aucun fichier image vide ne doit être ajouté pour contourner ce contrôle.