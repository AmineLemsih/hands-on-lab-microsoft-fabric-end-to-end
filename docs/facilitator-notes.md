# Notes animateur

**Product Hands-on Lab - Microsoft Fabric de bout en bout**  
Auteur unique : **Amine Lemsih**, conception et rédaction. Kit réutilisable par un CSA ou un animateur autorisé, sans contenu client dans le dépôt.

Le [workshop](workshop.md) contient les manipulations. Ce guide couvre la préparation et les vérifications que les participants ne doivent pas avoir à découvrir pendant la session. La [fiche participant](participant-sheet.template.md) est remplie et distribuée en privé.

## Contrat de livraison

Le texte est français, tous les identifiants techniques sont anglais. Noms génériques : `ws-shared`, `ws-lab-<email_local_part>`, `lh_source`, `lh_lab`, `energy_agent`, `energy_report`. Les noms exacts et liens de la session restent sur les fiches privées. Le fichier `workshop.md` ne doit pas devenir une fiche client.

La table `consumption` (consommation) contient les observations annuelles nettoyées. `emission_factors` (facteurs d'émission) contient une ligne par année et deux colonnes de coefficients. `consumption_latest_day` (consommation du dernier jour disponible) contient uniquement le dernier jour simulé. Cette granularité doit rester identique dans le rapport, SQL, DAX et les instructions de l'agent.

**Statut initial : `published: false`.** Génération locale, tests sur API simulées et rendu MOAW ne prouvent pas le fonctionnement dans Fabric. Le passage à `true` attend la répétition tenant, la résolution des points bloquants et les captures.

## Checklist J-7

- [ ] Confirmer 15 à 20 inscrits, les comptes dans le tenant et le parcours retenu. Prévoir un animateur et, si possible, un second intervenant pour l'assistance distancielle.
- [ ] Préparer le groupe de sécurité Entra contenant les participants ; contrôler les invités et leurs identifiants dans le tenant d'accueil.
- [ ] Confirmer les licences : droits de création Fabric, licence Power BI adaptée pour les exercices d'auteur, Pro ou compatible pour lire le rapport sous F64. Prévoir Pro pour les analystes qui créent les modèles de la section 7.
- [ ] Vérifier la capacité **payante**, la région, les fonctionnalités disponibles et le budget de la session. La capacité minimale d'une fonction ne constitue pas un dimensionnement pour 20 personnes.
- [ ] Faire un test de concurrence représentatif : quelques Dataflows simultanés, endpoint SQL, agent, modèle et flux temps réel. Échelonner les exécutions si nécessaire.
- [ ] Exécuter la simulation de [préparation](../setup/README.md), vérifier les noms, puis autoriser séparément les écritures réelles. Conserver le journal local.
- [ ] Vérifier Membre sur chaque workspace personnel et Viewer sur le workspace commun.
- [ ] Partager **explicitement `lh_source` avec le groupe**, option `ReadAll`, « Lire toutes les données Apache Spark » / « Lire toutes les données OneLake » selon l'interface. <!-- TODO vérifier --> Ce partage ajoute Read mais n'accorde pas Write. Tester le raccourci avec un compte participant, pas l'administrateur.
- [ ] Vérifier les politiques de sécurité OneLake et, si elles sont actives, le rôle de lecture de la source. Tester Direct Lake en SSO depuis le modèle personnel et ses raccourcis.
- [ ] Contrôler les paramètres tenant Copilot / Azure OpenAI intégré et data agents, leurs groupes autorisés et leur disponibilité régionale. Les libellés et règles de traitement/stockage interrégional doivent être vérifiés dans la documentation courante et avec l'organisation. <!-- TODO vérifier --> Ne pas activer une option cross-geo sans approbation.
- [ ] Créer un data agent de test sur les tables du lab. Vérifier les six questions, les instructions françaises, l'exemple validé et l'affichage des requêtes. Aucun secret Azure OpenAI n'est nécessaire pour le chat intégré.
- [ ] Répéter les deux variantes CSV. Choisir une variante par session et l'indiquer sur la fiche. Vérifier locale décimale, suppression des erreurs et nombre final de lignes.
- [ ] Répéter les opérations visuelles de la section 3 jusqu'à l'enregistrement de la vue. La simple lecture du SQL de référence ne valide pas le parcours sans code.
- [ ] Construire `energy_report` et `sm_energy_report`, puis associer la source à `conn_energy_report`, connexion à identité fixe, SSO désactivé. Tester l'actualisation et la lecture du rapport avec le compte Viewer.
- [ ] Effectuer le **test bloquant « Définir une alerte » depuis `energy_report` sur la capacité cible**, avec compte Viewer dans `ws-shared` et Membre dans son espace personnel. Enregistrer `act_energy` dans l'espace personnel, sans copier le rapport. <!-- TODO vérifier -->
- [ ] Vérifier l'exigence **F64 ou plus** indiquée pour le parcours d'alertes Power BI retenu, ainsi que le paramètre tenant autorisant le bouton. <!-- TODO vérifier --> Prévoir une montée temporaire PAYG en F64, approuvée et chiffrée, puis refaire le test avec exactement les mêmes permissions.
- [ ] Mesurer la latence réelle du franchissement avant/après jusqu'à Teams. Préparer une capture de la notification et de l'historique comme plan B.
- [ ] Pour le parcours complet, vérifier Upsert/staging du pipeline Warehouse, mesure DAX Direct Lake, échantillon Bicycles et champs KQL, mappage et destination Activator.
- [ ] Pour le bonus seulement, tester Copilot dans Dataflow Gen2 et dans le jeu de requêtes KQL. Son indisponibilité ne bloque pas les deux parcours principaux.

### Le point d'attention Viewer et F64

Le parcours demandé part du **rapport commun en lecture**, avec une alerte dans le workspace personnel. Le modèle utilise une identité fixe ; cela porte l'accès aux données, pas les droits d'édition du rapport.

La page [Activator depuis Power BI](https://learn.microsoft.com/fabric/real-time-intelligence/data-activator/activator-get-data-power-bi), consultée pendant la rédaction, décrit une expérience exigeant **Edit** sur le rapport. La condition F64 et l'accès depuis la lecture doivent donc être reconfirmés pour le parcours réellement disponible dans le tenant. <!-- TODO vérifier --> Ne pas présenter Viewer + F64 comme un fonctionnement testé alors que seule la documentation a été lue.

Plan B capacité : l'administrateur fait approuver le coût, monte la capacité PAYG de formation en F64 pour la session, puis la ramène à son niveau prévu ou la met en pause après nettoyage. **Ne pas redimensionner ni arrêter une capacité mutualisée sans autorisation.** Une montée de capacité ne corrige pas une permission Edit manquante.

Si le chemin lecteur n'est toujours pas disponible, annoncer avant la session que la section 5 sera une démonstration animateur et une analyse de capture. Ne pas ouvrir le workspace commun en écriture ni glisser une copie personnelle dans le parcours sans l'annoncer. `--clone-report` est seulement une option de préparation réservée, désactivée et non implémentée avant validation de l'API.

La documentation des anciennes alertes sur tuiles de dashboard ne valide pas ce scénario : le lab cible Activator sur le **visuel d'un rapport**, pas une tuile KPI.

## Checklist J-1

- [ ] Remplir une fiche privée par participant : tenant, compte, deux workspaces, rapport, fichier, Teams, contact, heure/fuseau et fin de planning.
- [ ] Générer les données et conserver le corrigé calculé. Vérifier 30 sites, une ligne de facteurs, 10 950 lignes brutes et 10 840 propres.
- [ ] Déposer les fichiers selon [data/README.md](../data/README.md). Vérifier les types des tables Delta, pas seulement la présence des CSV.
- [ ] Préparer `consumption` nettoyée dans `lh_source` pour le rapport ; préparer `df_source_latest` séparément pour les changements en direct.
- [ ] Charger l'état `before` dans le fichier actif, exécuter le flux, puis actualiser le modèle. Vérifier que les six régions sont sous le seuil de 20 000 kWh.
- [ ] Vérifier le rapport partagé, son lien, son modèle à identité fixe et sa dernière actualisation réussie.
- [ ] Préparer un raccourci de démonstration et un workspace animateur, distincts des espaces participants.
- [ ] Contrôler les tables du data agent de démonstration et les exemples. Conserver le corrigé accessible sans devoir exécuter un notebook en session.
- [ ] Préparer les captures listées dans [assets/SCREENSHOTS-TODO.md](assets/SCREENSHOTS-TODO.md), notamment le plan B de notification.
- [ ] Confirmer le résultat du test Viewer/F64 et annoncer le mode individuel ou démonstration pour la section 5.
- [ ] Garder les fichiers `before` et `after` locaux. Ne pas les combiner avec le fichier actif dans une source par dossier.
- [ ] Vérifier le rendu MOAW sur ordinateur et mobile. Garder les captures tenant privées tant qu'elles ne sont pas anonymisées.

## Checklist jour J

- [ ] Allumer ou reprendre **la capacité de formation autorisée** avant l'arrivée des participants. Vérifier son état, la capacité choisie pour le rapport et la disponibilité des items.
- [ ] Ouvrir Fabric avec le compte de test et confirmer les deux vérifications de la fiche : connexion/accès et licence.
- [ ] Afficher le parcours retenu et les horaires de pause. Rappeler que Copilot est un bonus hors minutage.
- [ ] Présenter le nommage anglais et les données fictives ; rappeler que les erreurs sont volontairement présentes.
- [ ] Noter les difficultés dans un support privé, sans jeton ni données client dans le canal public.
- [ ] Utiliser la réserve d'aide pour les connexions, la synchronisation SQL et les vérifications des résultats. Ne pas supprimer une étape de contrôle pour tenir le temps.
- [ ] En section 5, attendre que les règles soient actives et aient observé l'état sous le seuil avant de charger `after`.
- [ ] En fin de section 8, arrêter les règles de démonstration répétitives et le flux dès qu'ils ne sont plus utilisés, en coordination avec les participants.

## Minutage des deux parcours

Les horaires sont relatifs au début. La réserve en fin de tableau peut être répartie plus tôt ; elle n'ajoute pas de nouvelles activités.

### Parcours métiers 3 h

| Horaire | Activité | Minutes |
| --- | --- | ---: |
| 00:00 - 00:10 | 0. Introduction | 10 |
| 00:10 - 00:30 | 1. Prise en main | 20 |
| 00:30 - 01:05 | 2. Ingestion | 35 |
| 01:05 - 01:20 | Pause | 15 |
| 01:20 - 01:45 | 3. Exploration | 25 |
| 01:45 - 02:15 | 4. Data agent | 30 |
| 02:15 - 02:30 | 5. Alerte | 15 |
| 02:30 - 02:50 | Aide, transitions et questions, réaffectables | 20 |
| 02:50 - 03:00 | 10. Conclusion | 10 |
| **Total** | 145 activités + 15 pause + 20 réserve | **180** |

Les cinq blocs « Comprendre », les extensions et Copilot ne sont pas lus dans ce parcours. Le copier-coller d'un exemple généré et vérifié pour l'agent ne demande pas d'écrire du SQL.

### Parcours complet 5 h

| Horaire | Activité | Minutes |
| --- | --- | ---: |
| 00:00 - 00:10 | 0. Introduction | 10 |
| 00:10 - 00:35 | 1. Prise en main + Comprendre | 25 |
| 00:35 - 01:15 | 2. Ingestion + Comprendre | 40 |
| 01:15 - 01:30 | Première pause | 15 |
| 01:30 - 02:00 | 3. Exploration + Comprendre | 30 |
| 02:00 - 02:35 | 4. Data agent + Comprendre | 35 |
| 02:35 - 02:55 | 5. Alerte + Comprendre | 20 |
| 02:55 - 03:25 | 6. Entrepôt et T-SQL | 30 |
| 03:25 - 03:50 | 7. Direct Lake | 25 |
| 03:50 - 04:00 | Deuxième pause | 10 |
| 04:00 - 04:35 | 8. Temps réel | 35 |
| 04:35 - 04:50 | Aide, transitions et questions, réaffectables | 15 |
| 04:50 - 05:00 | 10. Conclusion | 10 |
| **Total** | 145 tronc + 90 extensions + 25 explications + 25 pauses + 15 réserve | **300** |

La section 9 demande environ 15 minutes **supplémentaires**. Ne pas l'ajouter tacitement à 5 h, ni retirer la seconde pause pour la caser. Si le groupe finit réellement en avance, l'animateur peut l'utiliser sans dépasser l'horaire annoncé.

## Déclenchement contrôlé en section 5

Le seuil de **20 000 kWh** est évalué **par région**. Il ne faut pas confondre ce seuil régional avec la question Q4 de l'agent, qui l'applique par couple site/jour. Les deux sont intentionnels, mais de granularités différentes.

### Avant les règles

1. Préparer le fichier actif avec le contenu `before`.
2. Remplacer `consumption_latest_day.csv` dans « Fichiers » de `lh_source`.
3. Exécuter `df_source_latest`.
4. Attendre son état de réussite.
5. Contrôler les 30 lignes de `consumption_latest_day`.
6. Actualiser `sm_energy_report`.
7. Attendre la réussite de l'actualisation.
8. Vérifier le visuel « consommation du dernier jour disponible par région ».
9. Faire créer et démarrer les règles des participants.
10. Attendre que l'observation de départ soit visible dans les règles, selon la latence mesurée à J-7.

Commande locale de préparation du fichier, sans action cloud :

```powershell
Copy-Item data/out/consumption_latest_day_before.csv data/out/consumption_latest_day.csv -Force
```

### Pendant la démonstration en direct

1. Préparer le fichier actif avec le contenu `after`.
2. Remplacer le même fichier dans `lh_source`, en conservant son nom.
3. Exécuter `df_source_latest`.
4. Attendre sa réussite.
5. Vérifier que la table conserve 30 lignes.
6. Actualiser `sm_energy_report`.
7. Noter l'heure de fin d'actualisation.
8. Vérifier que la Bretagne passe de **2 724,55 à 36 724,55 kWh**.
9. Observer l'historique des actions Activator.
10. Noter l'heure de réception Teams et la latence constatée.

```powershell
Copy-Item data/out/consumption_latest_day_after.csv data/out/consumption_latest_day.csv -Force
```

Le CSV annuel, les sites et les facteurs ne changent pas. La table des facteurs garde la mention « fictif, ne pas utiliser pour un reporting réel ». Les autres régions restent sous le seuil. Le visuel ne doit pas avoir d'axe temporel : Activator peut ignorer la correction d'un point temporel déjà examiné.

### Si la notification arrive trop tard

Montrer les observations, la condition et les étapes déjà réussies, puis la capture de répétition. Dire explicitement qu'elle a été reçue avant la session. Ne pas afficher « test réussi aujourd'hui » sans notification/action correspondante. Ne pas déclencher une série de changements de seuil ou de rafraîchissements incontrôlés.

![Plan B : notification reçue lors d'une répétition identifiée, destinataire anonymisé](assets/05-alert-notification.png)

## Pièges connus et reprise

### Consignes déplacées du workshop

Les passages ci-dessous ont été retirés du texte participant lors de la relecture. Les extraits gardent leur origine pour faciliter la revue ; les procédures actives et les checklists de ce guide font foi.

| Section source | Phrases déplacées et consigne conservée ici |
| --- | --- |
| 0, modalités | « Les temps d'aide sont répartis par l'animateur. » |
| 0, architecture et fiche | « L'animateur prépare et actualise les données. » ; « Votre animateur vous transmet une fiche participant privée. » |
| 0, Préparation obligatoire de l'alerte | « L'animateur teste à J-7 le bouton Définir une alerte depuis le rapport commun avec un compte Viewer, sur la capacité cible, en choisissant un workspace personnel comme destination. » Les prérequis de capacité et d'édition diffèrent selon l'expérience disponible ; le test autorise le déroulement individuel, sans copie nominale du rapport. |
| 0, auteur | « Les animateurs réutilisent le kit sans ajouter de contexte client au document public. » |
| 1, dépannage | « L'animateur contrôle le rôle Viewer. » ; « L'animateur adapte le chemin si le lakehouse source est sans schémas. » Vérifier aussi ReadAll et sa propagation si l'item est visible mais sa donnée refusée. |
| 2, contrôle et pause | Accompagner le contrôle des lignes écrites si les détails d'exécution sont difficiles à lire ; « L'animateur annonce l'heure de reprise. » |
| 3, vue et contrôle | « Toutes les transformations doivent pouvoir être traduites en SQL par l'éditeur ; l'animateur vérifie ce parcours visuel avant la session. » ; « L'animateur dispose du corrigé calculé pour comparer les résultats. » Ne pas substituer du SQL au parcours visuel sans l'annoncer. |
| 4, exemple et dépannage | « Si Q1 n'est pas correcte, l'animateur la vérifie avec vous avant l'ajout. » ; « L'animateur vérifie la capacité payante, la région et les paramètres tenant des data agents et de l'IA. » ; « Testez les instructions en français avant diffusion. » La capacité d'essai ne suffit pas au parcours prévu. |
| 5, bouton indisponible | « Ce chemin doit avoir été validé à J-7 avec les mêmes droits et la même capacité. » ; « La documentation décrit également une expérience demandant Edit sur le rapport. » ; « L'animateur applique le plan B annoncé. » Ne pas accorder l'écriture sur l'espace commun ni imposer une copie sans annonce. |
| 5, changement des données | « L'animateur remplace uniquement le fichier actif du dernier jour, recharge sa table puis actualise le modèle. » Vérifier `df_source_latest` et `sm_energy_report` avec son identité fixe si le rapport ne change pas. |
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
| Upsert après un Insert en double | Le chargement par clé ne supprime pas les doublons existants ; remettre la cible de démonstration à zéro avant reprise. |
| Direct Lake en erreur | Vérifier les relations et les accès de l'utilisateur/propriétaire à la cible des raccourcis. Ne pas remplacer discrètement SSO par une identité fixe dans l'exercice personnel. |
| KQL vide | Contrôler noms et types mappés, casse, plage des dates de l'échantillon et arrivée de nouvelles données. |

Prévoir les résultats de référence pour poursuivre une explication si un participant est bloqué. Une démonstration animateur ne compte pas comme une manipulation individuelle terminée.

## Checklist après la session

- [ ] Confirmer que chacun a enregistré ce qu'il doit conserver ; ne pas supprimer sans l'accord prévu pour la session.
- [ ] Arrêter les planifications quotidiennes, règles Activator et Eventstreams créés pour le lab.
- [ ] Révoquer ou examiner les connexions et partages créés pour la session selon la politique de l'organisation.
- [ ] Exécuter la simulation de suppression sur le journal, puis autoriser la suppression explicite des workspaces personnels. Ajouter l'espace commun uniquement s'il a été créé pour cette session et n'est plus utilisé.
- [ ] Examiner manuellement un espace commun préexistant : le script ne le supprime pas et ne retire pas automatiquement les partages ajoutés.
- [ ] Remettre la capacité PAYG de formation au niveau prévu ou la mettre en pause avec l'autorisation de son propriétaire. Faire le nettoyage avant la pause pour garder les API disponibles ; une reprise temporaire peut être nécessaire sinon.
- [ ] Publier l'enregistrement dans l'emplacement autorisé et le partager via la fiche/canal privé, avec consentement et contrôle des captures. Aucun lien client dans le workshop public.
- [ ] Archiver le journal privé selon les règles de rétention, puis retirer les jetons de l'environnement local. Ne jamais les consigner dans le compte rendu.
- [ ] Reporter les corrections génériques dans le dépôt sans données ni identifiants de client.

## Adapter à un client en 30 minutes

| Budget | Action |
| --- | --- |
| 0 - 10 min | Remplir les fiches privées : URL tenant, comptes, workspaces, rapport, fichier, Teams, contact. Vérifier les deux contrôles avant session. |
| 10 - 20 min | Garder les données synthétiques par défaut. Facultativement préparer un extrait client non sensible **au même schéma**, autorisé et stocké uniquement dans l'environnement privé. |
| 20 - 30 min | Adapter oralement ou dans les supports privés « Et chez vous ? », le vocabulaire métier, la décision et le prochain responsable. |

Changer les données exige de **recalculer** les résultats attendus, les dates, le seuil et les deux états. Le corrigé du générateur ne valide que les données synthétiques qu'il a produites. Si cette nouvelle recette n'est pas faisable en 30 minutes, garder le jeu Contoso ; ne pas promettre que tout extrait client est immédiatement compatible.

Ne pas changer les noms techniques pour une traduction. Les seuls éléments contextualisés appartiennent aux fiches et supports privés. Aucun facteur réel ne doit être proposé sans provenance et périmètre approuvés.

## Livrer en journée d'upskilling

Utiliser les supports de présentation existants le matin pour les concepts, la gouvernance, la sécurité et les cas d'usage. Réserver réellement cinq heures l'après-midi, par exemple 13 h - 18 h, pauses comprises. Un créneau de trois heures n'est pas un parcours complet compressé.

Préparer en plus : postes analystes pour copier les requêtes, licences de création Power BI, répétition Direct Lake/DAX, connecteurs et staging Warehouse, échantillon RTI et quotas de capacité, arrêt des flux, appui d'un second animateur si besoin. Précharger seulement les sources communes ; les participants construisent leurs propres éléments. Les corrigés et captures de reprise restent disponibles. Aucun deck ni simulateur de compteurs n'est créé dans la v1 du kit.

## Registre des vérifications produit

Les commentaires `<!-- TODO vérifier -->` restent près de l'instruction concernée. Cette table regroupe leur objet ; retirer un commentaire seulement après observation sur la version de l'interface et le rôle de la session.

| Section ou support | Vérifications regroupées |
| --- | --- |
| 0 | Libellé ReadAll ; droits/chemin d'alerte lecteur ; licences et capacité de la fiche |
| 1 | Case schémas, menu `dbo`, propriétés du raccourci et accès cible |
| 2 | Nommage/publication du flux ; navigation CSV binaire Lakehouse ; navigation Content SharePoint ; locale ; Début du mois ; destination Remplacer ; détails des lignes écrites ; planification |
| 3 | Accès endpoint SQL ; fusion/développement ; opérations arithmétiques sur colonnes ; chargement actif ; repli SQL et sauvegarde de vue sans tri |
| 4 | Libellé agent ; détails de réponse ; instructions françaises ; éditeur et validation d'exemples ; remise à zéro du chat |
| 5 | Bouton alerte en lecture ; F64/tenant ; condition Devient ; workspace destination ; validation et activation ; ouverture/historique Activator ; latence réelle |
| 6 | Libellé Warehouse ; création automatique ; types de mappage ; staging workspace ; Upsert et sélection des clés |
| 7 | Création/édition explicite du modèle ; mode Direct Lake/SSO ; gestion des relations ; permissions des sources de l'agent |
| 8 | Source intégrée/casse/champs ; ingestion directe/configuration/mappage ; jeu KQL ; destination Activator ; objet/propriété/condition ; test d'action distinct du test de franchissement |
| 9 | Disponibilité des deux surfaces Copilot, paramètres tenant/région et chemins français |
| Données | Chargement des fichiers ; ReadAll ; navigation du connecteur Lakehouse |
| Rapport | Format projet Desktop ; sélection base SQL ; séparateurs DAX ; interactions visuelles ; connexion cloud et SSO désactivé ; alerte Viewer/F64 |
| Préparation | Permissions réelles API/tenant ; ReadAll manuel ; contrat de l'option facultative de clonage Power BI |

## Sources et hypothèses

Les conventions MOAW ont été relues depuis le [template corrigé](https://raw.githubusercontent.com/microsoft/moaw/main/template/workshop/workshop.md) et la [référence de syntaxe](https://raw.githubusercontent.com/microsoft/moaw/main/workshops/create-workshop/workshop.md). Les deux autres modèles demandés ont inspiré la structure, pas la prose des exercices. Les parcours Fabric s'appuient sur les pages Learn liées depuis les modules et les guides.

Hypothèses retenues au-delà des décisions validées :

1. Les comptes, le groupe Entra et la capacité sont préparés par une organisation autorisée. Le kit ne les provisionne pas lui-même.
2. Les workspaces sources et destinations restent dans la même région pour les connexions qui le nécessitent.
3. L'année est civile et fixe en 2025 ; le dernier jour est le 31 décembre. Aucune donnée de 2024 n'est inférée.
4. Les facteurs ont une ligne annuelle et deux colonnes ; trois sites ouvrent pendant 2025, aucun ne ferme.
5. Le rapport fourni utilise Import avec une connexion à identité fixe. Le modèle personnel de la section 7 utilise Direct Lake en SSO.
6. Le groupe bénéficie de ReadAll sur la source. Les permissions fines supplémentaires sont vérifiées, pas automatisées avec une API conjecturale.
7. L'échantillon Bicycles est disponible ; son mapping vers `event_time`, `station_id`, `bike_count` est testé avant diffusion.
8. L'option de clonage reste une interface réservée qui échoue avant toute mutation lorsqu'elle est demandée en mode réel.
9. Les réserves de 20 et 15 minutes servent à l'aide et aux transitions ; les temps d'installation/préparation ne font pas partie de la session.
10. Le lien de rendu cible la branche `main` du dépôt fourni ; aucune publication GitHub n'est effectuée automatiquement.

## État de la recette

| Vérification | État à la rédaction |
| --- | --- |
| Génération et contrôles intégrés | Réussis localement sur le schéma anglais ; six tests de reproductibilité, volumes, résultats et états d'alerte réussis |
| Préparation/suppression | 18 tests hors ligne réussis avec API simulées ; aucun `--apply` réel exécuté |
| Construction MOAW | Réussie avec la CLI 1.6.1 ; 11 sections, frontmatter YAML, liens locaux, 28 placeholders et totaux 180/300 contrôlés |
| Rendu navigateur | Introduction, navigation, encadrés, SQL replié/ouvert et trois blocs KQL vérifiés ; ordinateur et mobile 390 px, tableaux défilants ; images absentes prévues |
| Permissions, six questions d'agent, SQL/DAX/KQL dans Fabric | Non exécutés sur tenant ; répétition obligatoire |
| Alerte lecteur, capacité et réception Teams | Non testés sur tenant ; gate J-7 bloquant |
| Captures, bannière et projet Power BI réel | Non produits ; placeholders et guide uniquement |

Les résultats de vérification locale et leurs limites sont à actualiser avant chaque diffusion. Le statut `published: false` demeure tant que le lab n'a pas été testé sur tenant.

Recette locale du 21 septembre 2026 : les 60 commentaires `TODO vérifier` du workshop se répartissent entre les sections 0 à 9 (respectivement 2, 3, 11, 9, 7, 7, 6, 4, 9 et 2). Ils concernent la version française de l'interface et les comportements à répéter sur tenant. Les guides comportent aussi leurs propres points de validation. Le registre ci-dessus les regroupe ; la présence de ces marqueurs exclut une affirmation de validation cloud complète.