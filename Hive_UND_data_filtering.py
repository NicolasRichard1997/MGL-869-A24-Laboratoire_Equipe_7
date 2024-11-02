import pandas as pd
import glob

# Function to process each CSV file
def process_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Filter for rows where Kind is "File"
    df = df[df['Kind'] == 'File']
    
    # Replace the first column (Kind) with "Bug" and set all values to 0
    df = df.drop(columns=['Kind'])  # Drop the 'Kind' column
    df.insert(0, 'Bug', 0)  # Insert 'Bug' column at the beginning with value 0 for all rows
    
    # Rename 'Name' to 'FileName'
    df = df.rename(columns={'Name': 'FileName'})
    
    # Reorder columns: Bug, FileName, AvgCyclomatic, and then the rest
    columns_order = ['Bug', 'FileName', 'AvgCyclomatic'] + [col for col in df.columns if col not in ['Bug', 'FileName', 'AvgCyclomatic']]
    df = df[columns_order]
    
    return df

# Path to the directory containing CSV files
input_files = glob.glob('/home/nicolas-richard/Desktop/UND_hive_data/*.csv')
output_files = []

# Process each CSV and save the result
for file_path in input_files:
    processed_df = process_csv(file_path)
    
    # Save the processed file
    output_file = file_path.replace('.csv', '_processed.csv')
    processed_df.to_csv(output_file, index=False)
    output_files.append(output_file)

print("Processing complete. Files saved:", output_files)
