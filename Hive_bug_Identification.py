import csv
import pandas as pd
import os

# Read the CSV file
input_file = 'modified_java_cpp_files.csv'  # Replace with your actual file path

# Initialize lists to store processed data
bug_ids = []
versions = []
file_names = []

# Open the input CSV and parse it
with open(input_file, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        bug_id = row[0]
        version = row[1]

        # Check if there are any affected files listed
        affected_files = row[2:] if len(row) > 2 else ["None"]

        # For each affected file, add an entry in the lists
        for file_path in affected_files:
            # Extract just the file name from the path
            file_name = os.path.basename(file_path).strip()
            bug_ids.append(bug_id)
            versions.append(version)
            file_names.append(file_name)

# Create a DataFrame to store the data in a structured format
output_df = pd.DataFrame({
    'Bug ID': bug_ids,
    'Version': versions,
    'File': file_names
})

# Display the output to verify
print(output_df)

# Initialize lists to store processed data
unfound_bug_ids = []
unfound_versions = []
unfound_file_names = []

for index, row in output_df.iterrows():
    filename = f"UND_hive_processed_data/UND_hive-{row['Version']}_processed.csv"
    target_file = row['File']  # The file name we are searching for in the second column

    try:
        # Read the CSV file into a list of rows
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Initialize a flag to indicate if we found a match
        found = False

        # Process each row and look for matches
        for i, columns in enumerate(rows):
            # Ensure there are at least two columns
            if len(columns) > 1:
                # Trim whitespace from the file name for accurate comparison
                file_name_in_row = columns[1].strip()
                if file_name_in_row == target_file:
                    # Match found, update the first column
                    columns[0] = '1'
                    rows[i] = columns  # Update the row
                    found = True
                    break  # Stop searching once we find the match

        # If no match was found, record the unfound entry
        if not found:
            unfound_bug_ids.append(row['Bug ID'])
            unfound_versions.append(row['Version'])
            unfound_file_names.append(row['File'])
        else:
            # Write the modified rows back to the CSV file
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    except FileNotFoundError:
        print(f"File {filename} not found.")

percentageBug_files_found = 100 - ((len(unfound_bug_ids)/(len(bug_ids))) * 100)

print(f"Percentage of files found: {percentageBug_files_found}%")
