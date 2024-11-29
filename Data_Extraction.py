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
# to fetch the bugs from a specific report. Bug reports for major and minor versions, as well as patches, can be downloaded.All of the bugs reports are kept in the `Jira_bug_data` folder, present in this repository.

# ## 2. Removing Redundant Bugs & Concatenating the Data 
# Since a given bug may affect more than a single version of the software, some redundancy is present in the downloaded data. Although, we might not want to remove duplicates as we will find the affected files for a specific bug in multiple versions of the project. So, we will use pandas data frames to load all of the data from the bugs in the files before concatenating the bugs in a single file with their specific version number.

# In[1]:


import pandas as pd
import os
import re
from pathlib import Path


# In order to simplify repertory changes, we'll initialize two variables, containning the paths of this current repository and the path of your clone of the Apache Hive repertory

# In[2]:


project_repo = "/home/nicolas-richard/Desktop/.Apache_Hive_Bug_Prediction_ML_Model/"
hive_repo = "/home/nicolas-richard/Desktop/.Apache_Hive/"


# In[3]:


project_repo = Path(project_repo)
data_dir = project_repo.joinpath("Jira_bug_data")

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


# We have gathered 2133 bugs. We will run a simple check to remove duplicate lines

# In[4]:


combined_bug_dfs = concatenated_bug_dfs.drop_duplicates()

combined_bug_dfs.info()

combined_bug_dfs.to_csv("Hive_Jira_Bug_Data.csv", index=False)


# Despite the above lines, some duplicate bug keys will remain, which is intentional. Those bugs affected more than a single version of the software. The below line of code outputs bugs affecting multiple versions

# In[5]:


print(concatenated_bug_dfs['Issue key'].value_counts())


# ## 2. Identified Affected Java and C++ Files
# 
# The goal here will be, for every single bug ID collected above, to identify the java and C++ in a given version of the software. Make sure you have a cloned repo of the Apache Hive project on you computer and the path at hand.

# In[6]:


import os
import csv
import subprocess


# In[ ]:


os.chdir(hive_repo)
subprocess.run(['git', 'checkout', "master"], check=True)
subprocess.run(['git', 'pull'], check=True)

bug_file_map = {}

with open(project_repo.joinpath("Hive_Jira_Bug_Data.csv"), 'r') as f:
    for line in f:
        bug_id, version = line.strip().split(',')
        bug_file_map[bug_id] = {'version': version, 'files': []}

for bug_id in bug_file_map:
    version = bug_file_map[bug_id]['version']
    print(f"Searching for bug ID: {bug_id} (Version: {version})")

    try:
        result = subprocess.run(
            ["git", "log", "--grep=" + bug_id, "--name-only", "--pretty=format:"],
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


# In[ ]:


os.chdir(project_repo)
output_file = 'Hive_Modified_Files.csv'

try:
    with open(output_file, 'w+', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for bug_id, data in bug_file_map.items():
            bug_id_str = str(bug_id)
            version_str = str(data['version'])
            files_str = ";".join(data['files'])
            writer.writerow([bug_id_str, version_str, files_str])
        print(f"Output has been written to {output_file}")
except Exception as e:
    print(f"An error occurred: {e}")


# ## 3. Gather Independant Variables for Each File in Each Version of Hive
# 
# We will now use  *SciTools Understand* to collect a plethora of independent variables that will eventually help us predict bugs. First though, we need to retrieve the very last commit before the release of each version of the software.

# From the [Apache Hive tags](https://github.com/apache/hive/tags), we can fetch manually the commit for each of the software version 

# In[ ]:


hive_versions = {
    "2.0.0": "7f9f1fcb8697fb33f0edc2c391930a3728d247d7",
    "2.0.1": "e3cfeebcefe9a19c5055afdcbb00646908340694",
    "2.1.0": "9265bc24d75ac945bde9ce1a0999fddd8f2aae29",
    "2.1.1": "1af77bbf8356e86cabbed92cfa8cc2e1470a1d5c",
    "2.2.0": "da840b0f8fa99cab9f004810cd22abc207493cae",
    "2.3.0": "6f4c35c9e904d226451c465effdc5bfd31d395a0",
    "2.3.1": "7590572d9265e15286628013268b2ce785c6aa08",
    "2.3.2": "857a9fd8ad725a53bd95c1b2d6612f9b1155f44d",
    "2.3.3": "3f7dde31aed44b5440563d3f9d8a8887beccf0be",
    "2.3.4": "56acdd2120b9ce6790185c679223b8b5e884aaf2",
    "2.3.5": "76595628ae13b95162e77bba365fe4d2c60b3f29",
    "2.3.6": "2c2fdd524e8783f6e1f3ef15281cc2d5ed08728f",
    "2.3.7": "cb213d88304034393d68cc31a95be24f5aac62b6",
    "2.3.8": "f1e87137034e4ecbe39a859d4ef44319800016d7",
    "2.3.9": "92dd0159f440ca7863be3232f3a683a510a62b9d",
    "2.3.10": "5160d3af392248255f68e41e1e0557eae4d95273",
    "3.0.0": "ce61711a5fa54ab34fc74d86d521ecaeea6b072a",
    "3.1.0": "bcc7df95824831a8d2f1524e4048dfc23ab98c19",
    "3.1.1": "f4e0529634b6231a0072295da48af466cf2f10b7",
    "3.1.2": "8190d2be7b7165effa62bd21b7d60ef81fb0e4af",
    "3.1.3": "4df4d75bf1e16fe0af75aad0b4179c34c07fc975",
    "4.0.0": "183f8cb41d3dbed961ffd27999876468ff06690c",
    "4.0.1": "3af4517eb8cfd9407ad34ed78a0b48b57dfaa264"
}


# These different release dates will allow us to associate a commit to specific a version of Hive 

# In[ ]:


output_file = project_repo.joinpath("Hive_Last_Commits.csv")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["Version", "Commit Hash"])

    for version, commit in hive_versions.items():
        writer.writerow([version, commit])

print("Derniers commits pour chaque version enregistrés dans 'Hive_Last_Commits.csv'")


# Finally, we can collect UND data 

# In[ ]:


version_file = project_repo.joinpath("Hive_Last_Commits.csv")
und_base = project_repo.joinpath("UND_projects")
settings_file_path = project_repo.joinpath("settings.xml")
hive_data = project_repo.joinpath('UND_hive_data')


os.chdir(project_repo)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}")

run_command(f'mkdir -p -m 777 {und_base}')
run_command(f' mkdir -p -m 777 {hive_data}')

os.chdir(hive_repo)

def process_versions():
    with open(version_file, "r") as file:
        next(file)
        for line in file:
            if line.strip():
                version, commit_id = line.split(",")[0].strip(), line.split(",")[1].strip()              

                run_command(f"cd {hive_repo} && git checkout {commit_id}")
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
                run_command(f"und settings -metricsOutputFile {hive_data.joinpath(f'UND_{version}.csv')} {und_project_path}")

                run_command(f"und add {hive_repo} {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile {hive_data.joinpath(f'UND_{version}.csv')} {und_project_path}")

                run_command(f"und analyze {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile {hive_data.joinpath(f'UND_{version}.csv')} {und_project_path}")

                run_command(f"und metrics {und_project_path}")
                
if __name__ == "__main__":
    process_versions()


# In[ ]:





# In[ ]:




