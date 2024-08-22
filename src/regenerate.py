import os

current_dir = os.path.dirname(os.path.realpath(__file__)).replace(" ", "\\ ")  # NOQA (basically tells pycharm to shut up)
os.system(f"pyside6-uic {current_dir}/ui/main.ui -o {current_dir}/ui/main_ui.py")
os.system(f"pyside6-uic {current_dir}/ui/login.ui -o {current_dir}/ui/login_ui.py")
os.system(
    f"pyside6-uic {current_dir}/ui/licenses.ui -o {current_dir}/ui/licenses_ui.py"
)
os.system(
    f"pyside6-uic {current_dir}/ui/no_internet.ui -o {current_dir}/ui/no_internet.py"
)
