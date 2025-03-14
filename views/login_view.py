# login_view.py
from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QCheckBox, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from presenters import login_presenter
from models import mock_stock_model

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart Finance - Secure Login")
        self.setFixedSize(450, 550)
        self.username = ""
        
        # Set window flags
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Apply stylesheets
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                font-family: 'Segoe UI', 'Open Sans', sans-serif;
            }
            QLabel {
                color: #2C3E50;
                font-family: 'Segoe UI', 'Open Sans', sans-serif;
            }
            QLabel#logo-text {
                color: #1E3A8A;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QLabel#title {
                color: #1E3A8A;
                font-size: 24px;
                font-weight: bold;
                margin-top: 10px;
            }
            QLabel#subtitle {
                color: #64748B;
                font-size: 15px;
                margin-bottom: 15px;
            }
            QLabel#field-label {
                color: #334155;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
            }
            QLineEdit {
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 12px 15px;
                background: white;
                font-size: 15px;
                height: 20px;
                color: #334155;
            }
            QLineEdit:focus {
                border: 1px solid #3B82F6;
                background-color: #F0F9FF;
            }
            QLineEdit::placeholder {
                color: #94A3B8;
            }
            QPushButton#login-button {
                background-color: #1E40AF;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border-radius: 6px;
                border: none;
                height: 45px;
            }
            QPushButton#login-button:hover {
                background-color: #1E3A8A;
            }
            QPushButton#register-button {
                background-color: transparent;
                color: #1E40AF;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border-radius: 6px;
                border: 1px solid #1E40AF;
                height: 45px;
            }
            QPushButton#register-button:hover {
                background-color: #EFF6FF;
            }
            QPushButton#forgot-button {
                background-color: transparent;
                color: #1E40AF;
                font-size: 14px;
                border: none;
                padding: 0px;
                text-align: right;
            }
            QPushButton#forgot-button:hover {
                color: #2563EB;
                text-decoration: underline;
            }
            QCheckBox {
                color: #64748B;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #CBD5E1;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #1E40AF;
                border: 1px solid #1E40AF;
            }
            QFrame#card {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
            QLabel#footer-text {
                color: #64748B;
                font-size: 13px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create the card widget
        card = QFrame()
        card.setObjectName("card")
        card.setContentsMargins(0, 0, 0, 0)
        
        # Add shadow effect to the card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)
        
        # Logo section
        logo_layout = QHBoxLayout()
        logo_icon = QLabel()
        logo_icon.setText("🔒")
        logo_icon.setStyleSheet("font-size: 28px;")
        logo_text = QLabel("Smart Finance")
        logo_text.setObjectName("logo-text")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.setAlignment(Qt.AlignCenter)
        card_layout.addLayout(logo_layout)
        
        # Title and subtitle
        title = QLabel("Welcome Back")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        subtitle = QLabel("Sign in to access your portfolio and investments")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(20)
        
        # Form layouts
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("field-label")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("field-label")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)
        
        # Error label – מוצג רק במקרה של כישלון
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.error_label)
        
        # Remember me and forgot password
        remember_forgot_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")
        remember_forgot_layout.addWidget(self.remember_checkbox)
        forgot_button = QPushButton("Forgot Password?")
        forgot_button.setObjectName("forgot-button")
        remember_forgot_layout.addWidget(forgot_button)
        remember_forgot_layout.setAlignment(forgot_button, Qt.AlignRight)
        form_layout.addLayout(remember_forgot_layout)
        form_layout.addSpacing(10)
        
        card_layout.addLayout(form_layout)
        
        # Buttons
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("login-button")
        self.login_button.clicked.connect(self.on_login_clicked)
        card_layout.addWidget(self.login_button)
        
        card_layout.addSpacing(10)
        
        self.register_button = QPushButton("Create New Account")
        self.register_button.setObjectName("register-button")
        card_layout.addWidget(self.register_button)
        
        # Footer
        card_layout.addSpacing(20)
        footer_text = QLabel("By signing in, you agree to our Terms of Service and Privacy Policy")
        footer_text.setObjectName("footer-text")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setWordWrap(True)
        card_layout.addWidget(footer_text)
        
        main_layout.addWidget(card, 1, Qt.AlignCenter)
        self.setLayout(main_layout)
        
        # יצירת ה-presenter והמודל
        from presenters.login_presenter import LoginPresenter
        from models.mock_stock_model import MockStockModel
        self.model = MockStockModel()
        self.presenter = LoginPresenter(self, self.model)
        print("LoginDialog: Presenter initialized")

    def on_login_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"LoginDialog: on_login_clicked() called with username={username}, password={password}")
        result = self.presenter.perform_login(username, password)
        if result:
            print("LoginDialog: Login successful, closing dialog.")
            self.username = username
            self.accept()
        else:
            print("LoginDialog: Login failed, please try again.")
            self.error_label.setText("Username or password incorrect.")

    def get_username(self):
        return self.username
