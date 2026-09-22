# Notes animateur

**Product Hands-on Lab - Microsoft Fabric de bout en bout**  
Auteur unique : **Amine Lemsih**, conception et rédaction. Kit réutilisable par un CSA ou un animateur autorisé, sans contenu client dans le dépôt.

Le [workshop](workshop.md) contient les manipulations. Ce guide couvre la préparation et les vérifications que les participants ne doivent pas avoir à découvrir pendant la session. Le participant reçoit un lien de session et se connecte, rien d'autre.

## Contrat de livraison

Le texte est français, tous les identifiants techniques sont anglais. Noms génériques : `ws-shared`, `ws-lab-<email_local_part>`, `lh_source`, `lh_lab`, `energy_agent`, `energy_report`. Les valeurs de session sont transmises par les variables MOAW, pas inscrites dans le document public.

La table `consumption` (consommation) contient les observations annuelles nettoyées. `emission_factors` (facteurs d'émission) contient une ligne par année et deux colonnes de coefficients. `consumption_latest_day` (consommation du dernier jour disponible) contient uniquement le dernier jour simulé. Cette granularité doit rester identique dans le rapport, SQL, DAX et les instructions de l'agent.

**Statut initial : `published: false`.** Génération locale, tests sur API simulées et rendu MOAW ne prouvent pas le fonctionnement dans Fabric. Le passage à `true` attend la répétition tenant, la résolution des points bloquants et les captures.

## Lien de session

**Le participant reçoit un lien et se connecte, rien d'autre.** Les comptes et les droits sont préparés avant la séance. Le lien personnalise le texte ; il ne crée pas de workspace et n'accorde aucune permission.

| Variable | Défaut | Valeur à prévoir pour la session |
| --- | --- | --- |
| `shared_ws` | `ws-shared` | Workspace contenant `lh_source` et le rapport |
| `lab_ws` | `ws-lab-<votre identifiant>` | Nom du workspace personnel, ou convention de nommage clairement communiquée |
| `teams_channel` | le canal Teams de l'atelier | Nom du canal ou lien autorisé |
| `contact` | votre animateur | Nom ou moyen de contact de l'animateur |
| `report_link` | le rapport energy_report dans l'espace commun | Lien du rapport publié |
| `sp_site` | l'URL de votre site SharePoint | URL du site, uniquement pour la variante de données propres |

Sur une URL de lecture sans paramètres, la syntaxe est `?vars=shared_ws:ws-shared,teams_channel:Atelier%20Contoso`. Sur le lien court qui contient déjà `?src=...`, ajouter **`&vars=`**, jamais un second `?` :

<https://aka.ms/ws?src=gh:AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/main/docs/&vars=shared_ws:ws-shared,lab_ws:ws-lab-demo,teams_channel:Atelier%20Contoso,contact:Amine%20Lemsih>

Les valeurs de cet exemple sont fictives. Encoder les valeurs d'URL avec `encodeURIComponent`, notamment les espaces, `&`, `#` et les URL de rapport. Le format MOAW sépare les paires par des virgules : éviter les virgules dans les valeurs et vérifier le rendu avant diffusion. Aucun mot de passe, jeton ou secret dans `vars` : ces paramètres restent visibles dans l'historique du navigateur. Distribuer les liens réels en privé, jamais les commiter. Un lien individuel peut renseigner `lab_ws` sans document séparé.

L'exemple Q1 est disponible dans [assets/q1-example.sql](assets/q1-example.sql). Le valider sur le tenant de répétition avant diffusion. Pour S3, annoncer la disponibilité et désigner le raccourci dans le canal de session ; aucune clé d'accès n'est transmise au participant.

## Checklist J-7

- [ ] Confirmer 15 à 20 inscrits, les comptes dans le tenant et le parcours retenu. Prévoir un animateur et, si possible, un second intervenant pour l'assistance distancielle.
- [ ] Préparer le groupe de sécurité Entra contenant les participants ; contrôler les invités et leurs identifiants dans le tenant d'accueil.
- [ ] Confirmer les licences : droits de création Fabric, licence Power BI adaptée pour les exercices d'auteur, Pro ou compatible pour lire le rapport sous F64. Prévoir Pro pour les analystes qui créent les modèles du Lab 7.
- [ ] Vérifier la capacité **payante**, la région, les fonctionnalités disponibles et le budget de la session. La capacité minimale d'une fonction ne constitue pas un dimensionnement pour 20 personnes.
- [ ] Faire un test de concurrence représentatif : quelques Dataflows simultanés, endpoint SQL, agent, modèle et flux temps réel. Échelonner les exécutions si nécessaire.
- [ ] Exécuter la simulation de [préparation](../setup/README.md), vérifier les noms, puis autoriser séparément les écritures réelles. Conserver le journal local.
- [ ] Vérifier Membre sur chaque workspace personnel et Viewer sur le workspace commun.
- [ ] Partager **explicitement `lh_source` avec le groupe**, option `ReadAll`, « Lire toutes les données Apache Spark » / « Lire toutes les données OneLake » selon l'interface. <!-- TODO vérifier --> Ce partage ajoute Read mais n'accorde pas Write. Tester le raccourci avec un compte participant, pas l'administrateur.
- [ ] Vérifier les politiques de sécurité OneLake et, si elles sont actives, le rôle de lecture de la source. Tester Direct Lake en SSO depuis le modèle personnel et ses raccourcis.
- [ ] Si la variante S3 est retenue, créer dans « Fichiers » de `lh_source` un raccourci vers un bucket de démonstration autorisé, avec une clé d'accès limitée à la lecture des fichiers et à leur parcours. Stocker la clé dans une connexion Fabric, jamais dans le lien ni le dépôt ; prévoir sa rotation/révocation après l'atelier.
- [ ] Tester à J-7 la **double indirection** : raccourci OneLake de `lh_lab` vers le raccourci S3 de `lh_source`, avec le compte participant et ses droits de connexion/cible. <!-- TODO vérifier --> Annoncer la variante uniquement après lecture réussie des fichiers via ce chemin ; sinon la sauter, sans exposer la clé aux participants.
- [ ] Contrôler les paramètres tenant Copilot / Azure OpenAI intégré et data agents, leurs groupes autorisés et leur disponibilité régionale. Les libellés et règles de traitement/stockage interrégional doivent être vérifiés dans la documentation courante et avec l'organisation. <!-- TODO vérifier --> Ne pas activer une option cross-geo sans approbation.
- [ ] Créer un data agent de test sur les tables du lab. Vérifier les six questions, les instructions françaises, l'exemple validé et l'affichage des requêtes. Aucun secret Azure OpenAI n'est nécessaire pour le chat intégré.
- [ ] Exécuter l'exemple téléchargeable Q1 sur le tenant et valider **2 896 164,51 kWh électriques observés en 2025**. Vérifier sa compatibilité avec la source `lh_lab` sélectionnée par le participant.
- [ ] Répéter les variantes CSV et annoncer la source retenue dans le canal de session. Vérifier locale décimale, suppression des erreurs et nombre final de lignes.
- [ ] Répéter les opérations visuelles du Lab 3 jusqu'à l'enregistrement de la vue. La simple lecture du SQL de référence ne valide pas le parcours sans code.
- [ ] Construire `energy_report` et `sm_energy_report`, puis associer la source à `conn_energy_report`, connexion à identité fixe, SSO désactivé. Tester l'actualisation et la lecture du rapport avec le compte Viewer.
- [ ] Effectuer le **test bloquant « Définir une alerte » depuis `energy_report` sur la capacité cible**, avec compte Viewer dans `ws-shared` et Membre dans son espace personnel. Enregistrer `act_energy` dans l'espace personnel, sans copier le rapport. <!-- TODO vérifier -->
- [ ] Vérifier l'exigence **F64 ou plus** indiquée pour le parcours d'alertes Power BI retenu, ainsi que le paramètre tenant autorisant le bouton. <!-- TODO vérifier --> Prévoir une montée temporaire PAYG en F64, approuvée et chiffrée, puis refaire le test avec exactement les mêmes permissions.
- [ ] Mesurer la latence réelle du franchissement avant/après jusqu'à Teams. Préparer une capture de la notification et de l'historique comme plan B.
- [ ] Pour le parcours complet, exécuter séparément les trois créations de tables Warehouse par sélection inter-bases depuis `lh_lab.dbo`, vérifier les types produits et la précision des facteurs, puis répéter DAX Direct Lake, Bicycles/KQL et Activator. <!-- TODO vérifier -->
- [ ] Pour le bonus seulement, tester Copilot dans Dataflow Gen2 et dans le jeu de requêtes KQL. Son indisponibilité ne bloque pas les deux parcours principaux.

### Le point d'attention Viewer et F64

Le parcours demandé part du **rapport commun en lecture**, avec une alerte dans le workspace personnel. Le modèle utilise une identité fixe ; cela porte l'accès aux données, pas les droits d'édition du rapport.

La page [Activator depuis Power BI](https://learn.microsoft.com/fabric/real-time-intelligence/data-activator/activator-get-data-power-bi), consultée pendant la rédaction, décrit une expérience exigeant **Edit** sur le rapport. La condition F64 et l'accès depuis la lecture doivent donc être reconfirmés pour le parcours réellement disponible dans le tenant. <!-- TODO vérifier --> Ne pas présenter Viewer + F64 comme un fonctionnement testé alors que seule la documentation a été lue.

Plan B capacité : l'administrateur fait approuver le coût, monte la capacité PAYG de formation en F64 pour la session, puis la ramène à son niveau prévu ou la met en pause après nettoyage. **Ne pas redimensionner ni arrêter une capacité mutualisée sans autorisation.** Une montée de capacité ne corrige pas une permission Edit manquante.

Si le chemin lecteur n'est toujours pas disponible, annoncer avant la session que le Lab 5 sera une démonstration animateur et une analyse de capture. Ne pas ouvrir le workspace commun en écriture ni glisser une copie personnelle dans le parcours sans l'annoncer. `--clone-report` est seulement une option de préparation réservée, désactivée et non implémentée avant validation de l'API.

La documentation des anciennes alertes sur tuiles de dashboard ne valide pas ce scénario : le lab cible Activator sur le **visuel d'un rapport**, pas une tuile KPI.

## Checklist J-1

- [ ] Préparer le lien de session : noms des workspaces, rapport, Teams et contact. Le pipeline est exécuté manuellement ; la planification est facultative dans « Comprendre ».
- [ ] Générer les données et conserver le corrigé calculé. Vérifier 30 sites, une ligne de facteurs, 10 950 lignes brutes et 10 840 propres.
- [ ] Importer [setup_lh_source.ipynb](../setup/setup_lh_source.ipynb) dans l'espace commun et l'attacher à `lh_source`, schémas activés. Exécuter les cellules 2 à 4 : les quatre tables du rapport sont préparées, sans dépôt manuel de CSV.
- [ ] Vérifier `consumption` nettoyée (10 840 lignes), `sites` (30), `emission_factors` (1) et `consumption_latest_day` (30), puis leur visibilité SQL.
- [ ] Actualiser le modèle sur l'état `before`. Vérifier que les six régions sont sous le seuil de 10 000 kWh et que `apply_after` reste False dans le notebook.
- [ ] Vérifier le rapport partagé, son lien, son modèle à identité fixe et sa dernière actualisation réussie.
- [ ] Préparer un raccourci de démonstration et un workspace animateur, distincts des espaces participants.
- [ ] Contrôler les tables du data agent de démonstration et les exemples. Conserver le corrigé accessible sans devoir exécuter un notebook en session.
- [ ] Préparer les captures listées dans [assets/SCREENSHOTS-TODO.md](assets/SCREENSHOTS-TODO.md), notamment le plan B de notification.
- [ ] Confirmer le résultat du test Viewer/F64 et annoncer le mode individuel ou démonstration pour le Lab 5.
- [ ] Vérifier les URL raw des états `before` et `after` versionnés. La bascule du notebook ne doit modifier que la table du dernier jour.
- [ ] Vérifier le rendu MOAW sur ordinateur et mobile. Garder les captures tenant privées tant qu'elles ne sont pas anonymisées.

## Checklist jour J

- [ ] Allumer ou reprendre **la capacité de formation autorisée** avant l'arrivée des participants. Vérifier son état, la capacité choisie pour le rapport et la disponibilité des items.
- [ ] Ouvrir Fabric avec le compte de test et confirmer connexion, accès et licence.
- [ ] Afficher le parcours retenu et les horaires de pause. Rappeler que Copilot est un bonus hors minutage.
- [ ] Présenter le nommage anglais et les données fictives ; rappeler que les erreurs sont volontairement présentes.
- [ ] Noter les difficultés dans un support privé, sans jeton ni données client dans le canal public.
- [ ] Utiliser la réserve d'aide pour les connexions, la synchronisation SQL et les vérifications des résultats. Ne pas supprimer une étape de contrôle pour tenir le temps.
- [ ] En Lab 5, attendre que les règles soient actives et aient observé l'état sous le seuil avant de charger `after`.
- [ ] En fin de Lab 8, arrêter les règles de démonstration répétitives et le flux dès qu'ils ne sont plus utilisés, en coordination avec les participants.

## Minutage des deux parcours

Les horaires sont relatifs au début. La réserve en fin de tableau peut être répartie plus tôt ; elle n'ajoute pas de nouvelles activités.

### Tableau détaillé déplacé de l'introduction

La lecture de l'introduction vise cinq minutes ; le créneau d'accueil de dix minutes inclut les échanges et le démarrage. Les contrôles et contextes optionnels restent dans le budget de chaque module.

| Section | Activité | Métiers | Complet |
| --- | --- | ---: | ---: |
| 0 | Introduction | 10 min | 10 min |
| 1 | Prise en main | 20 min | 20 + 5 min |
| 2 | Ingestion | 35 min | 35 + 5 min |
| Pause | Après le Lab 2 | 15 min | 15 min |
| 3 | Exploration | 25 min | 25 + 5 min |
| 4 | Data agent | 30 min | 30 + 5 min |
| 5 | Alerte | 15 min | 15 + 5 min |
| 6 | Extension : Entrepôt et T-SQL | Sauter | 20 min |
| 7 | Extension : Modèle sémantique Direct Lake | Sauter | 25 min |
| Pause | Après le Lab 7 | Sans objet | 10 min |
| 8 | Extension : Temps réel | Sauter | 35 min |
| 9 | Bonus Copilot | Hors minutage | Hors minutage |
| 10 | Conclusion | 10 min | 10 min |
| Réserve | Aide, transitions et questions | 20 min | 25 min |
| **Total** | **Pauses comprises, sans le bonus** | **180 min** | **300 min** |

### Parcours métiers 3 h

| Horaire | Activité | Minutes |
| --- | --- | ---: |
| 00:00 - 00:10 | Introduction | 10 |
| 00:10 - 00:30 | Lab 1 · Prise en main | 20 |
| 00:30 - 01:05 | Lab 2 · Ingestion | 35 |
| 01:05 - 01:20 | Pause | 15 |
| 01:20 - 01:45 | Lab 3 · Exploration | 25 |
| 01:45 - 02:15 | Lab 4 · Data agent | 30 |
| 02:15 - 02:30 | Lab 5 · Alerte | 15 |
| 02:30 - 02:50 | Aide, transitions et questions, réaffectables | 20 |
| 02:50 - 03:00 | Conclusion | 10 |
| **Total** | 145 activités + 15 pause + 20 réserve | **180** |

Les cinq blocs « Comprendre », les extensions et Copilot ne sont pas lus dans ce parcours. Copier l'exemple Q1 téléchargeable ne demande pas d'écrire du SQL.

### Parcours complet 5 h

| Horaire | Activité | Minutes |
| --- | --- | ---: |
| 00:00 - 00:10 | Introduction | 10 |
| 00:10 - 00:35 | Lab 1 · Prise en main + Comprendre | 25 |
| 00:35 - 01:15 | Lab 2 · Ingestion + Comprendre | 40 |
| 01:15 - 01:30 | Première pause | 15 |
| 01:30 - 02:00 | Lab 3 · Exploration + Comprendre | 30 |
| 02:00 - 02:35 | Lab 4 · Data agent + Comprendre | 35 |
| 02:35 - 02:55 | Lab 5 · Alerte + Comprendre | 20 |
| 02:55 - 03:15 | Lab 6 · Entrepôt et T-SQL | 20 |
| 03:15 - 03:40 | Lab 7 · Direct Lake | 25 |
| 03:40 - 03:50 | Deuxième pause | 10 |
| 03:50 - 04:25 | Lab 8 · Temps réel | 35 |
| 04:25 - 04:50 | Aide, transitions et questions, réaffectables | 25 |
| 04:50 - 05:00 | Conclusion | 10 |
| **Total** | 145 tronc + 80 extensions + 25 explications + 25 pauses + 25 réserve | **300** |

Le bonus Copilot demande environ 15 minutes **supplémentaires**. Ne pas l'ajouter tacitement à 5 h, ni retirer la seconde pause pour la caser. Si le groupe finit réellement en avance, l'animateur peut l'utiliser sans dépasser l'horaire annoncé.

La variante S3 du Lab 1 demande **10 minutes supplémentaires**, hors des deux minutages. Elle ne remplace pas les raccourcis des tables de référence ; annoncer sa disponibilité et son emplacement dans le canal de session.

## Déclenchement contrôlé au Lab 5

Le seuil de **10 000 kWh** est évalué **par région**. La question Q4 de l'agent conserve **20 000 kWh par couple site/jour**. Les deux seuils ont des valeurs et des granularités différentes.

### Avant les règles

1. Ouvrir le notebook de préparation attaché à `lh_source`.
2. Vérifier `apply_after = False` dans la cellule 6.
3. Exécuter les cellules 2 à 4 pour initialiser `before`.
4. Attendre leur réussite.
5. Contrôler les 30 lignes de `consumption_latest_day`.
6. Actualiser `sm_energy_report`.
7. Attendre la réussite de l'actualisation.
8. Vérifier le visuel « consommation du dernier jour disponible par région ».
9. Faire créer et démarrer les règles des participants.
10. Attendre que l'observation de départ soit visible dans les règles, selon la latence mesurée à J-7.

Le notebook télécharge le CSV `before` depuis le dépôt public et remplace la table Delta ; aucun fichier n'est à déposer manuellement dans le lakehouse.

### Pendant la démonstration en direct

1. Ouvrir la cellule 6 « bascule after » du notebook.
2. Passer `apply_after` à True.
3. Exécuter cette cellule uniquement.
4. Attendre sa réussite et remettre `apply_after` à False.
5. Vérifier que la table conserve 30 lignes.
6. Actualiser `sm_energy_report`.
7. Noter l'heure de fin d'actualisation.
8. Vérifier que la Bretagne passe de **2 724,55 à 36 724,55 kWh**.
9. Observer l'historique des actions Activator.
10. Noter l'heure de réception Teams et la latence constatée.

Le CSV annuel, les sites et les facteurs ne changent pas. La table des facteurs garde la mention « fictif, ne pas utiliser pour un reporting réel ». Les autres régions restent sous le seuil. Le visuel ne doit pas avoir d'axe temporel : Activator peut ignorer la correction d'un point temporel déjà examiné.

### Si la notification arrive trop tard

Montrer les observations, la condition et les étapes déjà réussies, puis la capture de répétition. Dire explicitement qu'elle a été reçue avant la session. Ne pas afficher « test réussi aujourd'hui » sans notification/action correspondante. Ne pas déclencher une série de changements de seuil ou de rafraîchissements incontrôlés.

<!-- ![Plan B : notification reçue lors d'une répétition identifiée, destinataire anonymisé](assets/lab05-13-rehearsal-notification.png) -->

## Pièges connus et reprise

### Consignes déplacées du workshop

Les passages ci-dessous ont été retirés du texte participant lors de la relecture. Les extraits gardent leur origine pour faciliter la revue ; les procédures actives et les checklists de ce guide font foi.

| Section source | Phrases déplacées et consigne conservée ici |
| --- | --- |
| 0, modalités | « Les temps d'aide sont répartis par l'animateur. » |
| 0, architecture et accès | L'animateur prépare les données et fournit le lien de session. |
| 0, Préparation obligatoire de l'alerte | « L'animateur teste à J-7 le bouton Définir une alerte depuis le rapport commun avec un compte Viewer, sur la capacité cible, en choisissant un workspace personnel comme destination. » Les prérequis de capacité et d'édition diffèrent selon l'expérience disponible ; le test autorise le déroulement individuel, sans copie nominale du rapport. |
| 0, auteur | « Les animateurs réutilisent le kit sans ajouter de contexte client au document public. » |
| 0, prérequis et conventions | Vérifier la capacité payante active, les licences de lecture/création et le partage Read + ReadAll de `lh_source`, ainsi que la lecture de `energy_report` et de son modèle à identité fixe. L'accès à la source des raccourcis reste nécessaire au modèle personnel en SSO. Rappeler de ne publier aucun jeton, mot de passe, URL privée ou message d'erreur sensible dans le dépôt. Les prérequis participant ne remplacent pas la checklist d'accès J-7. |
| 1, dépannage | « L'animateur contrôle le rôle Viewer. » ; « L'animateur adapte le chemin si le lakehouse source est sans schémas. » Vérifier aussi ReadAll et sa propagation si l'item est visible mais sa donnée refusée. |
| 2, contrôle et pause | Accompagner le contrôle des lignes écrites si les détails d'exécution sont difficiles à lire ; « L'animateur annonce l'heure de reprise. » |
| 2, planification | Les anciennes étapes 15 à 21 d'« Orchestrer et planifier » deviennent trois lignes facultatives dans « Comprendre » : fréquence quotidienne, heure/fuseau/date de fin, enregistrement. Aucun planning n'est exigé au point de contrôle. Tester la locale du dataflow avant import ; la détection peut laisser `kwh_elec` en Texte à cause de `invalid`, d'où la correction conditionnelle conservée. |
| 3, vue et contrôle | « Toutes les transformations doivent pouvoir être traduites en SQL par l'éditeur ; l'animateur vérifie ce parcours visuel avant la session. » ; « L'animateur dispose du corrigé calculé pour comparer les résultats. » Ne pas substituer du SQL au parcours visuel sans l'annoncer. |
| 4, exemple et dépannage | « Si Q1 n'est pas correcte, l'animateur la vérifie avec vous avant l'ajout. » ; « L'animateur vérifie la capacité payante, la région et les paramètres tenant des data agents et de l'IA. » ; « Testez les instructions en français avant diffusion. » La capacité d'essai ne suffit pas au parcours prévu. |
| 4, préparation de Q1 après relecture | L'exemple Q1 téléchargeable est validé à J-7. Le participant conserve uniquement le collage et la validation de l'exemple dans l'interface. |
| 5, bouton indisponible | « Ce chemin doit avoir été validé à J-7 avec les mêmes droits et la même capacité. » ; « La documentation décrit également une expérience demandant Edit sur le rapport. » ; « L'animateur applique le plan B annoncé. » Ne pas accorder l'écriture sur l'espace commun ni imposer une copie sans annonce. |
| 5, changement des données | L'animateur exécute la cellule de bascule du notebook, puis actualise `sm_energy_report` avec son identité fixe. Vérifier la table du dernier jour si le rapport ne change pas. |
| 5, contrôle et dépannage | « La notification peut arriver après la fin du module : sa latence est mesurée à J-7. » ; « Si le plan B capture est utilisé, distinguez clairement la règle créée aujourd'hui de la notification reçue en répétition. » Contrôler les droits et le paramètre tenant ; F64 ne donne pas Edit. Les filtres sont capturés à la création de la règle. |
| 6, chargement et dépannage | Le chargement automatique et les modes de copie doivent être répétés sur la version du connecteur utilisée ; préparer les destinations si nécessaire. « L'animateur remet la table de démonstration à zéro avant un nouvel essai. » Ne pas improviser des chargements en ajout après un échec. |
| 7, connexion et dépannage | Accompagner la vérification de SSO, des accès de l'utilisateur et du propriétaire à la cible du raccourci. Membre de l'espace personnel ne remplace pas la lecture de `lh_source`. |
| 8, schéma | « Le schéma des exemples intégrés peut évoluer. L'animateur le confirme à J-7. » Adapter le mappage si nécessaire. Référence déplacée : [requêtes du tutoriel temps réel](https://learn.microsoft.com/fabric/real-time-intelligence/tutorial-5-query-data), qui illustre les champs. |
| 8, règle et dépannage | « Si aucun événement ne satisfait la condition, l'animateur choisit avec vous un seuil de démonstration cohérent avec l'aperçu. » ; « Si l'échantillon rejoue des dates anciennes, l'animateur adapte la fenêtre à la plage affichée. » ; « L'animateur arrête les règles et le flux après l'exercice pour éviter le bruit et les coûts. » |
| 9, préparation et contrôle | « L'animateur vérifie sa disponibilité et les règles de traitement des données avant la session. » ; « Une fonction indisponible dans le tenant n'est pas un exercice échoué. » Vérifier région, capacité et paramètres avant d'annoncer le bonus. |
| 10, adaptation | « L'animateur adapte ce paragraphe oralement ou dans les supports privés de la session. Aucun nom de client, lien de tenant ou objectif confidentiel ne doit être ajouté au workshop public. » |
| 10, fermeture | « L'animateur arrête les planifications, les alertes et les flux, puis supprime les workspaces de la session à partir de son journal. Il gère la capacité selon l'accord de l'organisation. Un espace commun préexistant n'est pas supprimé automatiquement. » ; « Seul l'animateur applique le nettoyage prévu. » |
| 10, contrôle et ressources | « Les captures du brouillon et les tests tenant restent des prérequis de diffusion, pas des preuves de fonctionnement déjà réalisées. » Les exercices ont été réécrits pour Contoso, sans copie de la prose des sources. |

### Diagnostics

| Situation | Diagnostic et action |
| --- | --- |
| Table invisible en SQL | Vérifier Delta et raccourci dans le lakehouse, attendre la synchronisation, actualiser l'explorateur. Ne pas recréer immédiatement la table. |
| Viewer voit l'item mais pas les fichiers | Vérifier le partage Read + ReadAll, sa propagation et la sécurité OneLake. Un rôle workspace n'est pas tout le modèle d'accès. |
| Data agent absent | Capacité payante requise, paramètres tenant, région et autorisations de groupe ; la capacité d'essai n'est pas le parcours prévu. |
| Rapport refusé sous F64 | Contrôler la licence Power BI Pro ou compatible et les droits du rapport/modèle. Ne pas activer un essai à l'aveugle. |
| Rapport visible mais bouton alerte absent | Test Viewer/capacité/tenant à J-7 ; certaines expériences documentées demandent Edit. F64 ne donne pas Edit. |
| Alerte sans nouvel événement | Recharger la table puis actualiser le modèle. Rafraîchir la page ne suffit pas. Vérifier observation sous le seuil et règle active avant `after`. |
| Mauvais total électrique | Conversion des points décimaux, erreurs supprimées, mode Remplacer, pas d'imputation. |
| Carbone doublé | Facteurs non uniques par année, relation incorrecte ou résultats de deux sources ajoutés par l'agent. |
| Exemple d'agent ignoré | Validation SQL non terminée ou exemple incompatible avec les tables sélectionnées. Les modèles sémantiques n'utilisent pas ces paires SQL/KQL. |
| Table Warehouse déjà existante | Une création de table par sélection ne se rejoue pas comme une actualisation. Vérifier le contenu de la table existante ; préparer un environnement neuf avant le lab plutôt que demander une suppression aveugle. |
| Direct Lake en erreur | Vérifier les relations et les accès de l'utilisateur/propriétaire à la cible des raccourcis. Ne pas remplacer discrètement SSO par une identité fixe dans l'exercice personnel. |
| KQL vide | Contrôler noms et types mappés, casse, plage des dates de l'échantillon et arrivée de nouvelles données. |

Prévoir les résultats de référence pour poursuivre une explication si un participant est bloqué. Une démonstration animateur ne compte pas comme une manipulation individuelle terminée.

## Checklist après la session

- [ ] Confirmer que chacun a enregistré ce qu'il doit conserver ; ne pas supprimer sans l'accord prévu pour la session.
- [ ] Arrêter les éventuelles planifications facultatives, les règles Activator et les Eventstreams créés pour le lab.
- [ ] Révoquer ou examiner les connexions et partages créés pour la session selon la politique de l'organisation.
- [ ] Exécuter la simulation de suppression sur le journal, puis autoriser la suppression explicite des workspaces personnels. Ajouter l'espace commun uniquement s'il a été créé pour cette session et n'est plus utilisé.
- [ ] Examiner manuellement un espace commun préexistant : le script ne le supprime pas et ne retire pas automatiquement les partages ajoutés.
- [ ] Remettre la capacité PAYG de formation au niveau prévu ou la mettre en pause avec l'autorisation de son propriétaire. Faire le nettoyage avant la pause pour garder les API disponibles ; une reprise temporaire peut être nécessaire sinon.
- [ ] Publier l'enregistrement dans l'emplacement autorisé et le partager dans le canal privé, avec consentement et contrôle des captures. Aucun lien client dans le workshop public.
- [ ] Archiver le journal privé selon les règles de rétention, puis retirer les jetons de l'environnement local. Ne jamais les consigner dans le compte rendu.
- [ ] Reporter les corrections génériques dans le dépôt sans données ni identifiants de client.

## Adapter à un client en 30 minutes

| Budget | Action |
| --- | --- |
| 0 - 10 min | Préparer le lien de session : workspaces, rapport, Teams, contact. Vérifier connexion, accès et licence. |
| 10 - 20 min | Garder les données synthétiques par défaut. Facultativement préparer un extrait client non sensible **au même schéma**, autorisé et stocké uniquement dans l'environnement privé. |
| 20 - 30 min | Adapter oralement ou dans les supports privés « Et chez vous ? », le vocabulaire métier, la décision et le prochain responsable. |

Changer les données exige de **recalculer** les résultats attendus, les dates, le seuil et les deux états. Le corrigé du générateur ne valide que les données synthétiques qu'il a produites. Si cette nouvelle recette n'est pas faisable en 30 minutes, garder le jeu Contoso ; ne pas promettre que tout extrait client est immédiatement compatible.

Ne pas changer les noms techniques pour une traduction. Les éléments contextualisés appartiennent au lien de session et aux supports privés. Aucun facteur réel ne doit être proposé sans provenance et périmètre approuvés.

## Livrer en journée d'upskilling

Utiliser les supports de présentation existants le matin pour les concepts, la gouvernance, la sécurité et les cas d'usage. Réserver réellement cinq heures l'après-midi, par exemple 13 h - 18 h, pauses comprises. Un créneau de trois heures n'est pas un parcours complet compressé.

Préparer en plus : postes analystes pour copier les requêtes, licences de création Power BI, répétition Direct Lake/DAX, lecture inter-bases Warehouse et types des tables créées, échantillon RTI et quotas de capacité, arrêt des flux, appui d'un second animateur si besoin. Précharger seulement les sources communes ; les participants construisent leurs propres éléments. Les corrigés et captures de reprise restent disponibles. Aucun deck ni simulateur de compteurs n'est créé dans la v1 du kit.

## Registre des vérifications produit

Les commentaires `<!-- TODO vérifier -->` restent près de l'instruction concernée. Cette table regroupe leur objet ; retirer un commentaire applicable seulement après observation sur la version de l'interface et le rôle de la session. Les commentaires devenus orphelins après suppression d'une instruction sont retirés sans considérer la fonctionnalité comme validée.

| Section ou support | Vérifications regroupées |
| --- | --- |
| Préparation de l'introduction, hors texte participant | Libellé ReadAll ; droits/chemin d'alerte lecteur ; licences et capacité de la session |
| 1 | Case schémas, menu `dbo`, propriétés du raccourci et accès cible ; variante S3 facultative : double indirection OneLake vers raccourci S3 et permissions de lecture/connexion |
| Lab 2 | Nommage/publication du flux ; locale avant import ; Web/Texte-CSV anonyme sur l'URL raw ; variante Content SharePoint ; types détectés ; Début du mois ; destination Remplacer ; lignes écrites ; planification facultative |
| 3 | Accès endpoint SQL ; deux jointures externes gauches ; regroupement région/mois et sommes séparées ; chargement actif et sauvegarde de vue. Le carbone reste dans la variante SQL, l'agent et DAX. |
| 4 | Libellé agent ; détails de réponse ; instructions françaises ; éditeur et validation d'exemples ; remise à zéro du chat |
| 5 | Bouton alerte en lecture ; F64/tenant ; condition Devient ; workspace destination ; validation et activation ; ouverture/historique Activator ; latence réelle |
| 6 | Libellé Warehouse ; nom en trois parties `lh_lab.dbo` depuis le même workspace ; lecture des raccourcis ; types produits par CREATE TABLE AS SELECT et précision des facteurs |
| 7 | Création/édition explicite du modèle ; mode Direct Lake/SSO ; gestion des relations ; permissions des sources de l'agent |
| 8 | Source intégrée/casse/champs ; ingestion directe/configuration/mappage ; jeu KQL ; destination Activator ; objet/propriété/condition ; test d'action distinct du test de franchissement |
| 9 | Disponibilité des deux surfaces Copilot, paramètres tenant/région et chemins français |
| Données | Téléchargement anonyme des CSV ; notebook attaché au bon lakehouse ; types et volumes Delta ; ReadAll |
| Rapport | Format projet Desktop ; sélection base SQL ; séparateurs DAX ; interactions visuelles ; connexion cloud et SSO désactivé ; alerte Viewer/F64 |
| Préparation | Permissions réelles API/tenant ; ReadAll manuel ; contrat de l'option facultative de clonage Power BI |

## Sources et hypothèses

Les conventions MOAW ont été relues depuis le [template corrigé](https://raw.githubusercontent.com/microsoft/moaw/main/template/workshop/workshop.md) et la [référence de syntaxe](https://raw.githubusercontent.com/microsoft/moaw/main/workshops/create-workshop/workshop.md). Les deux autres modèles demandés ont inspiré la structure, pas la prose des exercices. Les parcours Fabric s'appuient sur les pages Learn liées depuis les modules et les guides.

Hypothèses retenues au-delà des décisions validées :

1. Les comptes, le groupe Entra et la capacité sont préparés par une organisation autorisée. Le kit ne les provisionne pas lui-même.
2. Les workspaces sources et destinations restent dans la même région pour les connexions qui le nécessitent.
3. L'année est civile et fixe en 2025 ; le dernier jour est le 31 décembre. Aucune donnée de 2024 n'est inférée.
4. Les facteurs ont une ligne annuelle et deux colonnes ; trois sites ouvrent pendant 2025, aucun ne ferme.
5. Le rapport fourni utilise Import avec une connexion à identité fixe. Le modèle personnel du Lab 7 utilise Direct Lake en SSO.
6. Le groupe bénéficie de ReadAll sur la source. Les permissions fines supplémentaires sont vérifiées, pas automatisées avec une API conjecturale.
7. L'échantillon Bicycles est disponible ; son mapping vers `event_time`, `station_id`, `bike_count` est testé avant diffusion.
8. L'option de clonage reste une interface réservée qui échoue avant toute mutation lorsqu'elle est demandée en mode réel.
9. Les réserves de 20 et 25 minutes servent à l'aide et aux transitions ; les temps d'installation/préparation ne font pas partie de la session.
10. Le lien de rendu cible la branche `main` du dépôt fourni ; aucune publication GitHub n'est effectuée automatiquement.

## État de la recette

| Vérification | État à la rédaction |
| --- | --- |
| Génération et contrôles intégrés | Réussis localement sur le schéma anglais ; six tests de reproductibilité, volumes, résultats et états d'alerte réussis |
| Préparation/suppression | 18 tests hors ligne réussis avec API simulées ; aucun `--apply` réel exécuté |
| Construction MOAW | CLI 1.6.1 ; construction réussie ; 11 pages nommées et titres de navigation identiques ; frontmatter, auteur unique, 415 étapes et totaux 180/300 contrôlés |
| Rendu navigateur v3 | Ordinateur 1440 px et mobile 390 px ; six variables avec valeurs par défaut puis personnalisées, conservation entre pages et URL de rapport avec paramètres vérifiées ; lien Q1 corrigé et chargé en HTTP 200 ; trois CTAS du Lab 6 et Takeaways présents |
| Fichiers publics | Six CSV accessibles anonymement, identiques octet par octet après régénération ; SQL et sources des six cellules du notebook publics et conformes aux fichiers locaux |
| Permissions, six questions d'agent, SQL/DAX/KQL dans Fabric | Non exécutés sur tenant ; répétition obligatoire |
| Alerte lecteur, capacité et réception Teams | Non testés sur tenant ; gate J-7 bloquant |
| Captures, schémas, bannière et projet Power BI réel | Contrôle des assets : 85 références, zéro fichier image présent, zéro modification nécessaire ; 72 écrans des Labs 1 à 5 et 10 compléments commentés ; trois schémas séparés restent actifs ; bannière non référencée ; aucun projet Power BI factice |
| Notebook de préparation | JSON, métadonnées et syntaxe Python contrôlés localement ; exécution Spark/Delta dans Fabric non réalisée |

Les résultats de vérification locale et leurs limites sont à actualiser avant chaque diffusion. Le statut `published: false` demeure tant que le lab n'a pas été testé sur tenant.

La v3 conserve 53 commentaires `TODO vérifier` : Labs 1 à 8, respectivement 4, 12, 6, 7, 6, 3, 4 et 9 ; bonus Copilot, 2. Les commentaires d'images sont distincts de ces vérifications produit. Les trois vérifications d'accès des Labs 1, 4 et 5 restent à effectuer sur tenant ; la recette documentaire ne les valide pas.

### Bilan des étapes v3

Comptage des lignes numérotées écrites, hors blocs de code, comparé au premier commit `c5ec06a`. Les deux variantes d'ingestion sont comptées dans le total du fichier, même si une seule est suivie. Les répétitions indiquées en prose ne sont pas développées artificiellement.

| Page | Premier état | V3 |
| --- | ---: | ---: |
| Introduction | 0 | 0 |
| Lab 1 | 30 | 47, dont 17 facultatives S3 |
| Lab 2 | 102 | 79, soit 65 par Web ou 70 par SharePoint |
| Lab 3 | 69 | 49 |
| Lab 4 | 37 | 35 |
| Lab 5 | 31 | 31 |
| Lab 6 | 65 | 33 |
| Lab 7 | 40 | 40 |
| Lab 8 | 72 | 72 |
| Bonus | 19 | 19 |
| Conclusion | 10 | 10 |
| **Total écrit** | **475** | **415** |

Dans le Lab 2, une seule source est utilisée, dont une correction de type conditionnelle. La planification facultative n'est pas un critère de réussite. La variante S3 et le bonus Copilot restent hors des 180/300 minutes. Les références de captures ne modifient pas le nombre des étapes.

Hypothèses v3 : l'introduction conserve dix minutes d'accueil ; les durées des labs restent inchangées. Les six CSV sont publics et régénérables, sans modification des valeurs, et Q4 reste à 20 000 kWh. Le notebook prépare aussi l'historique propre nécessaire au rapport, en plus des trois tables de référence/instantané demandées. L'exemple Q1 est téléchargeable pour éviter tout support séparé. Les trois schémas attendus restent actifs sans image factice ; les noms des captures suivent désormais le catalogue par écran. Les paramètres de session ne sont ni des secrets ni un mécanisme d'autorisation.

## Faire votre premier test de bout en bout

Prévoir un temps de préparation distinct du parcours chronométré. Avec un seul compte, suivre la variante **Autonomie** ci-dessous pour vérifier les manipulations. Pour valider ensuite les restrictions de la session guidée, utiliser deux comptes distincts : animateur et participant. Tester uniquement avec le compte créateur ne valide pas Viewer + ReadAll ni l'alerte depuis un rapport en lecture. Garder les résultats de répétition dans un support privé, sans identifiant de tenant dans le dépôt.

### Variante Autonomie : un compte, un workspace

Cette variante prépare les mêmes tables de démonstration sans script REST, liste de participants ni dépôt manuel de CSV. Elle est destinée à un test individuel ou à un apprentissage autonome. La préparation, y compris le rapport, reste hors des 3 h / 5 h de manipulation.

1. Ouvrir Fabric avec son compte d'organisation.
2. Créer un workspace personnel de démonstration, ou conserver celui déjà créé, avec droit de création d'items.
3. Vérifier qu'il est rattaché à une capacité Fabric payante active et que les licences nécessaires sont disponibles.
4. Dans ce workspace, créer `lh_source` avec les schémas activés.
5. Télécharger [setup_lh_source.ipynb](https://raw.githubusercontent.com/AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/main/setup/setup_lh_source.ipynb).
6. Importer le notebook **dans le même workspace** suivant [setup/README.md](../setup/README.md#préparer-lh_source-avec-le-notebook).
7. Attacher `lh_source` comme lakehouse par défaut.
8. Exécuter les cellules 2 à 4 ; laisser `apply_after = False` en cellule 6.
9. Vérifier les quatre tables Delta et leurs volumes : 30, 1, 10 840 et 30 lignes.
10. Construire `energy_report` et son modèle dans ce même workspace avec [report/README.md](../report/README.md), avant le Lab 5.
11. Ouvrir le workshop avec `shared_ws` et `lab_ws` renseignés avec **le même nom de workspace**.
12. Suivre le Lab 1 : créer `lh_lab`, puis ses raccourcis OneLake vers `lh_source` de ce workspace.
13. Poursuivre le Lab 2 avec l'URL publique, puis les autres labs ; ne pas utiliser les tables préchargées de `lh_source` comme destination de son Dataflow personnel.

Exemple fictif :

<https://aka.ms/ws?src=gh:AmineLemsih/hands-on-lab-microsoft-fabric-end-to-end/main/docs/&vars=shared_ws:ws-lab-demo,lab_ws:ws-lab-demo,contact:vous-m%C3%AAme>

Sans canal d'atelier, utiliser ses notes personnelles ; la notification du Lab 5 est destinée à son propre compte Teams. Ouvrir `energy_report` dans le même workspace si `report_link` n'est pas renseigné. Les identifiants techniques `lh_source`, `lh_lab` et les tables restent inchangés ; seule la séparation des workspaces disparaît.

Pour l'alerte : créer et activer la règle, attendre l'observation de `before`, puis exécuter la cellule 6 avec `apply_after = True`. Remettre le paramètre à False et actualiser `sm_energy_report`. Pour revenir à l'état initial, relancer les cellules 2 à 4. Ne pas réinitialiser la table entre le franchissement et sa détection.

Ne pas s'attribuer Fabric Administrator pour commencer : ce rôle tenant n'est pas le rôle Administrateur du workspace. Si le data agent ou les alertes sont indisponibles, faire vérifier les paramètres concernés par une personne autorisée. Un succès avec son propre compte reste un test fonctionnel, pas une preuve que les permissions du groupe de participants sont correctes.

En fermeture, arrêter les règles et flux créés, puis supprimer uniquement les éléments de démonstration prévus. Un workspace créé manuellement n'est pas dans le journal du script de suppression ; ne pas supposer qu'il sera nettoyé par celui-ci. Ne jamais supprimer un workspace préexistant qui contient d'autres travaux.

### Préparer une session à un participant

1. Faire confirmer une capacité payante active, la région et les licences nécessaires. Ne pas démarrer ou redimensionner une capacité mutualisée sans autorisation de son propriétaire.
2. Suivre [setup/README.md](../setup/README.md) avec une seule ligne dans la liste privée des participants : simulation, examen du plan, puis exécution réelle autorisée. Conserver le journal pour le nettoyage.
3. Vérifier Membre sur l'espace personnel, Viewer sur l'espace commun, puis partager `lh_source` avec ReadAll au groupe participant. Vérifier que le compte n'hérite pas d'un rôle plus élevé par un autre groupe.
4. Importer le notebook [setup_lh_source.ipynb](../setup/setup_lh_source.ipynb), l'attacher à `lh_source` et exécuter les cellules 2 à 4. Les CSV sont déjà publics ; la génération locale sert seulement à les régénérer à l'identique.
5. Construire et publier le vrai `energy_report` selon [report/README.md](../report/README.md), avec son modèle à identité fixe ; aucun rapport Power BI prêt à importer n'est livré dans le kit.
6. Préparer le lien de session. Choisir une seule variante d'ingestion et omettre S3 et Copilot pour la première passe.

### Vérifier d'abord les trois points bloquants

| Section | Action avec le compte participant | Réussite attendue |
| --- | --- | --- |
| 1 | Créer `lh_lab` et ses raccourcis, puis ouvrir les données avec Viewer + ReadAll sur la source | Lecture de `sites` et `emission_factors`, pas seulement visibilité de leurs noms |
| 4 | Chercher et ouvrir la création de « Agent de données Fabric » dans l'espace personnel ; le configurer après l'ingestion | Élément disponible avec la capacité et les paramètres tenant retenus, puis lecture effective des trois tables |
| 5 | Ouvrir `energy_report` en lecture, créer la règle régionale à 10 000 kWh et choisir le workspace personnel comme destination | Règle enregistrée dans `act_energy`, puis notification personnelle Teams après franchissement réel |

Pour le test du Lab 5, le compte animateur suit « Déclenchement contrôlé » : état `before` observé, cellule 6 de bascule `after`, puis actualisation de `sm_energy_report`. Noter les heures de fin d'actualisation, d'action Activator et de réception Teams. Ne pas assimiler une notification de test à une détection réelle. F64 est un repli à faire approuver et tester, pas un substitut aux permissions.

### Dérouler et chronométrer

Suivre ensuite le workshop dans l'ordre avec le compte participant. Si la vérification initiale a déjà créé un élément, le réutiliser pour la recette fonctionnelle ; pour mesurer le temps d'un vrai débutant, prévoir ensuite un espace personnel vierge. Réexécuter les cellules 2 à 4 et actualiser le modèle avant de refaire le Lab 5.

Noter pour chaque section : durée réelle, étape bloquante, libellé observé, résultat attendu/obtenu et message d'erreur. Vérifier les 10 840 lignes après ingestion et relance manuelle du pipeline, les 72 couples région/mois, puis les six questions avec `data/csv/questions_expected_answers.md`. Valider l'exemple Q1 téléchargeable sur le tenant avant la session. Ne pas confondre son seuil Q4 de 20 000 kWh par site/jour avec l'alerte régionale de 10 000 kWh.

Le Lab 2 représente **65 étapes par Web**, ou 70 avec SharePoint, et non les 79 étapes des deux variantes réunies : mesurer s'il tient en 35 minutes avec les contrôles. Le Lab 8 représente **72 étapes pour 35 minutes** : mesurer avec un profil analyste et consigner le dépassement éventuel. Il reste hors parcours métiers 3 h ; ne pas le raccourcir sans retour de répétition.

Pour le parcours complet, poursuivre les Labs 6 à 8 après réussite du tronc commun, puis ouvrir la page Conclusion. Garder S3 et Copilot pour des passes séparées. Le simulateur de compteurs vers Eventstream reste une piste du backlog, non implémentée dans la v3.

À la fin, suivre la checklist de nettoyage : arrêter les flux, alertes et éventuelles planifications, vérifier le journal avant suppression, puis remettre la capacité de formation dans l'état convenu. Transmettre pour correction les résultats de répétition anonymisés, section et étape à l'appui. Maintenir `published: false` tant que la recette tenant n'est pas terminée.