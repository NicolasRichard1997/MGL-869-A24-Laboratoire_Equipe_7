Here’s an improved version for clarity, flow, and technical presentation:

---
# MGL869-A24_Laboratoire

## Projet
Ce projet consiste à développer un modèle de machine learning pour prédire les fichiers du logiciel *Apache Hive* les plus susceptibles de contenir des bogues. Cette approche permettra de mieux prioriser les tests, particulièrement essentiel lors des phases finales précédant une nouvelle version.

## Objectifs
- Créer un modèle de prédiction de bogues.
- Identifier les fichiers présentant un risque élevé de bogue.
- Optimiser l'allocation des ressources de test.
- Améliorer la qualité des releases de Hive.

## 1. Extraction des données
La première étape consiste à recueillir les données nécessaires pour le modèle de prédiction en se focalisant sur les versions 2.0.0 et ultérieures de Hive.

### 1.1 Récupération des rapports de bogues sur Jira
Les rapports de bogues sont extraits depuis Jira pour chaque version majeure et mineure (excluant les patchs) à partir de 2.0.0, selon la requête suivante :

```sql
project = HIVE AND issuetype = Bug AND status in (Resolved, Closed) AND affectedVersion = X.Y.0
```

Les résultats sont téléchargés dans différents fichiers au format CSV. À l'aide du fichier `Hive_Concatenate_bug_list.py`, la liste des bogues est concaténée dans le fichier Hive_bug_list.csv` est produit, contenant les informations suivantes:

- Type de problème
- Version
- Clé du problème
- ID du problème
- Résumé
- Attributaire
- Rapporteur
- Priorité
- Statut
- Résolution
- Date de création
- Dernière mise à jour
- Date d’échéance

### 1.2 Identification des fichiers modifiés
À partir du fichier de bogues généré à la dernière étape, les IDs de bogues sont extraits avec le script `Hive_bug_IDs_extraction.py`. Ensuite, le script `Hive_bug_IDs+version_extraction.py` permet d'identifier les fichiers `.java` et `.cpp` modifiés pour chaque bogue ID.

Le résultat final est sauvegardé dans `modified_cpp-java_files.csv` au format suivant :

```csv
<Bug ID 1>,<version>,<fichier modifié Java/C++>,<fichier modifié Java/C++>,
<Bug ID 2>,<version>,<fichier modifié Java/C++>,
<Bug ID 23>,<version>,<fichier modifié Java/C++>,<fichier modifié Java/C++>,<fichier modifié Java/C++>,
[...]
```

### 1.3 Collecte des variables indépendantes avec `Understand`
Dans cette étape, le dernier commit avant chaque release majeure est identifié à l’aide du script `Hive_find_commit_before_release.py`, avec les résultats enregistrés dans `Hive_last_commit_before_release.txt` au format suivant:
```csv
hive-2.0.0: 21cf6ff3789ed94bdf61587e2e73fb94b1d9304c 2016-02-15 07:53:56 -0800
hive-2.1.0: c168af26de36ecb66e606b040c862a222ee2a190 2016-06-20 18:00:32 -0700
hive-2.2.0: 52f1b2471545a797856e4b9b1ae0a36cb4233c18 2018-05-04 14:32:50 -0700
[...]
```

À l'aide de ce fichier, du script `Hive_fetch_UND_variables.py` et du fichier `settings.xml`, on peut récolter les variables d'intérêt pour chacun des fichiers pour chacune des version du logiciel. Les résultats sont stockés dans le répertoire `UND_hive_understand_raw_data` dans des fichiers nommés `UND_hive-X.Y.0_processed.csv`, formattés comme suit:

```csv
Kind,Name,AvgCountLine,AvgCountLineBlank,AvgCountLineCode,AvgCountLineComment,AvgCyclomatic,AvgCyclomaticModified,AvgCyclomaticStrict,AvgCyclomaticStrictModified,AvgEssential,CCViolDensityCode,CCViolDensityLine,CountCCViol,CountCCViolType,CountClassBase,CountClassCoupled,CountClassCoupledModified,CountClassDerived,CountDeclClass,CountDeclClassMethod,CountDeclClassVariable,CountDeclExecutableUnit,CountDeclFile,CountDeclFileCode,CountDeclFileHeader,CountDeclFunction,CountDeclInstanceMethod,CountDeclInstanceVariable,CountDeclInstanceVariablePrivate,CountDeclInstanceVariableProtected,CountDeclInstanceVariablePublic,CountDeclMethod,CountDeclMethodAll,CountDeclMethodConst,CountDeclMethodDefault,CountDeclMethodFriend,CountDeclMethodPrivate,CountDeclMethodProtected,CountDeclMethodPublic,CountInput,CountLine,CountLineBlank,CountLineCode,CountLineCodeDecl,CountLineCodeExe,CountLineComment,CountLineInactive,CountLinePreprocessor,CountOutput,CountSemicolon,CountStmt,CountStmtDecl,CountStmtEmpty,CountStmtExe,Cyclomatic,CyclomaticModified,CyclomaticStrict,CyclomaticStrictModified,Essential,MaxCyclomatic,MaxCyclomaticModified,MaxCyclomaticStrict,MaxCyclomaticStrictModified,MaxEssential,MaxInheritanceTree,MaxNesting,PercentLackOfCohesion,PercentLackOfCohesionModified,RatioCommentToCode,SumCyclomatic,SumCyclomaticModified,SumCyclomaticStrict,SumCyclomaticStrictModified,SumEssential
File,"ACLConfigurationParser.java",11,0,11,0,3,3,3,3,2,0.00,0.00,0,0,,,,,1,0,3,10,,,,10,10,2,,,,10,,,0,,3,0,7,,167,22,125,38,70,20,,,,57,89,37,,58,,,,,,11,11,13,13,9,,3,,,0.16,29,29,32,32,22
File,"AMReporter.java",12,0,11,1,2,2,2,2,1,0.00,0.00,0,0,,,,,9,0,1,37,,,,37,37,31,,,,37,,,10,,2,4,21,,582,70,458,167,240,54,,,,218,303,149,,182,,,,,,7,7,9,9,3,,4,,,0.12,72,72,75,75,39
```
Les fichiers sont ensuite légèrement reformattés dans le répertoire `UND_hive_processed_data` pour inclure seulement les fichiers et ajouter une colonne 'bug' initialisé à `0` pour chacune des entrées à l'aide de `Hive_UND_data_filtering.py`.

Finalement, un dernier programme python `Hive_bug_Identification.py` est utilisé pour retrouver chacun des fichier modifiés dans `modified_cpp-java_files.csv` pour chacune des versions du logiciel et ajusté à `1`.















