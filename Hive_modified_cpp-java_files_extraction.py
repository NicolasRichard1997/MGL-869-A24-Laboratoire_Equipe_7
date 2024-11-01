import subprocess

# Load bug IDs from the text file
with open('bug_ids.txt', 'r') as f:
    bug_ids = f.read().splitlines()

# Dictionary to hold bug ID and associated modified files
bug_file_map = {}

# Check each bug ID in the Git log
for bug_id in bug_ids:
    print(f"Searching for bug ID: {bug_id}")
    try:
        # Run git log command
        result = subprocess.run(
            ["git", "log", "--grep=" + bug_id, "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            check=True
        )
        # Get all files and filter for only .cpp and .java files
        all_files = result.stdout.splitlines()
        filtered_files = [file for file in all_files if file.endswith(('.cpp', '.java'))]
        
        # Only add to dictionary if there are matching files
        if filtered_files:
            bug_file_map[bug_id] = filtered_files
    except subprocess.CalledProcessError as e:
        print(f"Error searching for {bug_id}: {e}")

# Save modified files associated with bug IDs to a text file
with open('modified_java_cpp_files.txt', 'w') as f:
    for bug_id, files in bug_file_map.items():
        f.write(f"{bug_id},")
        for file in files:
            f.write(f"{file},")
        f.write("\n")

