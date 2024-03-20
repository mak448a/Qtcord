import os
import shutil


try:
    import PyInstaller
    if PyInstaller:
        print("PyInstaller is good to go!")
except ModuleNotFoundError:
    raise Exception("You need pyinstaller installed. Make sure to install a version at least 2 months old as to avoid false positives on virus detectors. Use pip install pyinstaller.")


os.system("pyinstaller main.spec")

# choice = input("Delete build cache? (N/y) ").strip().lower()

# if choice == "yes" or choice == "y":
#     shutil.rmtree("build")
# else:
#     quit()
