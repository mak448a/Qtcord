import os
import sys
import subprocess

try:
    import PyInstaller

    print("PyInstaller is good to go!")
except ModuleNotFoundError:
    raise Exception(
        "You need pyinstaller installed. Make sure to install a version at least 2 months old as to avoid false positives on virus detectors. Use pip install pyinstaller."
    )

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_dir}")

# Find the correct paths
project_root = os.path.dirname(os.path.dirname(script_dir))
src_path = os.path.join(project_root, "src")
spec_path = os.path.join(script_dir, "win.spec")

print(f"Project root: {project_root}")
print(f"Src path: {src_path}")
print(f"Spec file path: {spec_path}")

# Verify paths exist
if not os.path.exists(src_path):
    print(f"Error: src directory not found at {src_path}")
    sys.exit(1)

if not os.path.exists(spec_path):
    print(f"Error: spec file not found at {spec_path}")
    sys.exit(1)

# Change to the src directory
try:
    os.chdir(src_path)
    print(f"Changed working directory to: {src_path}")
except Exception as e:
    print(f"Error changing directory: {e}")
    sys.exit(1)

# Use subprocess instead of os.system for better error handling
try:
    result = subprocess.run(
        ["pyinstaller", spec_path], capture_output=True, text=True, check=True
    )
    print("PyInstaller command executed successfully")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"PyInstaller command failed with error: {e}")
    print(f"Standard output: {e.stdout}")
    print(f"Standard error: {e.stderr}")
    sys.exit(1)
