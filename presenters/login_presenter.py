# login_presenter.py
from models.mock_stock_model import MockStockModel

class LoginPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def perform_login(self, username, password):
        print(f"LoginPresenter.perform_login() called with username={username}, password={password}")
        result = self.model.login(username, password)
        if result:
            print(f"LoginPresenter: Setting username in model to: {username}")
            self.model.set_username(username)
            print("LoginPresenter: Login successful")
        else:
            print("LoginPresenter: Login failed")
        return result
