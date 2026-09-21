# Product Hands-on Lab - Microsoft Fabric de bout en bout

Un atelier hands-on réutilisable pour relier données, analyse et action dans Microsoft Fabric. Contoso, entreprise fictive multi-sites, suit l'énergie et l'empreinte carbone de ses bâtiments. Les données sont synthétiques et les facteurs carbone fictifs.

Le kit est conçu pour être animé par n'importe quel CSA, ou architecte de solutions cloud, dans un environnement autorisé. Aucun nom de client, URL de tenant, secret ou lien privé n'est intégré au contenu public.

**État : brouillon, `published: false`.** Les contrôles locaux ne remplacent pas une répétition sur tenant. Les images sont des placeholders. Aucun fichier Power BI factice n'est fourni. Le parcours d'alerte depuis le rapport partagé est un test J-7 bloquant avant une session individuelle.

## Les deux parcours

| Parcours | Contenu | Public | Durée |
| --- | --- | --- | ---: |
| **Parcours métiers 3 h** | Sections 0 à 5, puis 10 ; pas de code à écrire ; blocs « Comprendre » sautés | Analystes métier, projets, contrôle de gestion, RSE ; distanciel, 15 à 20 participants | 145 min d'activités + 15 min de pause + 20 min d'aide |
| **Parcours complet 5 h** | Tronc commun, cinq blocs « Comprendre », extensions 6 à 8, conclusion | Analystes, journée d'upskilling en présentiel | 225 min d'activités + 25 min d'explications + 25 min de pauses + 25 min d'aide |

La section 9, **Bonus Copilot**, demande environ 15 minutes supplémentaires, si le temps et les paramètres du tenant le permettent. Elle n'entre dans aucun des deux totaux. La seconde pause de 10 minutes intervient après la section 7.

La **variante S3** de la section 1 demande 10 minutes supplémentaires, hors minutage, uniquement si la fiche participant indique qu'elle est disponible.

La section 2 conserve son créneau de 35 minutes avec exécution manuelle du pipeline ; la planification n'est qu'une option du bloc « Comprendre ». La section 6 dure 20 minutes : les dix minutes gagnées portent la réserve du parcours complet à 25 minutes. L'introduction garde dix minutes d'accueil, dont environ cinq de lecture.

## Ouvrir l'atelier

