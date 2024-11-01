import pandas as pd

# Load the combined CSV
df = pd.read_csv('Hive_bug_list.csv')

# Create a dictionary to store bug ID and version mapping
bug_version_map = {}

# Iterate through the dataframe to create the mapping
for index, row in df.iterrows():
    bug_id = row['Issue key']
    version = row['Version']
    # If a bug ID appears multiple times, keep the latest version
    bug_version_map[bug_id] = version

# Sort the bug IDs to ensure consistent output
sorted_bug_ids = sorted(bug_version_map.keys())

# Save the bug IDs and versions to a new file
with open('bug_ids_with_versions.txt', 'w') as f:
    for bug_id in sorted_bug_ids:
        version = bug_version_map[bug_id]
        # Write both bug ID and version, separated by a tab
        f.write(f"{bug_id},{version}\n")

# Print summary statistics
print(f"Total unique bugs processed: {len(sorted_bug_ids)}")
print("Output saved to 'bug_ids_with_versions.txt'")
