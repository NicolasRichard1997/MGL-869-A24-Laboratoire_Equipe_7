# MGL869-A24_Laboratoire

## Description du projet
Ce projet vise à développer un modèle d'apprentissage machine pour prédire les fichiers les plus susceptibles de contenir des bogues dans le logiciel *Apache Hive*. Cette prédiction permettra une meilleure priorisation des tests, particulièrement crucial lors des phases finales avant une nouvelle release.


## Objectifs
- Développer un modèle de prédiction de bogues
- Identifier les fichiers à risque élevé
- Optimiser l'allocation des ressources de test
- Améliorer la qualité des releases de Hive

## 1. Extraction des données
L'objectif de cette première étape est de collecter les données nécessaires pour le modèle de prédiction, en se concentrant sur les versions 2.0.0 et ultérieures de Hive.

### 1.1 Collection des fichiers qui contiennent un bogue sur Jira

Les bogues sont extraits de Jira tel que suit, pour toutes les versions majeures et mineures (excluant les patchs) à partir de 2.0.0:

```sql
project = HIVE AND issuetype = Bug AND status in (Resolved, Closed) AND affectedVersion = X.Y.0
```

Les bogues sont extraits dans le fichier `Hive_bug_list.csv` contenant les variables suivantes, à l'aide du fichier 'concatenate_bug_list.py':

- Issue Type
- version
- Issue key
- Issue id
- Summary
- Assignee
- Reporter
- Priority
- Status
- Resolution
- Created
- Updated
- Due Date


### 1.2 Identification des fichiers modifiés

À partir du fichier généré à l'étape précédente, les `bug IDs` ont été extraits via l'exécution du fichier `Hive_bug_IDs_extraction.py`

Ce fichier permet l'identification des fichiers `java` et `C++` modifiés lors de la résolution de chacun des bogues par `Hive_modified_cpp-java_files_extraction.py`.

Le résultat est présent dans le fichier `Hive_modified_cpp-java_files.csv` dans le format suivant:

```CSV
<Bug ID 1>, <modified Java/CPP file 1>,  <modified Java/CPP file 2>, [...],
<Bug ID 2>, <modified Java/CPP file 1>,  <modified Java/CPP file 2>, [...],
```

### 1.3 Collection des variables indépendantes avec `Understand`

Dans un premier temps, on extrait le dernier commit avant les 'releases' majeur avec le programme en python suivant:
`Hive_find_commit_before_release.py'. Le résultat est stcoké dans le fichier `Hive_last_commit_before_release.txt`.



