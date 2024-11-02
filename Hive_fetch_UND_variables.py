import subprocess
import os

# Paths to your files and repository
version_file_path = "~/Desktop/.MGL_869_Laboratoire/Hive_last_commit_before_release.txt"
repo_path = "~/Desktop/Apache_Hive"
und_project_base_path = "~/Desktop"

def run_command(command):
    """Utility function to execute a shell command."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.cmd}")

def process_versions():
    # Expand ~ to the full home directory path
    version_file = version_file_path.replace("~", "/home/nicolas-richard")
    repo = repo_path.replace("~", "/home/nicolas-richard")
    und_base = und_project_base_path.replace("~", "/home/nicolas-richard")

    # Read the versions and commit IDs from the file
    with open(version_file, "r") as file:
        for line in file:
            if line.strip():
                # Parse the version and commit ID from each line
                version, commit_id = line.split(":")[0].strip(), line.split()[1].strip()
                #print(version, commit_id)

                # Git checkout the specific commit
                run_command(f"cd {repo} && git checkout {commit_id}")
                # print(f"Successfully checked out {commit_id} before {version}")

                # Create project paths for Understand commands
                und_project_path = f"{und_base}/UND_{version}.und"

                # Create the Understand project directory if it does not exist
                os.makedirs(und_project_path, exist_ok=True)

                # Check if settings.xml exists and handle accordingly
                settings_file_path = "/home/nicolas-richard/Desktop/settings.xml"
                destination_settings_file = f"{und_project_path}/settings.xml"

                # Option to overwrite the settings file if it exists
                if os.path.exists(destination_settings_file):
                    print(f"Removing existing settings.xml at {destination_settings_file}")
                    os.remove(destination_settings_file)

                # Copy the settings.xml file
                run_command(f"cp {settings_file_path} {und_project_path}")

                # Run the Understand commands
                run_command(f"und create -languages java C++ {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile ~/Desktop/UND_{version}.csv {und_project_path}")
                run_command(f"und add {repo} {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile ~/Desktop/UND_{version}.csv {und_project_path}")
                run_command(f"und analyze {und_project_path}")
                run_command(f"cp {settings_file_path} {destination_settings_file}")
                run_command(f"und settings -metricsOutputFile ~/Desktop/UND_{version}.csv {und_project_path}")
                run_command(f"und metrics {und_project_path}")
                
if __name__ == "__main__":
    process_versions()
