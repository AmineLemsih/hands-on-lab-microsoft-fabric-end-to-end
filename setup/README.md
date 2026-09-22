# Préparer et nettoyer les workspaces

Les scripts de workspaces sont réservés à l'animateur. Ils utilisent l'API REST Fabric publique `https://api.fabric.microsoft.com/v1`. **Ils ne créent pas de capacité, ne la démarrent pas et ne la suppriment pas.** La préparation des données est assurée séparément par le notebook ci-dessous ; le rapport reste à construire.

## Préparer lh_source avec le notebook

Cette procédure ne nécessite pas les scripts REST si vos workspaces existent déjà. Utiliser un compte autorisé à créer un notebook et écrire dans le lakehouse. Les participants de la session guidée n'exécutent pas cette préparation.

1. Ouvrir le workspace commun, normalement `ws-shared`.
2. Créer un lakehouse `lh_source` si absent, avec les schémas activés.
3. Télécharger [setup_lh_source.ipynb](https://raw.githubusercontent.com/AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/main/setup/setup_lh_source.ipynb).
4. Dans le workspace, choisir « Importer un notebook » / « Charger un notebook ». <!-- TODO vérifier -->
5. Sélectionner le fichier téléchargé.
6. Ouvrir le notebook importé.
7. Dans son explorateur, choisir « Ajouter un lakehouse » et sélectionner `lh_source`. <!-- TODO vérifier -->
8. Définir `lh_source` comme lakehouse par défaut ; redémarrer la session Spark si Fabric le demande.
9. Vérifier l'utilisation du langage PySpark et lire l'avertissement de la cellule 1.
10. Exécuter les cellules 2 à 4, ou « Exécuter tout » en laissant `apply_after = False` en cellule 6.
11. Vérifier les volumes affichés : 30 sites, une ligne de facteurs, 10 840 consommations historiques et 30 observations du dernier jour.
12. Actualiser l'explorateur de `lh_source` et attendre la visibilité des tables dans son point de terminaison SQL.

Le notebook télécharge les CSV publics anonymement avec un délai limité, vérifie le schéma et les volumes avant écriture, puis utilise des types explicites. Les tables de démonstration existantes sont **remplacées**, pas cumulées. Ne pas l'attacher à un lakehouse de production. Le contrôle de nom `lh_source` est un garde-fou, pas une autorisation de modifier un environnement quelconque.

La cellule 6 « bascule after » est volontairement désactivée. Pendant le lab d'alerte, passer `apply_after` à True et exécuter uniquement cette cellule après observation de `before`. Elle remplace `consumption_latest_day`, pas l'historique. Remettre False et actualiser `sm_energy_report` dans le service. Pour revenir à `before`, réexécuter les cellules 2 à 4. La création du rapport suit [report/README.md](../report/README.md).

Le notebook est livré sans sorties ni IDs de tenant. Sa syntaxe et ses données sont contrôlées localement ; téléchargement réseau, `notebookutils.runtime.context` et écriture Delta restent à répéter dans Fabric. [Contexte d'exécution NotebookUtils](https://learn.microsoft.com/fabric/data-engineering/notebookutils/notebookutils-runtime) ; [tables dans les schémas lakehouse](https://learn.microsoft.com/fabric/data-engineering/lakehouse-schemas).

La simulation est le comportement par défaut : elle ne demande pas de jeton, ne lit pas le tenant et n'écrit pas de journal. Elle valide les paramètres locaux et affiche un plan **conditionnel**, pas un inventaire de l'existant.

## Prérequis

- Python 3.11 ou ultérieur.
- Pour le mode réel : les bibliothèques `requests` et `azure-identity`.
- Une capacité Fabric payante active dans une région compatible avec les fonctionnalités choisies.
- Une identité autorisée à créer des workspaces ; administrateur des espaces à réutiliser ; contributeur ou administrateur de la capacité pour l'affectation.
- Un groupe de sécurité Entra **déjà créé**, contenant les participants. Le script lui donne le rôle Viewer sur l'espace commun ; il ne crée pas le groupe et n'en change pas les membres.
- L'autorisation de l'organisation pour les connexions interactives et les permissions déléguées ci-dessous.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install requests azure-identity
```

Les identifiants, chemins de connexion et listes réelles restent locaux. Le fichier d'exemple contient seulement des adresses du domaine réservé `example.invalid`.

## Authentification sans secret dans les fichiers

### Connexion interactive recommandée

Utiliser une inscription d'application publique Entra approuvée, application de bureau, URI de redirection `http://localhost`, flux public autorisé, sans secret client. Fournir son identifiant avec `--client-id` et celui du tenant avec `--tenant-id`. `InteractiveBrowserCredential` ouvre le navigateur ; les mots de passe et les demandes MFA restent dans la page de connexion.

Configurer les permissions **déléguées** de l'application, puis faire accorder le consentement requis par le tenant :

| Service | Permission | Utilisation |
| --- | --- | --- |
| Fabric | `Workspace.ReadWrite.All` | Lister, créer, affecter des rôles et supprimer les workspaces |
| Fabric | `Capacity.ReadWrite.All` | Affecter un espace existant à la capacité |
| Fabric | `Lakehouse.ReadWrite.All` ou `Item.ReadWrite.All` | Créer `lh_source` |
| Microsoft Graph | `User.ReadBasic.All` | Résoudre les UPN des autres utilisateurs en identifiants Entra |

Le script demande le scope `https://api.fabric.microsoft.com/.default`, et séparément `https://graph.microsoft.com/.default` si une résolution d'identité est nécessaire. `.default` ne donne pas de permission supplémentaire : il utilise celles déjà configurées et consenties. Les droits du compte restent nécessaires en plus des scopes.

### Jetons fournis par l'environnement

Une autre méthode consiste à injecter un jeton délégué Fabric dans `FABRIC_TOKEN` et, si nécessaire, un jeton Graph distinct dans `GRAPH_TOKEN`, avec un outil approuvé par votre organisation. Ne pas passer de jeton dans la ligne de commande, dans le CSV ou dans Git. Un jeton Fabric n'est pas un jeton Graph. Les jetons fournis ne sont pas renouvelés par le script.

Ne pas copier de secret dans une conversation d'assistance. Aucun jeton n'est demandé ou créé par la simulation.

## Liste des participants

Créer localement `setup/participants.csv` à partir de [participants.example.csv](participants.example.csv). Colonnes obligatoires : `email,first_name`. Le prénom est informatif ; il ne détermine jamais le nom du workspace.

Le champ `email` est supposé être l'**UPN du compte dans le tenant de l'atelier**. Si l'adresse mail diffère de l'UPN, ou pour un invité B2B, ajouter une colonne facultative `object_id` contenant l'identifiant **objet utilisateur dans ce tenant**, pas l'identifiant d'une application. Cette colonne évite l'appel Graph pour la ligne concernée. Ne pas deviner l'UPN d'un invité à partir de son adresse externe.

Le nom est `ws-lab-<partie locale de l'email>`. Exemple fictif : `camille.martin@example.invalid` donne `ws-lab-camille.martin`. La partie locale est passée en minuscules sans accents ; points, underscores et tirets sont conservés, les autres caractères sont remplacés par un tiret. La longueur retenue est limitée à 100 caractères. Deux adresses de domaines différents ayant la même partie locale, deux noms normalisés identiques ou deux identifiants Entra identiques arrêtent le script avant toute écriture. Utiliser des comptes à parties locales distinctes pour une session ; ne pas inventer une adresse pour contourner une collision. Les mêmes prénoms sont autorisés.

Conserver les adresses, le préfixe et l'identifiant de session d'une relance à l'autre. Les identifiants des autres items du lab utilisent `snake_case` anglais, sans espace ni tiret : `lh_source`, `lh_lab`, `wh_energy`, `consumption`. La [création d'un lakehouse](https://learn.microsoft.com/fabric/data-engineering/create-lakehouse) exige une lettre initiale, puis lettres/chiffres/underscores, et au plus 123 caractères. Nous appliquons ce sous-ensemble conservateur aux warehouses et tables également ; ce n'est pas une affirmation que tous les types d'items ont exactement les mêmes limites.

## Paramètres et exécution

Exemples PowerShell, depuis la racine. Les variables ci-dessous doivent être renseignées **localement** ; leurs valeurs ne doivent pas être ajoutées à la documentation publique.

```powershell
.venv\Scripts\python setup/create_workspaces.py --participants setup/participants.csv --capacity-id $env:FABRIC_CAPACITY_ID --participants-group-id $env:FABRIC_PARTICIPANTS_GROUP_ID
```

Après examen du plan, l'animateur peut lancer la création réelle :

```powershell
.venv\Scripts\python setup/create_workspaces.py --participants setup/participants.csv --capacity-id $env:FABRIC_CAPACITY_ID --participants-group-id $env:FABRIC_PARTICIPANTS_GROUP_ID --tenant-id $env:FABRIC_TENANT_ID --client-id $env:FABRIC_CLIENT_ID --apply
```

| Option | Défaut | Sens |
| --- | --- | --- |
| `--participants` | `setup/participants.csv` | Liste locale |
| `--capacity-id` | Obligatoire | UUID de la capacité, pas l'identifiant de ressource Azure |
| `--participants-group-id` | Obligatoire | UUID du groupe de sécurité Entra |
| `--role` | `Member` | `Admin`, `Member`, `Contributor` ou `Viewer` ; seul Member est le profil nominal du lab |
| `--prefix` | `ws-lab-` | Préfixe des espaces personnels |
| `--common-name` | `ws-shared` | Nom de l'espace commun |
| `--session` | `energy-lab` | Marqueur stable de la session, en minuscules/chiffres/tirets |
| `--journal` | `setup/workspaces.csv` | Journal CSV local à conserver jusqu'au nettoyage |
| `--clone-report` | Désactivé | Option réservée, non implémentée, voir ci-dessous |
| `--dry-run` | Implicite | Simulation hors ligne |
| `--apply` | Désactivé | Autorise les écritures distantes |

Pour plusieurs sessions simultanées, choisir des noms communs, préfixes, marqueurs et journaux distincts. Reporter les noms utiles dans les variables du lien de session MOAW.

## Idempotence et protections

Le script parcourt toutes les pages de résultats. Il crée les espaces manquants avec la capacité demandée et attend l'affectation si nécessaire. Il crée `lh_source` avec le schéma `dbo` si absent. Les opérations longues de création du lakehouse sont suivies via leur identifiant et leur résultat, avec un délai maximal.

Chaque workspace créé est journalisé **avant les étapes suivantes**, avec son UUID et un marqueur dans sa description. Une relance avec les mêmes paramètres réutilise les espaces et les rôles ; le journal est ajouté, jamais effacé. Un rôle direct différent n'est pas remplacé automatiquement. Un espace personnel sans le marqueur attendu n'est pas adopté. Un workspace commun préexistant est réutilisable s'il est sur la capacité demandée ; il n'est jamais déplacé ni considéré comme créé par cette session.

Le journal distingue `created`, `reused`, `pending`, `completed` et `deleted`. Il contient aussi les identifiants des lakehouses créés et des opérations en attente. Le verrou local empêche deux scripts d'utiliser **le même journal** en même temps. Ne pas lancer deux préparations concurrentes avec des journaux différents pour les mêmes noms.

Les réponses 429 utilisent `Retry-After`, dans une fenêtre bornée. Une erreur réseau ou HTTP inattendue arrête le script, sans rejeu aveugle des créations. En cas de perte de la réponse après une création côté serveur, vérifier Fabric et le journal : une ressource créée mais non journalisée ne sera volontairement **pas** supprimée automatiquement. Pour une opération longue échouée ou expirée, inspecter son état avant d'archiver le journal et de reprendre ; ne pas retirer une ligne `pending` sans vérification. Un verrou restant après un arrêt brutal ne doit être retiré qu'après confirmation qu'aucun autre processus ne travaille.

## Permissions complémentaires à préparer

La préparation API donne les **rôles de workspace**, pas toutes les permissions des éléments. Ne pas annoncer l'environnement prêt avant ces actions manuelles :

1. Ouvrir le partage de `lh_source` dans `ws-shared`.
2. Ajouter le groupe des participants.
3. Activer l'option donnant `ReadAll`, « Lire toutes les données Apache Spark » / « Lire toutes les données OneLake » selon l'interface. <!-- TODO vérifier -->
4. Confirmer le partage, qui accorde aussi `Read` sans droit d'écriture.
5. Tester les fichiers, les raccourcis et Direct Lake sur OneLake en SSO avec un compte participant, conformément au [guide de données](../data/README.md).
6. Publier `energy_report` et son modèle `sm_energy_report` dans `ws-shared` selon [le guide du rapport](../report/README.md).
7. Associer le modèle à une connexion cloud à **identité fixe**, avec SSO désactivé pour cette connexion.
8. Vérifier les droits de lecture de l'identité fixe sur la source et du groupe sur le rapport/modèle.
9. Tester à **J-7** « Définir une alerte » depuis le rapport commun avec le rôle Viewer, en enregistrant `act_energy` dans le workspace personnel Member. <!-- TODO vérifier -->

Le parcours nominal ne copie pas le rapport et n'exige pas Build pour le lire. L'identité fixe du modèle commun ne remplace **pas** ReadAll sur `lh_source` pour les raccourcis et le modèle personnel en SSO. Si la sécurité OneLake est activée, faire vérifier ses rôles par l'administrateur. [Partage du lakehouse](https://learn.microsoft.com/fabric/data-engineering/lakehouse-sharing) ; [sécurité Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-security-integration).

**Point de validation bloquant :** la documentation actuelle [Activator depuis Power BI](https://learn.microsoft.com/fabric/real-time-intelligence/data-activator/activator-get-data-power-bi) décrit aussi un parcours qui exige Edit sur le rapport. Ne pas promettre que Viewer suffit dans chaque tenant. Vérifier le chemin disponible et l'exigence F64 ou supérieure annoncée pour le parcours d'alertes Power BI retenu. <!-- TODO vérifier --> Plan B capacité : faire approuver une montée temporaire de la capacité PAYG en F64, puis refaire exactement le test Viewer. Une montée de capacité n'accorde pas Edit. Si le parcours reste indisponible, le Lab 5 doit être annoncé comme démonstration animateur avec capture, sans augmenter discrètement les droits sur `ws-shared`.

## Option de clonage hors parcours nominal

`--clone-report` est conservée, désactivée par défaut. En simulation, elle affiche le travail restant. Avec `--apply`, elle arrête le script **avant tout appel réseau**, car son contrat n'a pas été validé. Aucun succès de clonage fictif n'est annoncé.

TODO vérifier : l'[API Power BI de clonage](https://learn.microsoft.com/rest/api/power-bi/reports/clone-report-in-group), le scope et le jeton Power BI distincts du jeton Fabric, `targetWorkspaceId`, les droits sur le rapport et son modèle, ainsi que l'idempotence. <!-- TODO vérifier --> Ne pas inventer un endpoint Fabric de copie. Après validation produit, l'option pourra automatiser un repli explicitement choisi par l'animateur ; elle n'est pas utilisée en Lab 5.

## Suppression explicite

Examiner d'abord le journal :

```powershell
python setup/delete_workspaces.py --journal setup/workspaces.csv
```

Seuls les workspaces ayant une ligne `created` et pas encore `deleted` sont candidats. Par défaut, le workspace commun est protégé. Les éléments qu'un participant a ajoutés dans son workspace seront supprimés avec celui-ci.

```powershell
.venv\Scripts\python setup/delete_workspaces.py --journal setup/workspaces.csv --tenant-id $env:FABRIC_TENANT_ID --client-id $env:FABRIC_CLIENT_ID --apply --confirm DELETE
```

Pour supprimer aussi le workspace commun **créé par cette session**, après vérification qu'il n'est plus utilisé :

```powershell
.venv\Scripts\python setup/delete_workspaces.py --journal setup/workspaces.csv --include-common --tenant-id $env:FABRIC_TENANT_ID --client-id $env:FABRIC_CLIENT_ID --apply --confirm DELETE
```

Le script vérifie les noms et marqueurs de tous les candidats avant le premier DELETE. Un espace renommé ou réaffecté bloque la suppression. Un 404 est enregistré comme déjà absent. Les espaces réutilisés, le groupe Entra et la capacité ne sont jamais supprimés. Les rôles ajoutés à un espace préexistant et un `lh_source` créé dans un espace préexistant restent à examiner manuellement après la session.

## Tests locaux

```powershell
python -m unittest discover -s setup -p "test_*.py" -v
```

Ces tests utilisent des réponses simulées. Ils ne remplacent pas une répétition sur un tenant de test autorisé.

## Contrats API consultés

| Opération | Route relative | Documentation |
| --- | --- | --- |
| Lister les workspaces | `GET /workspaces` | [Liste et pagination](https://learn.microsoft.com/rest/api/fabric/core/workspaces/list-workspaces) |
| Lire un workspace | `GET /workspaces/{workspaceId}` | [Lecture](https://learn.microsoft.com/rest/api/fabric/core/workspaces/get-workspace) |
| Créer un workspace | `POST /workspaces` | [displayName, description, capacityId](https://learn.microsoft.com/rest/api/fabric/core/workspaces/create-workspace) |
| Affecter la capacité | `POST /workspaces/{workspaceId}/assignToCapacity` | [capacityId, réponse 202](https://learn.microsoft.com/rest/api/fabric/core/workspaces/assign-to-capacity) |
| Lister les rôles | `GET /workspaces/{workspaceId}/roleAssignments` | [Rôles](https://learn.microsoft.com/rest/api/fabric/core/workspaces/list-workspace-role-assignments) |
| Ajouter un rôle | `POST /workspaces/{workspaceId}/roleAssignments` | [principal.id, principal.type, role](https://learn.microsoft.com/rest/api/fabric/core/workspaces/add-workspace-role-assignment) |
| Lister/créer un lakehouse | `GET` / `POST /workspaces/{workspaceId}/lakehouses` | [Création et enableSchemas](https://learn.microsoft.com/rest/api/fabric/lakehouse/items/create-lakehouse) |
| Suivre une création | `GET /operations/{operationId}` puis `/result` | [Opérations longues](https://learn.microsoft.com/rest/api/fabric/articles/long-running-operation) |
| Supprimer un workspace | `DELETE /workspaces/{workspaceId}` | [Suppression, réponse 200](https://learn.microsoft.com/rest/api/fabric/core/workspaces/delete-workspace) |
| Résoudre un UPN | `GET https://graph.microsoft.com/v1.0/users/{UPN}` | [Microsoft Graph](https://learn.microsoft.com/graph/api/user-get) |

Contrats consultés le 21 septembre 2026. Aucun endpoint ou payload conjectural n'est utilisé. Les permissions effectives et le comportement de bout en bout doivent encore être validés dans un tenant de test. <!-- TODO vérifier -->