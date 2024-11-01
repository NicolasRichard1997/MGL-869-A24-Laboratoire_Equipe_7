import pandas as pd
import glob
import re

def extract_version(filename):
    """Extract version number from filename."""
    match = re.search(r'hive-(\d+\.\d+\.\d+)\.csv', filename)
    return match.group(1) if match else None

def concatenate_hive_files():
    # Get list of all hive CSV files
    files = glob.glob('hive-*.csv')
    
    # Initialize an empty list to store all dataframes
    dfs = []
    
    # Process first file to get headers
    first_df = pd.read_csv(files[0])
    headers = list(first_df.columns)
    
    # Insert 'Version' column after 'Issue Type'
    new_headers = headers[:1] + ['Version'] + headers[1:]
    
    # Process each file
    for file in files:
        # Read the CSV file
        df = pd.read_csv(file)
        
        # Extract version from filename
        version = extract_version(file)
        
        if version:
            # Insert version column after 'Issue Type'
            df.insert(1, 'Version', version)
            
            # Append to list of dataframes
            dfs.append(df)
        else:
            print(f"Warning: Could not extract version from {file}")
    
    # Concatenate all dataframes
    final_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure columns are in the correct order
    final_df = final_df[new_headers]
    
    # Save to new file
    final_df.to_csv('Hive_bug_list.csv', index=False)
    
    print(f"Successfully concatenated {len(files)} files into Hive_bug_list.csv")
    print(f"Total number of rows: {len(final_df)}")

if __name__ == "__main__":
    try:
        concatenate_hive_files()
    except Exception as e:
        print(f"Error: {str(e)}")
