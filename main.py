import sys
import os
from PySide6.QtWidgets import QApplication
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
from views.login_view import LoginDialog
from views.main_view import MainView


def main():
    app = QApplication(sys.argv)

    # הצגת חלון ההתחברות
    login_dialog = LoginDialog()
    if login_dialog.exec() == LoginDialog.Accepted:
        username = login_dialog.get_username()  # קבלת שם המשתמש
        
        window = MainView(username)  # העברת שם המשתמש לחלון הראשי
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
