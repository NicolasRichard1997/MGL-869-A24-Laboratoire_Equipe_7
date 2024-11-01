import pandas as pd

# Load the combined CSV
df = pd.read_csv('combined.csv')

# Extract unique bug IDs (assuming the column name is 'bug_id', adjust as necessary)
bug_ids = df['Issue key'].unique()

# Save the bug IDs to a new file (optional)
with open('bug_ids.txt', 'w') as f:
    for bug_id in bug_ids:
        f.write(f"{bug_id}\n")

