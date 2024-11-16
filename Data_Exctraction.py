#!/usr/bin/env python
# coding: utf-8

# # Data Extraction
# 
# This notebook contains all the steps necessary to fetch all bugs from the Apache Hive Jira online repository (available at [this address](https://issues.apache.org/jira/projects/HIVE/issues/HIVE-25351?filter=allopenissues)). We will begin by downloading the data to this repository before filtering it. 

# ## 1. Fetching Bug Reports from Jira
# 
# The first steps is to download and copy all the bug reports from *Hive 2.0.0* and subsequent versions. [On this page](https://issues.apache.org/jira/projects/HIVE/issues/HIVE-25351?filter=allopenissues), we can select `Advanced Search` and copy the following command :
# ```sql
# project = HIVE AND issuetype = Bug AND status in (Resolved, Closed) AND affectedVersion = X.Y.Z
# ```
# to fetch the bugs from a specific report. Bug reports for major and minor versions, as well as patches, can be downloaded.All of the bugs reports are kept in the `Jira_Bug_Data` folder, present in this repository.

# ## 2. Removing Redundant Bugs & Concatenating the Data 
# Since a given bug may affect more than a single version of the software, some redundancy is present in the downloaded data. Although, we might not want to remove duplicates as we will find the affected files for a specific bug in multiple versions of the project. So, we will use pandas data frames to load all of the data from the bugs in the files before concatenating the bugs in a single file with their specific version number.

# In[1]:


import pandas as pd
import re
from pathlib import Path


# In[2]:


data_dir = Path("Jira_Bug_Data")

version_pattern = re.compile(r'_(\d+\.\d+\.\d+)_')

bug_dfs = []

for file_path in data_dir.glob("*.csv"):
    
    df = pd.read_csv(file_path)

    filename = file_path.name  # e.g., 'Hive_3.3.0_Jira_Bug_Data.csv'

    match = version_pattern.search(filename)
    version = match.group(1) if match else 'Unknown'
    
    df['Version'] = version

    df = df[['Issue key', 'Version']]
   
    bug_dfs.append(df)

concatenated_bug_dfs = pd.concat(bug_dfs, ignore_index=True)

concatenated_bug_dfs.info()


# Here we want to remove duplicate lines

# In[3]:


combined_bug_dfs = concatenated_bug_dfs.drop_duplicates()

combined_bug_dfs.info()

combined_bug_dfs.to_csv("Hive_Jira_Bug_Data.csv", index=False)


# Despite the above lines, some duplicate bug keys will remain, which is intentional. Those bugs affected more than a single version of the software. The below line of code outputs bugs affecting multiple versions

# In[4]:


print(concatenated_bug_dfs['Issue key'].value_counts())


# ## 2. Identified Affected Java and C++ Files
# 
# The goal here will be, for every single bug ID coledcted above, to identify the java and C++ in a given version of the software. Make sure you have a cloned repo of the Apache Hive project on you computer and the path at hand.

# In[5]:


import subprocess
import csv
import os


# In[6]:


repo_path = os.path.expanduser('~/Desktop/.Apache_Hive')  # Adjust the path to your local clone of Apache Hive
os.chdir(repo_path)

bug_file_map = {}

current_path = os.path.expanduser('~/Desktop/.Apache_Hive_Bug_Prediction_ML_Model')

bug_data_path = current_path + '/Hive_Jira_Bug_Data.csv'

with open(bug_data_path, 'r') as f:
    for line_number, line in enumerate(f, start=1):
        parts = line.strip().split(',')
        if len(parts) != 2:
            print(f"Skipping malformed line {line_number}: {line.strip()}")
            continue
        bug_id, version = parts
        bug_file_map[bug_id] = {'version': version, 'files': []}

for bug_id in bug_file_map:
    version = bug_file_map[bug_id]['version']
    print(f"Searching for bug ID: {bug_id} (Version: {version})")

    try:
        result = subprocess.run(
            ["git", "log", "--grep", bug_id, "--name-only", "--pretty=format:"],
            capture_output=True,
            text=True,
            check=True
        )

        all_files = result.stdout.splitlines()
        filtered_files = [file for file in all_files if file.endswith(('.cpp', '.java'))]

        if filtered_files:
            bug_file_map[bug_id]['files'].extend(filtered_files)

    except subprocess.CalledProcessError as e:
        print(f"Error searching for {bug_id}: {e}")


# In[7]:


output_csv =  current_path + "/Hive_Affected_Files.csv"

