# register_view.py
from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart Finance - Create Account")
        self.setFixedSize(450, 600)
        
        # Set window flags
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Apply stylesheets (same as login dialog for consistency)
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
            QPushButton#register-button {
                background-color: #1E40AF;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border-radius: 6px;
                border: none;
                height: 45px;
            }
            QPushButton#register-button:hover {
                background-color: #1E3A8A;
            }
            QPushButton#cancel-button {
                background-color: transparent;
                color: #64748B;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border-radius: 6px;
                border: 1px solid #CBD5E1;
                height: 45px;
            }
            QPushButton#cancel-button:hover {
                background-color: #F1F5F9;
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
            QLabel#error-text {
                color: #EF4444;
                font-size: 14px;
                margin-top: 5px;
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
        logo_icon.setText("🔐")
        logo_icon.setStyleSheet("font-size: 28px;")
        logo_text = QLabel("Smart Finance")
        logo_text.setObjectName("logo-text")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.setAlignment(Qt.AlignCenter)
        card_layout.addLayout(logo_layout)
        
        # Title and subtitle
        title = QLabel("Create New Account")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        subtitle = QLabel("Join Smart Finance and start managing your investments")
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
        self.username_input.setPlaceholderText("Choose a username")
        form_layout.addWidget(self.username_input)
        
        # Email field
        email_label = QLabel("Email")
        email_label.setObjectName("field-label")
        form_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        form_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("field-label")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)
        
        # Confirm Password field
        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setObjectName("field-label")
        form_layout.addWidget(confirm_password_label)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.confirm_password_input)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setObjectName("error-text")
        self.error_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.error_label)
        
        card_layout.addLayout(form_layout)
        
        # Buttons
        self.register_button = QPushButton("Create Account")
        self.register_button.setObjectName("register-button")
        self.register_button.clicked.connect(self.on_register_clicked)
        card_layout.addWidget(self.register_button)
        
        card_layout.addSpacing(10)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel-button")
        self.cancel_button.clicked.connect(self.reject)
        card_layout.addWidget(self.cancel_button)
        
        # Footer
        card_layout.addSpacing(20)
        footer_text = QLabel("By creating an account, you agree to our Terms of Service and Privacy Policy")
        footer_text.setObjectName("footer-text")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setWordWrap(True)
        card_layout.addWidget(footer_text)
        
        main_layout.addWidget(card, 1, Qt.AlignCenter)
        self.setLayout(main_layout)
    
    def set_presenter(self, presenter):
        self.presenter = presenter
    
    def on_register_clicked(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validation
        if not username or not email or not password or not confirm_password:
            self.error_label.setText("All fields are required")
            return
            
        if password != confirm_password:
            self.error_label.setText("Passwords do not match")
            return
            
        # Call presenter
        print(f"RegisterDialog: Attempting to register user: {username}")
        result = self.presenter.perform_registration(username, email, password)
        
        if result:
            print("RegisterDialog: Registration successful, closing dialog")
            self.accept()
        else:
            print("RegisterDialog: Registration failed")
            self.error_label.setText("Registration failed. Username may already exist.")