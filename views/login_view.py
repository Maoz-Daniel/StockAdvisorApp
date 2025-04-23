# login_view.py

from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect,
                              QLineEdit, QPushButton, QCheckBox, QFrame, QGraphicsDropShadowEffect,
                              QProgressBar)
from PySide6.QtCore import Qt, QTimer, Signal, Slot, QPropertyAnimation, QRect, QEasingCurve, QPoint, QSize
from PySide6.QtGui import QColor, QIcon, QFont, QPixmap
from PySide6.QtSvg import QSvgRenderer

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
        self.setFixedSize(1200, 650)  # Wider dialog to accommodate the new design
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
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        
        # Start floating elements animation
        self._start_float_animation()
    
    def _apply_stylesheet(self):
        """Apply stylesheet to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: #F8FAFC;
                font-family: 'Segoe UI', 'Open Sans', sans-serif;
            }
            QLabel {
                color: #324A5E;
                font-family: 'Segoe UI', 'Open Sans', sans-serif;
            }
            QLabel#logo-text {
                color: #324A5E;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QLabel#hero-title {
                color: #1E293B;
                font-size: 42px;
                font-weight: bold;
                line-height: 1.2;
                margin-bottom: 10px;
            }
            QLabel#hero-subtitle {
                color: #4B5563;
                font-size: 20px;
                margin-bottom: 20px;
            }
            QLabel#form-title {
                color: #1E293B;
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 10px;
            }
            QLabel#field-label {
                color: #1E293B;
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
            }
            QLineEdit {
                border: 1.5px solid #CBD5E1;
                border-radius: 8px;
                padding: 12px 15px;
                background: white;
                font-size: 16px;
                height: 25px;
                color: #1E293B;
                transition: all 0.3s;
            }
            QLineEdit:focus {
                border: 1.5px solid #4F46E5;
                background-color: #F0F9FF;
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
            }
            QLineEdit::placeholder {
                color: #94A3B8;
            }
            QPushButton#login-button {
                background-color: #4F46E5;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border-radius: 8px;
                border: none;
                height: 46px;
                transition: all 0.3s ease;
            }
            QPushButton#login-button:hover {
                background-color: #4338CA;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
            }
            QPushButton#login-button:pressed {
                transform: translateY(1px);
                box-shadow: 0 2px 6px rgba(79, 70, 229, 0.2);
            }
            QPushButton#register-button {
                background-color: transparent;
                color: #4F46E5;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 0px;
                border: none;
                height: 30px;
                text-align: center;
                transition: all 0.3s ease;
            }
            QPushButton#register-button:hover {
                color: #4338CA;
                text-decoration: underline;
            }
            QPushButton#forgot-button {
                background-color: transparent;
                color: #4F46E5;
                font-size: 14px;
                border: none;
                padding: 0px;
                text-align: right;
                transition: all 0.2s ease;
            }
            QPushButton#forgot-button:hover {
                color: #4338CA;
                text-decoration: underline;
            }
            QPushButton#show-password-button {
                background-color: transparent;
                border: none;
                color: #94A3B8;
                transition: color 0.2s ease;
            }
            QPushButton#show-password-button:hover {
                color: #4F46E5;
            }
            QCheckBox {
                color: #4B5563;
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
                background-color: #4F46E5;
                border: 1px solid #4F46E5;
            }
            QFrame#card {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
            QFrame#metric-item {
                padding: 8px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 12px;
                margin: 5px;
                transition: all 0.3s ease;
            }
            QFrame#metric-item:hover {
                background-color: white;
                box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
                transform: translateY(-5px);
            }
            QLabel#metric-value {
                color: #1E293B;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel#metric-label {
                color: #4B5563;
                font-size: 14px;
            }
            QLabel#float-element {
                background-color: white;
                border-radius: 8px;
                padding: 8px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            }
            QProgressBar {
                border: 1px solid #E2E8F0;
                border-radius: 5px;
                text-align: center;
                height: 20px;
                background-color: #F1F5F9;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #EC4899);
                border-radius: 5px;
            }
            QLabel#loading-text {
                color: #4F46E5;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton#watch-demo {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:1 #EC4899);
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 24px;
                border: none;
                height: 48px;
                transition: all 0.3s ease;
            }
            QPushButton#watch-demo:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338CA, stop:1 #DB2777);
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
            }
            QPushButton#watch-demo:pressed {
                transform: translateY(1px);
                box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);
            }
            QPushButton#explore-plans {
                background-color: transparent;
                color: #4F46E5;
                font-size: 15px;
                font-weight: bold;
                border: none;
                text-decoration: underline;
                transition: all 0.2s ease;
            }
            QPushButton#explore-plans:hover {
                color: #4338CA;
                transform: translateY(-1px);
            }
        """)
    
    def _setup_ui(self):
        """Set up UI components"""
        main_layout = QHBoxLayout()  # Changed to horizontal layout for the two-column design
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)
        
        # Left section - Hero content
        hero_section = QVBoxLayout()
        hero_section.setSpacing(20)
        
        # Hero title and subtitle
        title = QLabel("Smart Investments,\nSecure Financial Future")
        title.setObjectName("hero-title")
        title.setWordWrap(True)
        hero_section.addWidget(title)
        
        subtitle = QLabel("Professional tools and personalized advice—take control of your portfolio today.")
        subtitle.setObjectName("hero-subtitle")
        subtitle.setWordWrap(True)
        hero_section.addWidget(subtitle)
        
        # Metrics bar
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(30)
        
        # 10K+ Satisfied Investors - Using SVG instead of emoji
        metric1 = QFrame()
        metric1.setObjectName("metric-item")
        metric1_layout = QVBoxLayout(metric1)
        metric1_layout.setSpacing(2)
        
        # Create SVG for users icon
        users_svg = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="_x32_" width="40px" height="40px" viewBox="0 0 512 512" xml:space="preserve">
        <style type="text/css">
        <![CDATA[ 
        .st0{fill:#4F46E5;}
        ]]>
        </style>
        <g> 
        <path class="st0" d="M147.57,320.188c-0.078-0.797-0.328-1.531-0.328-2.328v-6.828c0-3.25,0.531-6.453,1.594-9.5 c0,0,17.016-22.781,25.063-49.547c-8.813-18.594-16.813-41.734-16.813-64.672c0-5.328,0.391-10.484,0.938-15.563 c-11.484-12.031-27-18.844-44.141-18.844c-35.391,0-64.109,28.875-64.109,73.75c0,35.906,29.219,74.875,29.219,74.875 c1.031,3.047,1.563,6.25,1.563,9.5v6.828c0,8.516-4.969,16.266-12.719,19.813l-46.391,18.953 C10.664,361.594,2.992,371.5,0.852,383.156l-0.797,10.203c-0.406,5.313,1.406,10.547,5.031,14.438 c3.609,3.922,8.688,6.125,14.016,6.125H94.93l3.109-39.953l0.203-1 .078c3.797-20.953,17.641-38.766,36.984-47.672L147.57,320.188z"/> 
        <path class="st0" d="M511.148,383.156c-2.125-11.656-9.797-21.563-20.578-26.531l-46.422-18.953 c-7.75-3.547-12.688-11.297-12.688-19.813v-6.828c0-3.25,0.516-6.453,1.578-9.5c0,0,29.203-38.969,29.203-74.875 c0-44.875-28.703-73.75-64.156-73.75c-17.109,0-32.625,6.813-44.141,18.875c0.563,5.063,0.953,10.203,0.953,15.531 c0,22.922-7.984,46.063-16.781,64.656c8.031,26.766,25.078,49.563,25.078,49.563c1.031,3.047,1.578,6.25,1.578,9.5v6.828 c0,0.797-0.266,1.531-0.344,2.328l11.5,4.688c20.156,9.219,34,27.031,37.844,47.984l0.188,1.094l3.094,39.969h75.859 c5.328,0,10.406-2.203,14-6.125c3.625-3.891,5.438-9.125,5.031-14.438L511.148,383.156z"/> 
        <path class="st0" d="M367.867,344.609l-56.156-22.953c-9.375-4.313-15.359-13.688-15.359-23.969v-8.281 c0-3.906,0.625-7.797,1.922-11.5c0,0,35.313-47.125,35.313-90.594c0-54.313-34.734-89.234-77.594-89.234 c-42.844,0-77.594,34.922-77.594,89.234c0,43.469,35.344,90.594,35.344,90.594c1.266,3.703,1.922,7.594,1.922,11.5v8.281 c0,10.281-6.031,19.656-15.391,23.969l-56.156,22.953c-13.047,5 984-22.344,17.984-24.906,32.109l-2.891,37.203h139.672h139.672 l-2.859-37.203C390.211,362.594,380.914,350.594,367.867,344.609z"/>
        </g>
        </svg>"""
        
        users_label = QLabel()
        users_label.setObjectName("metric-icon")
        users_label.setPixmap(self._svg_to_pixmap(users_svg, 30, 30))
        metric1_layout.addWidget(users_label, 0, Qt.AlignCenter)
        
        metric1_value = QLabel("10K+")
        metric1_value.setObjectName("metric-value")
        metric1_layout.addWidget(metric1_value, 0, Qt.AlignCenter)
        
        metric1_label = QLabel("Satisfied Investors")
        metric1_label.setObjectName("metric-label")
        metric1_layout.addWidget(metric1_label, 0, Qt.AlignCenter)
        
        metrics_layout.addWidget(metric1)
        
        # 24/7 Expert Support - Using SVG clock
        metric2 = QFrame()
        metric2.setObjectName("metric-item")
        metric2_layout = QVBoxLayout(metric2)
        metric2_layout.setSpacing(2)
        
        # Create SVG for clock icon
        clock_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="40px" height="40px" viewBox="0 0 1024 1024" class="icon" version="1.1"><path d="M512 512m-426.666667 0a426.666667 426.666667 0 1 0 853.333334 0 426.666667 426.666667 0 1 0-853.333334 0Z" fill="#00ACC1"/><path d="M512 512m-341.333333 0a341.333333 341.333333 0 1 0 682.666666 0 341.333333 341.333333 0 1 0-682.666666 0Z" fill="#EEEEEE"/><path d="M490.666667 234.666667h42.666666v277.333333h-42.666666z" fill="#4F46E5"/><path d="M667.413333 632.618667L632.746667 667.306667l-138.752-138.752 34.688-34.709334z" fill="#4F46E5"/><path d="M512 512m-42.666667 0a42.666667 42.666667 0 1 0 85.333334 0 42.666667 42.666667 0 1 0-85.333334 0Z" fill="#4F46E5"/><path d="M512 512m-21.333333 0a21.333333 21.333333 0 1 0 42.666666 0 21.333333 21.333333 0 1 0-42.666666 0Z" fill="#00ACC1"/></svg>"""
        
        clock_label = QLabel()
        clock_label.setObjectName("metric-icon")
        clock_label.setPixmap(self._svg_to_pixmap(clock_svg, 30, 30))
        metric2_layout.addWidget(clock_label, 0, Qt.AlignCenter)
        
        metric2_value = QLabel("24/7")
        metric2_value.setObjectName("metric-value")
        metric2_layout.addWidget(metric2_value, 0, Qt.AlignCenter)
        
        metric2_label = QLabel("Expert Support")
        metric2_label.setObjectName("metric-label")
        metric2_layout.addWidget(metric2_label, 0, Qt.AlignCenter)
        
        metrics_layout.addWidget(metric2)
        
        # 99.9% Platform Uptime - Using SVG shield
        metric3 = QFrame()
        metric3.setObjectName("metric-item")
        metric3_layout = QVBoxLayout(metric3)
        metric3_layout.setSpacing(2)
        
        # Create SVG for shield icon
        shield_svg = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="40px" height="40px" viewBox="0 0 24 24">
        <defs>
        <polygon id="shield-a" points="8.455 .877 6.063 11.43 0 16.419 2.21 17.919 8.455 12.827 11.295 1.601"/>
        <path id="shield-c" d="M1.24082757,3.43204021 L9.24082757,0.149687264 C9.72726647,-0.0498957548 10.2727335,-0.0498957548 10.7591724,0.149687264 L18.7591724,3.43204021 C19.6808014,3.81017913 20.1836337,4.80892643 19.9385064,5.77448404 L17.331099,16.0450723 C17.2264545,16.4572674 16.9931441,16.8253759 16.6650469,17.0959448 L11.2724543,21.5430036 C10.5335703,22.1523321 9.46642971,22.1523321 8.72754569,21.5430036 L3.3349531,17.0959448 C3.00685591,16.8253759 2.77354552,16.4572674 2.66890103,16.0450723 L0.0614936214,5.77448404 C-0.183633728,4.80892643 0.319198645,3.81017913 1.24082757,3.43204021 Z M2,5.28235294 L4.60740741,15.5529412 L10,20 L15.3925926,15.5529412 L18,5.28235294 L10,2 L2,5.28235294 Z M11,7.49860418 L11,15 C11,15.5522847 10.5522847,16 10,16 C9.44771525,16 9,15.5522847 9,15 L9,6 C9,5.28679018 9.72523878,4.80284733 10.3838218,5.07659283 L14.7619957,6.89641705 C15.2719794,7.108396 15.5135599,7.69366236 15.301581,8.20364606 C15.089602,8.71362975 14.5043357,8.95521033 13.994352,8.74323139 L11,7.49860418 Z"/> 
        </defs> 
        <g fill="none" fill-rule="evenodd" transform="translate(2 1)"> 
        <g transform="translate(8 3)"> 
        <mask id="shield-b" fill="#ffffff"> 
        <use xlink:href="#shield-a"/> 
        </mask> 
        <use fill="#D8D8D8" xlink:href="#shield-a"/> 
        <g fill="#FFA0A0" mask="url(#shield-b)"> 
        <rect width="24" height="24" transform="translate(-10 -4)"/> 
        </g> 
        </g> 
        <mask id="shield-d" fill="#ffffff"> 
        <use xlink:href="#shield-c"/> 
        </mask> 
        <use fill="#000000" fill-rule="nonzero" xlink:href="#shield-c"/> 
        <g fill="#7600FF" mask="url(#shield-d)"> 
        <rect width="24" height="24" transform="translate(-2 -1)"/> 
        </g> 
        </g>
        </svg>"""
        
        shield_label = QLabel()
        shield_label.setObjectName("metric-icon")
        shield_label.setPixmap(self._svg_to_pixmap(shield_svg, 30, 30))
        metric3_layout.addWidget(shield_label, 0, Qt.AlignCenter)
        
        metric3_value = QLabel("99.9%")
        metric3_value.setObjectName("metric-value")
        metric3_layout.addWidget(metric3_value, 0, Qt.AlignCenter)
        
        metric3_label = QLabel("Platform Uptime")
        metric3_label.setObjectName("metric-label")
        metric3_layout.addWidget(metric3_label, 0, Qt.AlignCenter)
        
        metrics_layout.addWidget(metric3)
        metrics_layout.addStretch(1)
        
        hero_section.addLayout(metrics_layout)
        hero_section.addSpacing(20)
        
        # Hero buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.watch_demo = QPushButton("Pro Plan")  # Added play icon
        self.watch_demo.setObjectName("watch-demo")
        buttons_layout.addWidget(self.watch_demo)
        
        self.explore_plans = QPushButton("Explore Plans")
        self.explore_plans.setObjectName("explore-plans")
        buttons_layout.addWidget(self.explore_plans)
        
        buttons_layout.addStretch(1)
        hero_section.addLayout(buttons_layout)
        
        hero_section.addStretch(1)  # Push content to top
        
        # Right section - Auth form with floating elements
        form_container = QFrame()
        form_container.setMinimumWidth(400)
        form_container_layout = QVBoxLayout(form_container)
        form_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create the floating elements (just the chart element, removing message bubble)
        self.chart_float = QLabel("+3%")
        self.chart_float.setObjectName("float-element")
        self.chart_float.setStyleSheet("""
            QLabel#float-element {
                background-color: white;
                color: #10B981;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
        """)
        self.chart_float.setFixedSize(60, 30)
        self.chart_float.setAlignment(Qt.AlignCenter)
        self.chart_float.move(350, 10)  # Position will be animated
        
        # Create the card for login
        form_section = QFrame(form_container)
        form_section.setObjectName("card")
        form_section.setFixedWidth(380)
        form_layout = QVBoxLayout(form_section)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)
        
        # Add shadow effect to the card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 10)
        form_section.setGraphicsEffect(shadow)
        
        # Form title
        form_title = QLabel("Account Access")
        form_title.setObjectName("form-title")
        form_title.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(form_title)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setObjectName("field-label")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(48)
        form_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setObjectName("field-label")
        form_layout.addWidget(password_label)
        
        # Password field with eye icon button
        password_container = QFrame()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(48)
        password_layout.addWidget(self.password_input)
        
        # Use the specified SVG for the eye icon
        self.show_password_button = QPushButton()
        self.show_password_button.setObjectName("show-password-button")
        self.show_password_button.setFixedWidth(40)
        
        # Set the eye SVG icon
        eye_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800px" height="800px" viewBox="0 0 24 24" fill="none">
<path d="M15.0007 12C15.0007 13.6569 13.6576 15 12.0007 15C10.3439 15 9.00073 13.6569 9.00073 12C9.00073 10.3431 10.3439 9 12.0007 9C13.6576 9 15.0007 10.3431 15.0007 12Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12.0012 5C7.52354 5 3.73326 7.94288 2.45898 12C3.73324 16.0571 7.52354 19 12.0012 19C16.4788 19 20.2691 16.0571 21.5434 12C20.2691 7.94291 16.4788 5 12.0012 5Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""
        eye_pixmap = self._svg_to_pixmap(eye_svg, 18, 18)
        self.show_password_button.setIcon(QIcon(eye_pixmap))
        self.show_password_button.setIconSize(QSize(18, 18))
        
        password_layout.addWidget(self.show_password_button)
        
        form_layout.addWidget(password_container)
        
        # Forgot password link
        forgot_button = QPushButton("Forgot Password?")
        forgot_button.setObjectName("forgot-button")
        form_layout.addWidget(forgot_button, 0, Qt.AlignRight)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.error_label)
        
        # Buttons
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("login-button")
        self.login_button.setMinimumHeight(48)
        form_layout.addWidget(self.login_button)
        
        form_layout.addSpacing(10)
        # Create account link (changed to match design)
        self.register_button = QPushButton("Create New Account")
        self.register_button.setObjectName("register-button")
        form_layout.addWidget(self.register_button, 0, Qt.AlignCenter)
        
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
        
        form_layout.addWidget(self.loading_widget)
        
        # Position the floating elements
        self.chart_float.setParent(form_container)
        
        # Center the form in the container
        form_container_layout.addWidget(form_section, 0, Qt.AlignCenter)
        
        # Add left and right sections to main layout
        left_widget = QFrame()
        left_widget.setLayout(hero_section)
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(form_container, 1)
        
        self.setLayout(main_layout)
    
    def _svg_to_pixmap(self, svg_str, width, height):
        """Convert SVG string to QPixmap"""
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtGui import QPixmap, QPainter
        
        renderer = QSvgRenderer()
        renderer.load(bytes(svg_str, 'utf-8'))
        
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return pixmap
        
    def _start_float_animation(self):
        """Start the floating animation for elements"""
        # Chart float animation
        self.chart_anim = QPropertyAnimation(self.chart_float, b"geometry")
        self.chart_anim.setDuration(3000)
        self.chart_anim.setStartValue(QRect(-40, 10, 60, 30))
        self.chart_anim.setEndValue(QRect(350, 10, 60, 30))
        self.chart_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.chart_anim.start()
        
        # Setup pulse animation timer
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self._pulse_elements)
        self.pulse_timer.start(3000)  # Pulse every 3 seconds
    
    def _pulse_elements(self):
        """Create a pulse effect for floating elements"""
        # Chart element pulse
        chart_pulse = QPropertyAnimation(self.chart_float, b"geometry")
        chart_pulse.setDuration(1000)
        current_geom = self.chart_float.geometry()
        
        # Slightly grow and then shrink back
        chart_pulse.setStartValue(current_geom)
        bigger_geom = QRect(
            current_geom.x() - 2,
            current_geom.y() - 2,
            current_geom.width() + 4,
            current_geom.height() + 4
        )
        chart_pulse.setKeyValueAt(0.5, bigger_geom)
        chart_pulse.setEndValue(current_geom)
        chart_pulse.setEasingCurve(QEasingCurve.InOutQuad)
        chart_pulse.start()
    
    def set_presenter(self, presenter):
        """Set the presenter for this view"""
        self.presenter = presenter
    
    def get_username(self):
        """Get the authenticated username"""
        return self.username

    def toggle_password_visibility(self):
        """Toggle password visibility when eye icon is clicked"""
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            
            # Use SVG for eye-off icon
            eye_off_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800px" height="800px" viewBox="0 0 24 24" fill="none">
<path d="M2.99902 3L20.999 21M9.8433 9.91364C9.32066 10.4536 8.99902 11.1892 8.99902 12C8.99902 13.6569 10.3422 15 11.999 15C12.8215 15 13.5667 14.669 14.1086 14.133M6.49902 6.64715C4.59972 7.90034 3.15305 9.78394 2.45703 12C3.73128 16.0571 7.52159 19 11.9992 19C13.9881 19 15.8414 18.4194 17.3988 17.4184M10.999 5.04939C11.328 5.01673 11.6617 5 11.9992 5C16.4769 5 20.2672 7.94291 21.5414 12C21.2607 12.894 20.8577 13.7338 20.3522 14.5" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""
            
            eye_off_pixmap = self._svg_to_pixmap(eye_off_svg, 18, 18)
            self.show_password_button.setIcon(QIcon(eye_off_pixmap))
            
            # Add animation for toggle
            effect = QGraphicsOpacityEffect(self.show_password_button)
            self.show_password_button.setGraphicsEffect(effect)
            
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(200)
            anim.setStartValue(0.3)
            anim.setEndValue(1.0)
            anim.start()
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            
            # Use SVG for eye icon
            eye_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucid-eye "><path d="M2 12s3-7 10-7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>"""
            
            eye_pixmap = self._svg_to_pixmap(eye_svg, 18, 18)
            self.show_password_button.setIcon(QIcon(eye_pixmap))
            
            # Add animation for toggle
            effect = QGraphicsOpacityEffect(self.show_password_button)
            self.show_password_button.setGraphicsEffect(effect)
            
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(200)
            anim.setStartValue(0.3)
            anim.setEndValue(1.0)
            anim.start()

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
            
            # Add success animation before showing loading view
            self._animate_login_success()
            
            # Hide login form and show loading after animation
            QTimer.singleShot(800, self.show_loading_view)
            
            # Start loading data in the background
            self.presenter.start_loading_data(username, self)
        else:
            print("LoginDialog: Login failed, please try again.")
            self._animate_login_error()
            self.error_label.setText("Username or password incorrect.")
    
    def _animate_login_success(self):
        """Add a success animation when login is successful"""
        # Flash effect on login button
        success_anim = QPropertyAnimation(self.login_button, b"styleSheet")
        success_anim.setDuration(400)
        original_style = self.login_button.styleSheet()
        success_style = """
            background-color: #10B981;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 0px;
            border-radius: 8px;
            border: none;
            height: 46px;
        """
        success_anim.setStartValue(original_style)
        success_anim.setEndValue(success_style)
        success_anim.start()
    
    def _animate_login_error(self):
        """Add a shake animation when login fails"""
        # Create shake animation for login form
        shake_anim = QPropertyAnimation(self.password_input, b"pos")
        shake_anim.setDuration(500)
        
        # Get current position
        pos = self.password_input.pos()
        x, y = pos.x(), pos.y()
        
        # Define keyframes for shake effect
        shake_anim.setKeyValueAt(0, pos)
        shake_anim.setKeyValueAt(0.1, QPoint(x+10, y))
        shake_anim.setKeyValueAt(0.2, QPoint(x-10, y))
        shake_anim.setKeyValueAt(0.3, QPoint(x+6, y))
        shake_anim.setKeyValueAt(0.4, QPoint(x-6, y))
        shake_anim.setKeyValueAt(0.5, QPoint(x+3, y))
        shake_anim.setKeyValueAt(0.6, QPoint(x-3, y))
        shake_anim.setKeyValueAt(0.7, QPoint(x+1, y))
        shake_anim.setKeyValueAt(0.8, QPoint(x-1, y))
        shake_anim.setKeyValueAt(1, pos)
        
        # Use ease-out curve for more natural shake
        shake_anim.setEasingCurve(QEasingCurve.OutQuad)
        shake_anim.start()
    
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
            color: #4F46E5;
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
                background-color: #4F46E5;
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