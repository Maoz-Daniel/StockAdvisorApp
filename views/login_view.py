# login_view.py

from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect,
                              QLineEdit, QPushButton, QCheckBox, QFrame, QGraphicsDropShadowEffect,
                              QProgressBar)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QColor

class LoginDialog(QDialog):
    """
    Dialog for user login with loading animation.
    Shows an overlay with progress bar during data loading.
    """
    login_success = Signal(str)  # Signal to indicate successful login with username
    close_dialog = Signal()      # Signal to close the dialog after loading
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart Finance - Secure Login")
        self.setFixedSize(450, 550)
        self.username = ""
        self.presenter = None
        
        # Set window flags
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Apply stylesheets
        self._apply_stylesheet()
        
        # Setup UI components
        self._setup_ui()
        
        # Connect signals
        self.close_dialog.connect(self.complete_login)
        self.login_button.clicked.connect(self.on_login_clicked)
        self.register_button.clicked.connect(self.on_register_clicked)
    
    def _apply_stylesheet(self):
        """Apply stylesheet to the dialog"""
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
            QProgressBar {
                border: 1px solid #E2E8F0;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #1E40AF;
                border-radius: 5px;
            }
            QLabel#loading-text {
                color: #1E40AF;
                font-size: 14px;
                font-weight: 500;
            }
        """)
    
    def _setup_ui(self):
        """Set up UI components"""
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
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("field-label")
        self.form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("field-label")
        self.form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.password_input)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.form_layout.addWidget(self.error_label)
        
        # Remember me and forgot password
        remember_forgot_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox("Remember me")
        remember_forgot_layout.addWidget(self.remember_checkbox)
        forgot_button = QPushButton("Forgot Password?")
        forgot_button.setObjectName("forgot-button")
        remember_forgot_layout.addWidget(forgot_button)
        remember_forgot_layout.setAlignment(forgot_button, Qt.AlignRight)
        self.form_layout.addLayout(remember_forgot_layout)
        self.form_layout.addSpacing(10)
        
        card_layout.addLayout(self.form_layout)
        
        # Buttons
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("login-button")
        card_layout.addWidget(self.login_button)
        
        card_layout.addSpacing(10)
        
        self.register_button = QPushButton("Create New Account")
        self.register_button.setObjectName("register-button")
        card_layout.addWidget(self.register_button)
        
        # Loading Section - Initially hidden
        self.loading_layout = QVBoxLayout()
        self.loading_layout.setSpacing(10)
        
        self.loading_text = QLabel("Loading your dashboard...")
        self.loading_text.setObjectName("loading-text")
        self.loading_text.setAlignment(Qt.AlignCenter)
        self.loading_layout.addWidget(self.loading_text)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.loading_layout.addWidget(self.progress_bar)
        
        # Create a widget to hold the loading controls
        self.loading_widget = QFrame()
        self.loading_widget.setLayout(self.loading_layout)
        self.loading_widget.setVisible(False)  # Initially hidden
        
        card_layout.addWidget(self.loading_widget)
        
        # Footer
        card_layout.addSpacing(20)
        footer_text = QLabel("By signing in, you agree to our Terms of Service and Privacy Policy")
        footer_text.setObjectName("footer-text")
        footer_text.setAlignment(Qt.AlignCenter)
        footer_text.setWordWrap(True)
        card_layout.addWidget(footer_text)
        
        main_layout.addWidget(card, 1, Qt.AlignCenter)
        self.setLayout(main_layout)
    
    def set_presenter(self, presenter):
        """Set the presenter for this view"""
        self.presenter = presenter
    
    def get_username(self):
        """Get the authenticated username"""
        return self.username

    # Login flow methods
    def on_login_clicked(self):
        """Handle login button click"""
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"LoginDialog: on_login_clicked() called with username={username}, password={password}")
        
        # Use the original perform_login method to check credentials
        if self.presenter.perform_login(username, password):
            print("LoginDialog: Login successful, showing loading bar.")
            self.username = username
            
            # Hide login form and show loading
            self.show_loading_view()
            
            # Start loading data in the background
            self.presenter.start_loading_data(username, self)
        else:
            print("LoginDialog: Login failed, please try again.")
            self.error_label.setText("Username or password incorrect.")
    
    def show_loading_view(self):
        """Create a modal overlay for the loading view"""
        # Create a semi-transparent overlay for the entire dialog
        self.overlay = QFrame(self)
        self.overlay.setObjectName("loading-overlay")
        self.overlay.setStyleSheet("""
            QFrame#loading-overlay {
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 12px;
            }
        """)
        self.overlay.setGeometry(self.rect())
        
        # Create loading components on the overlay
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setAlignment(Qt.AlignCenter)
        
        self.overlay_loading_text = QLabel("Loading your dashboard...")
        self.overlay_loading_text.setObjectName("loading-text")
        self.overlay_loading_text.setAlignment(Qt.AlignCenter)
        self.overlay_loading_text.setStyleSheet("""
            color: #1E40AF;
            font-size: 16px;
            font-weight: 500;
        """)
        
        self.overlay_progress_bar = QProgressBar()
        self.overlay_progress_bar.setRange(0, 100)
        self.overlay_progress_bar.setValue(0)
        self.overlay_progress_bar.setFixedWidth(300)
        self.overlay_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E2E8F0;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                background-color: #F8FAFC;
            }
            QProgressBar::chunk {
                background-color: #1E40AF;
                border-radius: 5px;
            }
        """)
        
        overlay_layout.addWidget(self.overlay_loading_text)
        overlay_layout.addWidget(self.overlay_progress_bar)
        
        # Show the overlay
        self.overlay.raise_()
        self.overlay.show()
        
        # Update the UI
        self.repaint()
    
    def update_progress(self, progress, status_text=None):
        """Update the progress bar with actual loading progress"""
        self.overlay_progress_bar.setValue(progress)
        
        if status_text:
            self.overlay_loading_text.setText(status_text)
        
        # Update the UI
        self.repaint()
        
        # If progress is 100%, update the text but don't automatically close
        if progress >= 100:
            self.overlay_loading_text.setText("Ready! Opening dashboard...")
            # Let the UI update before proceeding
            self.repaint()
    
    @Slot()
    def complete_login(self):
        """Complete the login process after data is loaded"""
        print("LoginDialog: Loading complete, closing dialog.")
        
        # Use a short timer to ensure the UI gets updated before closing
        QTimer.singleShot(200, self._finish_login)
    
    def _finish_login(self):
        """Actual method to close the dialog and emit success signal - called by timer"""
        if hasattr(self, 'overlay'):
            self.overlay.deleteLater()
        self.login_success.emit(self.username)
        self.accept()

    # Registration method
    def on_register_clicked(self):
        """Open the registration dialog when the register button is clicked"""
        from views.register_view import RegisterDialog
        from presenters.register_presenter import RegisterPresenter
        
        register_dialog = RegisterDialog(self)
        register_presenter = RegisterPresenter(register_dialog, self.presenter.model)
        register_dialog.set_presenter(register_presenter)
        
        if register_dialog.exec():
            # If registration was successful, automatically fill in the username
            username = register_dialog.username_input.text()
            self.username_input.setText(username)
            self.password_input.setFocus()