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
src_path = os.path.join(script_dir, "src")
spec_path = os.path.join(script_dir, "helper_scripts", "win.spec")

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
