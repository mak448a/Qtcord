import os


try:
    import PyInstaller

    if PyInstaller:
        print("PyInstaller is good to go!")
except ModuleNotFoundError:
    raise Exception(
        "You need pyinstaller installed. Make sure to install a version at least 2 months old as to avoid false positives on virus detectors. Use pip install pyinstaller."
    )

current_dir = os.getcwd()
os.chdir("src")
new_dir = os.getcwd()
print(f"Changed from {current_dir} to {new_dir}")
os.system("pyinstaller ../helper_scripts/win.spec")
