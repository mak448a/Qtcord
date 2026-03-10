import os
import platformdirs
import keyring  # NEW: Import keyring for secure token storage
from PySide6.QtWidgets import QMainWindow
from ui import login_ui
from discord_integration import login, load_token

class LoginUI(QMainWindow, login_ui.Ui_MainWindow):
    def __init__(self, switcher):
        super().__init__()

        self.ui = login_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.info_frame.hide()

        self.ui.pushButton.clicked.connect(self.switch)
        self.switcher = switcher

        self.ui.password.returnPressed.connect(self.switch)
        self.ui.email.returnPressed.connect(self.switch)
        self.ui.totp.returnPressed.connect(self.switch)

    def switch(self):
        # Grab email, password, and totp code from the UI fields
        email = self.ui.email.text()
        password = self.ui.password.text()
        totp = self.ui.totp.text()

        # Check on our end before validating with Discord
        valid = email and password

        if valid:
            # Reset UI elements
            self.ui.email.setText("")
            self.ui.password.setText("")
            self.ui.info_frame.hide()

            # Get the token from the Discord API using our credentials.
            if totp:
                _token = login(email, password, totp_code=totp)
            else:
                _token = login(email, password)

            if _token:
                # 1. SECURITY UPDATE: Save token to Keyring
                # This stores the token in the OS secure vault, encrypted.
                keyring.set_password("Qtcord", "discord_token", _token)

                # 2. DELETE INSECURE FILE:
                # We no longer save to 'discordauth.txt'. Instead, we delete it 
                # if it exists to make sure the token isn't lying around in plaintext.
                auth_path = os.path.join(platformdirs.user_config_dir("Qtcord"), "discordauth.txt")
                if os.path.exists(auth_path):
                    try:
                        os.remove(auth_path)
                    except Exception as e:
                        print(f"Note: Could not remove legacy file: {e}")

                # Load the token into the app's memory from the keyring
                load_token()

                # Switch the page to the chat page
                self.switcher.setCurrentIndex(self.switcher.currentIndex() + 1)
            else:
                self.ui.info_frame.show()
        else:
            self.ui.info_frame.show()