- [Rendu MOAW](https://aka.ms/ws?src=gh:aminelemsih/hands-on-lab-microsoft-fabric-end-to-end/main/docs/).
- [Source du workshop](docs/workshop.md).
- [Dépôt GitHub cible](https://github.com/aminelemsih/hands-on-lab-microsoft-fabric-end-to-end).
- [Mother Of All Workshops](https://aka.ms/moaw).

Le lien de rendu devient utilisable après publication des fichiers sur la branche `main`. `published: false` empêche le référencement dans le catalogue, **pas l'accès par lien direct** : ce n'est pas une protection de confidentialité. La création locale du kit n'effectue ni commit ni push.

## Prévisualisation locale

Prérequis animateur/auteur : Node.js 20 ou ultérieur et npm. Depuis la racine :

```powershell
npm i -g @moaw/cli
moaw serve docs
```

La CLI indique l'URL locale, ici `http://localhost:4444/workshop/docs/`. Si le port est occupé :

```powershell
moaw serve docs --port 4445
```

Contrôle de construction, après génération des données :

```powershell
moaw build docs/workshop.md -d data/out/workshop.build.md
```

Les images manquantes sont attendues dans ce brouillon ; leur inventaire est dans [docs/assets/SCREENSHOTS-TODO.md](docs/assets/SCREENSHOTS-TODO.md). Ne pas les remplacer par des images générées ou des captures contenant un tenant réel.

## Pour les animateurs

Commencer par [docs/facilitator-notes.md](docs/facilitator-notes.md), puis remplir une copie privée de [docs/participant-sheet.template.md](docs/participant-sheet.template.md).

| Ressource | Utilisation |
| --- | --- |
| [setup/README.md](setup/README.md) | Préparer les workspaces et les accès ; simulation par défaut ; nettoyage confirmé |
| [data/README.md](data/README.md) | Générer les CSV, charger les tables et préparer les deux états d'alerte |
| [report/README.md](report/README.md) | Construire et publier le vrai rapport fourni `energy_report` |
| [docs/assets/SCREENSHOTS-TODO.md](docs/assets/SCREENSHOTS-TODO.md) | Réaliser les captures anonymisées |

Les participants sont Membre dans leur espace `ws-lab-<email_local_part>` et Viewer dans l'espace commun `ws-shared`. Le groupe reçoit aussi le partage explicite ReadAll sur `lh_source`. Le modèle de `energy_report` utilise une connexion à identité fixe ; chaque participant enregistre son alerte dans son espace personnel, sans copier le rapport. Ce chemin est à répéter sur la capacité cible. L'option `--clone-report` reste désactivée et non implémentée tant que son API n'est pas validée.

Tous les identifiants techniques sont anglais : noms de fichiers, colonnes, tables et items. Le texte reste français. Ne traduisez pas `consumption` ni `emission_factors` dans une adaptation linguistique. Les chemins documentaires sont également anglais pour rester stables.

## Contrôles locaux

```powershell
python data/generate_data.py
python -m unittest discover -s data -p "test_*.py" -v
python -m unittest discover -s setup -p "test_*.py" -v
```

Attendus : 30 sites, une ligne de facteurs annuels avec deux coefficients, 10 950 lignes brutes, 110 rejets, 10 840 lignes propres, six pics historiques et 30 lignes par instantané. Toutes les régions sont sous 10 000 kWh dans l'état avant ; seule la Bretagne dépasse le seuil dans l'état après. Q4 conserve son seuil distinct de 20 000 kWh par site et jour.

Les fichiers générés et les paramètres réels restent exclus de Git. Le corrigé est calculé dans `data/out/questions_expected_answers.md`. Aucun script n'est exécuté en mode réel lors des tests locaux.

## Backlog

- **Simulateur de compteurs, script Python vers un endpoint personnalisé d'Eventstream.** La v1 utilise les données d'exemple intégrées, sans les présenter comme de l'énergie.
- Valider puis implémenter l'option facultative `--clone-report` avec les droits et le journal adaptés, sans en faire un prérequis du parcours nominal.
- Réaliser les captures et la répétition tenant avant de passer `published` à `true`.

## Auteur

**Amine Lemsih**, conception et rédaction de l'atelier. Contact : **@aminelemsih**. Auteur unique du frontmatter et du kit.

## Contributeurs

La liste [CONTRIBUTORS.md](CONTRIBUTORS.md) est volontairement vide à ce stade. Les contributions ne changent pas automatiquement la paternité indiquée dans les métadonnées.

## Contribuer

Utiliser les issues et demandes de tirage du dépôt. Indiquer le module, l'étape, le comportement attendu et le résultat constaté. Fournir uniquement des données synthétiques et des captures anonymisées. Maintenir les minutages, les identifiants anglais et les contrôles du jeu de données.

Conventions suivies, sans reprise du texte des exercices : le template et la [syntaxe MOAW](https://aka.ms/ws?src=create-workshop/), le lab Microsoft Agent Framework avec Microsoft Foundry, le workshop FabConRTI et les [exercices Microsoft Learn Fabric](https://microsoftlearning.github.io/mslearn-fabric/). Les modèles ne sont pas crédités comme co-auteurs de cet atelier.

## Licences

- **Code et extraits de code : MIT**, voir [LICENSE](LICENSE).
- **Contenu pédagogique, guides Markdown, données synthétiques et futures captures : CC BY-SA 4.0**, voir [docs/LICENSE](docs/LICENSE), y compris les guides situés hors du dossier docs.
- Les marques Microsoft et les ressources externes gardent leurs droits et conditions propres. Les facteurs fictifs n'accordent aucune validité à un reporting réel.

Attribution à reproduire : **« Product Hands-on Lab - Microsoft Fabric de bout en bout », Amine Lemsih, https://github.com/aminelemsih/hands-on-lab-microsoft-fabric-end-to-end, contenu sous CC BY-SA 4.0.** Indiquer les modifications lors d'une adaptation.