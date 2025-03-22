# register_presenter.py
class RegisterPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def perform_registration(self, username, email, password):
        """Register a new user using the model's registration method"""
        print(f"RegisterPresenter: Registering user: {username}, email: {email}")
        
        # Call model's registration method
        result = self.model.register(username, password, email)
        
        if result:
            print(f"RegisterPresenter: Registration successful for {username}")
        else:
            print(f"RegisterPresenter: Registration failed for {username}")
            
        return result