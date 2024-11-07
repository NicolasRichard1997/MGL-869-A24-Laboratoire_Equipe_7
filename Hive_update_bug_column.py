import pandas as pd 
import os

# Chemin vers le dossier contenant les fichiers de version traités
data_folder = "UND_hive_processed_data"
modified_files_path = "modified_java_cpp_files.csv"

# Ouvrir le fichier modified_java_cpp_files.csv et le lire ligne par ligne
with open(modified_files_path, 'r') as modified_files:
    for line in modified_files:
        # Extraire l'ID du bogue, la version et les fichiers associés
        parts = line.strip().split(',')
        if len(parts) < 3:
            print(f"Ligne incorrecte ou incomplète: {line}")
            continue

        bug_id = parts[0]  # ID du bogue (non utilisé dans ce script, mais on le conserve)
        version = parts[1]
        # Extraire uniquement le nom de fichier et l'extension
        files_with_bugs = [os.path.basename(file_path) for file_path in parts[2:]]  # Liste de noms de fichiers avec extension

        # Construire le chemin du fichier pour la version spécifique
        processed_file_path = os.path.join(data_folder, f"UND_hive-{version}_processed.csv")

        # Charger le fichier CSV de la version
        if os.path.exists(processed_file_path):
            processed_df = pd.read_csv(processed_file_path)

            # Vérifier si le fichier CSV a les colonnes nécessaires
            if 'FileName' in processed_df.columns and 'Bug' in processed_df.columns:
                # Mettre à jour la colonne Bug pour chaque fichier contenant un bogue
                for file_with_bug in files_with_bugs:
                    # Mise à jour de la colonne 'Bug' pour le fichier correspondant
                    processed_df.loc[processed_df['FileName'] == file_with_bug, 'Bug'] = 1
                    print(f"Mise à jour de la colonne 'Bug' pour le fichier {file_with_bug} dans {processed_file_path}")
                
                # Sauvegarder les changements dans le fichier CSV
                processed_df.to_csv(processed_file_path, index=False)
            else:
                print(f"Le fichier {processed_file_path} ne contient pas les colonnes attendues 'FileName' et 'Bug'.")
        else:
            print(f"Le fichier pour la version {version} n'existe pas dans le dossier {data_folder}.")
