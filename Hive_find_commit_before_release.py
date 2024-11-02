import subprocess

# Dictionnaire contenant les versions Hive avec leurs dates de publication
hive_versions = {
    "hive-2.0.0": "2016-02-15 18:45",
    "hive-2.1.0": "2016-06-21 01:26",
    "hive-2.2.0": "2018-05-04 20:50",
    "hive-2.3.0": "2017-10-04 10:50",
    "hive-3.0.0": "2018-05-22 18:49",
    "hive-3.1.0": "2018-07-30 18:40",
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

print("Derniers commits pour chaque version enregistrés dans 'Hive_last_commits_per_version.txt'")

