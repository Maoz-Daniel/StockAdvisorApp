import sys
import os
from PySide6.QtWidgets import QApplication
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
from views.login_view import LoginDialog
from views.main_view import MainView
from views.login_view import LoginDialog
from views.main_view import MainView
from models.mock_stock_model import MockStockModel
from presenters.login_presenter import LoginPresenter

def main():
    app = QApplication(sys.argv)
    model = MockStockModel()


    # הצגת חלון ההתחברות
    login_dialog = LoginDialog()
    login_presenter = LoginPresenter(login_dialog, model)
    login_dialog.set_presenter(login_presenter)


    if login_dialog.exec() == LoginDialog.Accepted:
        username = login_dialog.get_username()  # קבלת שם המשתמש
        print(f"main.py: Updated model username to: {model.get_username()}")

        
        window = MainView(username,model)  # העברת שם המשתמש לחלון הראשי
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
