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

# Print out the contents of the script directory
print("Contents of script directory:")
print(os.listdir(script_dir))

# Attempt to locate the src directory
possible_src_paths = [
    os.path.join(script_dir, "src"),
    os.path.join(os.path.dirname(script_dir), "src"),
    os.path.join(script_dir, "..", "src"),
    os.path.join(script_dir, "Qtcord", "src"),
]

src_path = None
for path in possible_src_paths:
    abs_path = os.path.abspath(path)
    print(f"Checking path: {abs_path}")
    if os.path.exists(abs_path) and os.path.isdir(abs_path):
        src_path = abs_path
        break

if not src_path:
    print("Could not find src directory")
    sys.exit(1)

print(f"Found src directory: {src_path}")

# Find the spec file
spec_path = os.path.join(script_dir, "helper_scripts", "win.spec")
print(f"Spec file path: {spec_path}")

if not os.path.exists(spec_path):
    print("Spec file not found")
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
