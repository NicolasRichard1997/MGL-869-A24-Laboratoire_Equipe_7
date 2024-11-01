import subprocess
import os

# Set the working directory to the Apache_Hive repository
repo_path = os.path.expanduser('~/Desktop/hive')
os.chdir(repo_path)

# Path to the 'bug_ids_with_versions.txt' file
bug_ids_file_path = os.path.expanduser('~/Desktop/.MGL_869_Laboratoire/bug_ids_with_versions.txt')

# Path to save the output CSV file
output_file_path = os.path.expanduser('~/Desktop/.MGL_869_Laboratoire/modified_java_cpp_files.csv')

# Load bug IDs and versions from the text file
bug_file_map = {}

with open(bug_ids_file_path, 'r') as f:
    for line in f:
        # Split each line by the comma to separate bug ID and version
        bug_id, version = line.strip().split(',')
        bug_file_map[bug_id] = {'version': version, 'files': []}

# Check each bug ID in the Git log
for bug_id in bug_file_map:
    version = bug_file_map[bug_id]['version']
    print(f"Searching for bug ID: {bug_id} (Version: {version})")

    try:
        # Run git log command to find modified files for the given bug ID
        result = subprocess.run(
            ["git", "log", "--grep=" + bug_id, "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            check=True
        )

        # Get all files and filter for only .cpp and .java files
        all_files = result.stdout.splitlines()
        filtered_files = [file for file in all_files if file.endswith(('.cpp', '.java'))]

        # Add filtered files to the bug's entry if there are matching files
        if filtered_files:
            bug_file_map[bug_id]['files'].extend(filtered_files)

    except subprocess.CalledProcessError as e:
        print(f"Error searching for {bug_id}: {e}")

# Save modified files associated with bug IDs to a CSV file
with open(output_file_path, 'w') as f:
    for bug_id, data in bug_file_map.items():
        # Write bug ID, version, and associated files
        f.write(f"{bug_id},{data['version']},")
        f.write(",".join(data['files']))
        f.write("\n")

