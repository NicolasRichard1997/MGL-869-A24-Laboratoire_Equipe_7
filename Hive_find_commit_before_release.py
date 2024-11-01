import subprocess

# Dictionnaire contenant les versions Hive avec leurs dates de publication
hive_versions = {
    "hive-2.0.0": "2016-02-15 18:45",
  #  "hive-2.0.1": "2016-05-24 17:20",
    "hive-2.1.0": "2016-06-21 01:26",
   # "hive-2.1.1": "2018-05-04 20:50",
    "hive-2.2.0": "2018-05-04 20:50",
    "hive-2.3.0": "2017-10-04 10:50",
 #   "hive-2.3.1": "2017-11-06 17:57",
  #  "hive-2.3.10": "2024-05-09 15:41",
  #  "hive-2.3.2": "2018-03-27 23:05",
  #  "hive-2.3.3": "2018-05-04 20:48",
  #  "hive-2.3.4": "2018-11-06 06:50",
   # "hive-2.3.5": "2019-05-14 19:32",
  #  "hive-2.3.6": "2019-08-22 18:53",
  #  "hive-2.3.7": "2020-07-03 04:34",
  #  "hive-2.3.8": "2021-01-15 21:12",
  #  "hive-2.3.9": "2022-06-17 12:34",
    "hive-3.0.0": "2018-05-22 18:49",
    "hive-3.1.0": "2018-07-30 18:40",
  # "hive-3.1.1": "2018-10-31 19:07",
  #  "hive-3.1.2": "2022-06-17 12:34",
  #  "hive-3.1.3": "2022-06-17 12:34",
    "hive-4.0.0": "2024-03-29 10:42",
    "hive-4.0.1": "2024-10-02 06:35"
}

# Dictionnaire pour stocker le dernier commit pour chaque version
last_commits = {}

# Boucle sur chaque version pour identifier le dernier commit avant la date de version
for version, date in hive_versions.items():
    try:
        # Exécute la commande git log pour obtenir le dernier commit avant la date de la version
        result = subprocess.run(
            ["git", "log", "--before", date, "--pretty=format:%H %cd", "--date=iso"],
            capture_output=True, text=True, check=True
        )
        
        # Récupère le premier commit retourné, s'il y en a un
        last_commit = result.stdout.splitlines()[0] if result.stdout else "No commit found"
        last_commits[version] = last_commit

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la récupération du commit pour la version {version}: {e}")
        last_commits[version] = "Error retrieving commit"

# Enregistre les résultats dans un fichier
with open("Hive_last_commit_before_release.txt", "w") as file:
    for version, commit in last_commits.items():
        file.write(f"{version}: {commit}\n")

print("Derniers commits pour chaque version enregistrés dans 'last_commits_per_version.txt'")