try:
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Bug_ID', 'Version', 'Affected_File(s)'])
        for bug_id, data in bug_file_map.items():

            if (
                isinstance(data, dict) and
                data.get('version') and
                data.get('files')
            ):
                files_str = ";".join(data['files']) if data['files'] else ""
                writer.writerow([bug_id, data['version'], files_str])
            
    print(f"Results have been saved to {output_csv}")
except Exception as e:
    print(f"Error writing to csv file {output_csv}: {e}")


# ## 3. Gather Independant Variables for Each File in Each Version of Hive
# 
# We will now use  *SciTools Understand* to collect a plethora of independent variables that will eventually help us predict bugs. First though, we need to retrieve the very last commit before the release of each version of the software.

# From the [Apache Hive archives](https://archive.apache.org/dist/hive/), we can fetch the release date for each of the software version 

# In[8]:


hive_versions = {
    "hive-2.0.0": "2016-02-15 18:45",
    "hive-2.0.1": "2016-05-24 17:20",
    "hive-2.1.0": "2016-06-21 01:26",
    "hive-2.1.1": "2018-05-04 20:50",
    "hive-2.2.0": "2018-05-04 20:50",
    "hive-2.3.0": "2017-10-04 10:50",
    "hive-2.3.1": "2017-11-06 17:57",
    "hive-2.3.2": "2018-03-27 23:05",
    "hive-2.3.3": "2018-05-04 20:48",
    "hive-2.3.4": "2018-11-06 06:50",
    "hive-2.3.5": "2019-05-14 19:32",
    "hive-2.3.6": "2019-08-22 18:53",
    "hive-2.3.7": "2020-07-03 04:34",
    "hive-2.3.8": "2021-01-15 21:12",
    "hive-2.3.9": "2022-06-17 12:34",
    "hive-2.3.10": "2024-05-09 15:41",
    "hive-3.0.0": "2018-05-22 18:49",
    "hive-3.1.0": "2018-07-30 18:40",
    "hive-3.1.1": "2018-10-31 19:07",
    "hive-3.1.2": "2022-06-17 12:34",
    "hive-3.1.3": "2022-06-17 12:34",
    "hive-4.0.0": "2024-03-29 10:42",
    "hive-4.0.1": "2024-10-02 06:35"
}


# These different release dates will allow us to associate a commit to specific a version of Hive 

# In[9]:


last_commits = {}

for version, date in hive_versions.items():
    try:
        result = subprocess.run(
            ["git", "log", "--before", date, "--pretty=format:%H %cd", "--date=iso"],
            capture_output=True, text=True, check=True
        )
        
        last_commit = result.stdout.splitlines()[0] if result.stdout else "No commit found"
        last_commits[version] = last_commit

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la récupération du commit pour la version {version}: {e}")
        last_commits[version] = "Error retrieving commit"

with open(current_path + "/Hive_last_commit_before_release.txt", "w") as file:
    for version, commit in last_commits.items():
        file.write(f"{version}: {commit}\n")

print("Derniers commits pour chaque version enregistrés dans 'Hive_last_commits_per_version.txt'")


# The following 

# In[ ]:


# Paths to files and repositories. Adapt as needed
project_repo = '/home/nicolas-richard/Desktop/.Apache_Hive_Bug_Prediction_ML_Model'
version_file = project_repo + "/Hive_last_commit_before_release.txt"
repo = "/home/nicolas-richard/Desktop/.Apache_Hive"
und_base = project_repo + "/UND_projects"
settings_file_path = project_repo + "/settings.xml"

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}")

run_command(f'mkdir {und_base}')

def process_versions():
    with open(version_file, "r") as file:
        for line in file:
            if line.strip():
                version, commit_id = line.split(":")[0].strip(), line.split()[1].strip()
                run_command(f"cd {repo} && git checkout {commit_id}")
                print(f"Successfully checked out {commit_id} before {version}")

                und_project_path = f"{und_base}/UND_{version}.und"


                run_command(f"und create -languages java C++ {und_project_path}")

                destination_settings_file = f"{und_project_path}/settings.xml"

                if os.path.exists(destination_settings_file):
                    print(f"Removing existing settings.xml at {destination_settings_file}")
                    os.remove(destination_settings_file)

                run_command(f"cp {settings_file_path} {und_project_path}")

                # Redudancy here is to override SciTools Understand's automatic generation of files
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile {project_repo}/UND_{version}.csv {und_project_path}")

                run_command(f"und add {repo} {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile {project_repo}/UND_{version}.csv {und_project_path}")

                run_command(f"und analyze {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile {project_repo}/UND_{version}.csv {und_project_path}")

                run_command(f"und metrics {und_project_path}")
                
if __name__ == "__main__":
    process_versions()

