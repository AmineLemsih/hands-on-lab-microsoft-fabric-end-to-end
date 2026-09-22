# Captures à réaliser

Une capture seulement pour un **écran où l'on peut se tromper** ou un **résultat à reconnaître**. Jamais pour un menu, un bouton évident ou une page d'accueil. Viser **6 à 8 captures par lab**, variantes comprises ; ne pas en ajouter pour atteindre un quota dans un lab court. Les indications *[capture : …]* placées dans [le workshop](../workshop.md) font foi. S3 et SharePoint restent facultatifs.

Format : PNG, **largeur 1600 px**, hauteur adaptée sans réduire le texte, interface française. Encadrer en **rouge** le contrôle ou le résultat à repérer ; garder assez de contexte pour reconnaître l'écran. Nom : `<lab>-<sujet>.png`, sujet anglais décrivant l'écran, sans numéro d'étape. Ne pas présenter une image recomposée comme une capture d'un comportement testé.

Le texte nomme ce que l'on cherche et les libellés de l'interface, pas la position d'un bouton : éviter « en haut à droite » ou « le troisième bouton ». Lors d'une répétition, refaire uniquement les captures dont l'écran ou le résultat a changé.

Seul « Contoso » peut apparaître comme organisation. Masquer les adresses de compte, avatars, autres noms de tenant, UUID, URLs privées, IDs de capacité, connexions privées et canaux identifiants. Les noms génériques d'items restent visibles. Aucune clé ni aucun jeton ne doit être capturé.

## Schémas pédagogiques livrés

| Fichier | Usage | État |
| --- | --- | --- |
| `00-learning-path.svg` | Introduction, cinq étapes en chevrons | Livré, autonome, largeur 1600 px |
| `00-architecture.png` | Introduction, architecture | Livré, 1600 x 860 px, export du draw.io |
| `00-architecture.svg` | README et vue agrandie | Livré, icônes intégrées sans ressource externe |
| `10-recap.svg` | Conclusion, cinq acquis | Livré, autonome, largeur 1600 px |
| `banner.jpg` | Bannière optionnelle | 1280 x 640 px ; ne pas ajouter banner_url avant livraison |

Ces trois schémas ne sont pas des captures de Fabric. L'architecture a deux formats d'export et une source éditable dans [../architecture.drawio](../architecture.drawio). Tous les labs et le bonus utilisent des indications de capture visibles ; seule la capture de répétition des notes animateur conserve une référence commentée tant que son fichier est absent.

## Capturer en déroulant les labs

Les emplacements sont intégrés dans les pages, au plus près de l'écran ou du contrôle concerné. Ils remplacent l'ancien catalogue fondé sur les numéros de clics : utilisez le libellé de l'indication, pas un ancien numéro d'étape.

| Lab | Indications de capture | Contenu |
| --- | ---: | --- |
| Lab 1 | 6 | Création, raccourcis, cible source et fichiers S3 |
| Lab 2 | 8 | Locale, connexion, aperçu, types, mois, destination, résultat et filtre SharePoint |
| Lab 3 | 6 | Jointures, colonnes développées, regroupement et vue |
| Lab 4 | 6 | Tables sélectionnées, réponses, instructions et validation de l'exemple |
| Lab 5 | 6 | État initial, condition, destination, franchissement, Teams et historique |
| Lab 6 | 6 | Exécution SQL, types des tables, résultats des trois requêtes et vue |
| Lab 7 | 6 | Tables du modèle, Direct Lake/SSO, relations, mesure et source de l'agent |
| Lab 8 | 8 | Source, destination, mappage, résultats KQL et règle Activator |
| Bonus Copilot | 4 | Source distincte, proposition de transformation, KQL et comparaison |
| **Total** | **56** | 32 dans le parcours principal et 24 dans les options ; variantes et contrôles compris |

Après avoir réalisé et anonymisé un écran, ajoutez son PNG ici, puis remplacez la ligne *[capture : …]* correspondante par une référence Markdown :

```markdown
![Lakehouse lh_lab, zones Tables et Fichiers](assets/lab01-lakehouse-explorer.png)
```

Gardez l'indentation de la ligne quand elle appartient à une étape numérotée. Le nom reste stable si une étape est déplacée : par exemple `lab01-shortcut-properties.png` ou `lab02-destination-mapping.png`. Une capture doit montrer le résultat réellement obtenu ; signalez un écart plutôt que fabriquer l'état attendu.

## Complément de répétition

| Fichier | Usage | Écran |
| --- | --- | --- |
| `lab05-rehearsal-notification.png` | Notes animateur uniquement | Notification de répétition datée, identifiée comme telle |

## Activer les captures livrées

Déposer chaque PNG réel dans ce dossier avec le nom attendu, puis exécuter depuis la racine :

```powershell
python tools/check_assets.py
python tools/check_assets.py --check --summary
```

La première commande traite les références Markdown déjà insérées : elle signale les fichiers présents/manquants, commente les captures absentes et décommente celles dont le fichier existe et n'est pas vide. Elle ne transforme pas les indications *[capture : …]* en liens et ne génère ni image ni bannière. Les trois schémas restent actifs par exception explicite. La seconde commande contrôle sans écrire ; son code vaut 1 seulement si une référence doit changer.

Avant commit : vérifier le cadre rouge, la lisibilité à 1600 px, les textes alternatifs, l'écran réellement testé et l'anonymisation. Aucun fichier image vide ne doit être ajouté pour contourner ce contrôle.