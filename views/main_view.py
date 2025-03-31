import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtSvg import QSvgRenderer

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMenuBar, QStatusBar,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QMenu,
    QHeaderView, QFrame, QTabWidget, QGraphicsDropShadowEffect, QApplication, QScrollArea,
    QMessageBox, QSizePolicy, QGraphicsOpacityEffect, QSpacerItem, QLineEdit, QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
)
from PySide6.QtGui import QAction, QColor, QFont, QPalette, QBrush, QGradient, QLinearGradient, QPixmap, QIcon, QPainter
from PySide6.QtCore import Qt, QDate, QSize, QPropertyAnimation, QEasingCurve, QTimer, QByteArray

from buy_order_view import BuyOrderWindow
from sell_order_view import SellOrderWindow
from ai_advisor_view import AIAdvisorWindow
from trade_history_view import TradeHistoryWindow

from presenters.main_presenter import MainPresenter

# Import the FaceID6 theme
from assets.theme import FaceID6Theme
from assets.theme import LuxuryTheme
from assets.theme import DarkLuxuryTheme


class MainView(QMainWindow):
    def __init__(self, username, model, parent=None):
        super().__init__()
        
        # Apply theme first
        self.setStyleSheet(FaceID6Theme.STYLE_SHEET)

        self.username = username
        self.model = model

        self.setWindowTitle(f"SmartInvest Pro - {username}")

        # Connect the Presenter
        self.presenter = MainPresenter(self, model)

        # Set window size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() * 0.85), int(screen_size.height() * 0.85))

        # Create header bar early
        self.create_header_bar()

        # Setup layouts and other components
        self.setup_main_layout()
        # self.setup_menu_bar()
        self.create_header()
        self.create_action_buttons()
        self.create_portfolio_view()
        self.create_market_overview()
        self.setup_status_bar()

        # Load data from presenter
        self.presenter.load_user_data()
        self.presenter.load_portfolio_data()

        print(f"MainView.__init__: Received model with username: {model.get_username()}")


    def create_header_bar(self):
        """Create a visible header bar with logo and navigation buttons"""
        # Create header frame
        self.header_frame = QFrame(self)
        self.header_frame.setObjectName("header-bar")
        self.header_frame.setGeometry(0, 0, self.width(), 60)
        
        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # SVG Logo with dollar sign
        svg_data = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-dollar-sign h-8 w-8 text-emerald-400"><line x1="12" x2="12" y1="2" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>"""

        # Create logo from SVG
        logo_renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        logo_pixmap = QPixmap(24, 24)
        logo_pixmap.fill(Qt.transparent)
        logo_painter = QPainter(logo_pixmap)
        logo_renderer.render(logo_painter)
        logo_painter.end()
        
        # Logo widget
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        
        # App name
        app_name = QLabel("InvestPro")
        app_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-left: 10px;")
        
        # Logo container
        logo_container = QHBoxLayout()
        logo_container.addWidget(logo_label)
        logo_container.addWidget(app_name)
        logo_container.addStretch()
        
        # Navigation buttons layout
        nav_layout = QHBoxLayout()
        
        # Define menu options with actions
        menu_options = [
            ("Main Menu", [
                ("Dashboard", self.open_dashboard),
                ("My Portfolio", self.open_portfolio),
                ("Market Overview", self.open_market_overview),
                ("Reports & Analysis", self.open_reports),
                ("Account Settings", self.open_account_settings),
                ("Exit", self.close)
            ]),
            ("Trading", [
                ("Buy Assets", self.presenter.open_buy_order),
                ("Sell Assets", self.presenter.open_sell_order),
                ("Order History", self.presenter.open_trade_history)
            ]),
            ("Analytics", [
                ("Performance", self.open_performance),
                ("Risk Analysis", self.open_risk_analysis),
                ("AI Insights", self.presenter.open_ai_advisor)
            ]),
            ("Help", [
                ("Documentation", self.open_documentation),
                ("Support", self.open_support),
                ("About", self.open_about)
            ])
        ]
        
        # Create dropdown menus
        for menu_name, menu_items in menu_options:
            menu_btn = QPushButton(menu_name)
            menu_btn.setStyleSheet("""
                QPushButton {
                    color: #D1D5DB;
                    background: transparent;
                    border: none;
                    padding: 8px 12px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: white;
                }
            """)
            
            # Create dropdown menu
            dropdown_menu = QMenu()
            for item_name, action in menu_items:
                menu_action = dropdown_menu.addAction(item_name)
                menu_action.triggered.connect(action)
            
            # Set dropdown menu for button
            menu_btn.setMenu(dropdown_menu)
            
            nav_layout.addWidget(menu_btn)
        
        # Account button
        account_btn = QPushButton()
        account_btn.setIcon(QIcon.fromTheme("user-identity"))  # Fallback icon
        svg_user_data = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="transparent" stroke="#D1D5DB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user h-6 w-6"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
        
        # Create user icon from SVG
        user_renderer = QSvgRenderer(QByteArray(svg_user_data.encode()))
        user_pixmap = QPixmap(24, 24)
        user_pixmap.fill(Qt.transparent)
        user_painter = QPainter(user_pixmap)
        user_renderer.render(user_painter)
        user_painter.end()
        
        account_btn.setIcon(QIcon(user_pixmap))
        account_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 20px;
                padding: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Main header layout
        header_layout.addLayout(logo_container)
        header_layout.addLayout(nav_layout)
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Overall frame styling
        self.header_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                color: white;
            }
        """)
    def setup_header_bar(self):
        """Create a visible header bar with logo and account button"""
        # Create header frame
        self.header_frame = QFrame(self)
        self.header_frame.setObjectName("header-bar")
        self.header_frame.setGeometry(0, 0, self.width(), 60)
        
        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 0, 15, 0)
        
        # SVG Logo with dollar sign
        svg_data = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-dollar-sign h-8 w-8 text-emerald-400"><line x1="12" x2="12" y1="2" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>"""

        # Create logo from SVG
        logo_renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        logo_pixmap = QPixmap(24, 24)
        logo_pixmap.fill(Qt.transparent)
        logo_painter = QPainter(logo_pixmap)
        logo_renderer.render(logo_painter)
        logo_painter.end()
        
        # Logo widget
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)
        
        # App name
        app_name = QLabel("InvestPro")
        app_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-left: 10px;")
        
        # Logo container
        logo_container = QHBoxLayout()
        logo_container.addWidget(logo_label)
        logo_container.addWidget(app_name)
        logo_container.addStretch()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        # Define menu options
        menu_options = [
            ("Main Menu", [
                ("Dashboard", "lucide-layout-dashboard"),
                ("My Portfolio", "lucide-pie-chart"),
                ("Market Overview", "lucide-bar-chart3"),
                ("Reports & Analysis", "lucide-line-chart"),
                ("Account Settings", "lucide-settings")
            ]),
            ("Trading", [
                ("Buy Assets", "lucide-trending-up"),
                ("Sell Assets", "lucide-trending-down"),
                ("Order History", "lucide-history")
            ]),
            ("Analytics", [
                ("Performance", "lucide-line-chart"),
                ("Risk Analysis", "lucide-shield-alert"),
                ("AI Insights", "lucide-brain")
            ]),
            ("Help", [
                ("Documentation", "lucide-book-open"),
                ("Support", "lucide-help-circle"),
                ("About", "lucide-info")
            ])
        ]
        
        # Create dropdown menus
        for menu_name, _ in menu_options:
            menu_btn = QPushButton(menu_name)
            menu_btn.setStyleSheet("""
                QPushButton {
                    color: #D1D5DB;
                    background: transparent;
                    border: none;
                    padding: 8px 12px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: white;
                }
            """)
            nav_layout.addWidget(menu_btn)
        
        # Account button
        account_btn = QPushButton()
        account_btn.setIcon(QIcon.fromTheme("user-identity"))  # Fallback icon
        svg_user_data = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user h-6 w-6"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
        
        # Create user icon from SVG
        user_renderer = QSvgRenderer(QByteArray(svg_user_data.encode()))
        user_pixmap = QPixmap(24, 24)
        user_pixmap.fill(Qt.transparent)
        user_painter = QPainter(user_pixmap)
        user_renderer.render(user_painter)
        user_painter.end()
        
        account_btn.setIcon(QIcon(user_pixmap))
        account_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 20px;
                padding: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        
        # Main header layout
        header_layout.addLayout(logo_container)
        header_layout.addLayout(nav_layout)
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Overall frame styling
        self.header_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                color: white;
            }
        """)
    def setup_menu_bar(self):
        """Setup the application menu bar"""
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create main menu
        self.file_menu = QMenu("Main Menu", self)
        self.menu_bar.addMenu(self.file_menu)

        # Create menu actions
        self.dashboard_action = QAction("Dashboard", self)
        self.portfolio_action = QAction("My Portfolio", self)
        self.market_action = QAction("Market Overview", self)
        self.reports_action = QAction("Reports & Analysis", self)
        self.settings_action = QAction("Account Settings", self)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        # Add actions to menu
        self.file_menu.addAction(self.dashboard_action)
        self.file_menu.addAction(self.portfolio_action)
        self.file_menu.addAction(self.market_action)
        self.file_menu.addAction(self.reports_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addAction(self.exit_action)
        
        # Additional menus
        trading_menu = QMenu("Trading", self)
        self.menu_bar.addMenu(trading_menu)
        
        trading_menu.addAction("Buy Assets")
        trading_menu.addAction("Sell Assets")
        trading_menu.addAction("Order History")
        
        analysis_menu = QMenu("Analytics", self)
        self.menu_bar.addMenu(analysis_menu)
        
        analysis_menu.addAction("Performance")
        analysis_menu.addAction("Risk Analysis")
        analysis_menu.addAction("AI Insights")
        
        help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(help_menu)
        
        help_menu.addAction("Documentation")
        help_menu.addAction("Support")
        help_menu.addAction("About")

    def resizeEvent(self, event):
        """Handle resize events to adjust header bar width"""
        super().resizeEvent(event)
        if hasattr(self, 'header_frame'):
            # Ensure the header bar spans the full width of the window and stays at the top
            self.header_frame.setGeometry(0, 0, self.width(), 60)

    def setup_main_layout(self):
        """Setup the main layout with a fixed header and scrollable content"""
        # Create a main vertical layout for the entire window
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Ensure the header frame is at the top and fixed
        if hasattr(self, 'header_frame'):
            main_layout.addWidget(self.header_frame)
            self.header_frame.setFixedHeight(60)  # Ensure consistent height
            self.header_frame.setObjectName("header-bar")  # Ensure correct styling

        # Main container for scrollable content
        container = QWidget()
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(25)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(container)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        # Add scroll area to main layout
        main_layout.addWidget(self.scroll_area)

        # Create a central widget to hold the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

    def create_header(self):
        """Create modern header with user greeting"""
        # Create header frame
        self.header_frame = QFrame()
        self.header_frame.setObjectName("header-frame")
        
        # Add subtle shadow effect
        shadow = QGraphicsDropShadowEffect(self.header_frame)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.header_frame.setGraphicsEffect(shadow)
        
        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Left side with welcome message
        left_layout = QVBoxLayout()
        
        # Welcome label
        self.label = QLabel("Welcome, Loading...")
        self.label.setObjectName("welcome-label")
        
        # Subtitle with date
        current_date = QDate.currentDate().toString("dddd, MMMM d, yyyy")
        subtitle = QLabel(f"Today is {current_date}")
        subtitle.setObjectName("subtitle-label")
        
        left_layout.addWidget(self.label)
        left_layout.addWidget(subtitle)
        left_layout.addStretch()
        
        # Right side with account summary
        right_frame = QFrame()
        right_frame.setObjectName("info-card")
        
        right_layout = QVBoxLayout(right_frame)
        
        account_label = QLabel("Premium Account")
        account_label.setObjectName("account-text")
        
        last_login = QLabel("Last login: Today, 09:15 AM")
        last_login.setStyleSheet("color: #666666; font-size: 12px;")
        
        # Quote
        smart_quote = QLabel("\"Precision in timing, diversity in selection, patience in growth.\"")
        smart_quote.setObjectName("quote-text")
        smart_quote.setWordWrap(True)
        
        right_layout.addWidget(account_label)
        right_layout.addWidget(last_login)
        right_layout.addWidget(smart_quote)
        
        # Add both sections to header
        header_layout.addLayout(left_layout, 7)
        header_layout.addWidget(right_frame, 3)
        
        self.main_layout.addWidget(self.header_frame)

    def create_action_buttons(self):
        """Create modern action buttons"""
        # Section title
        action_title = QLabel("Investment Actions")
        action_title.setObjectName("section-title")
        action_title.setStyleSheet("font-size: 22px; font-weight: 600;")
        self.main_layout.addWidget(action_title)
        
        # Button container
        button_frame = QFrame()
        button_frame.setObjectName("card")
        button_frame.setStyleSheet("QFrame#card { padding: 20px; }")
        
        # Shadow effect
        button_shadow = QGraphicsDropShadowEffect(button_frame)
        button_shadow.setBlurRadius(10)
        button_shadow.setColor(QColor(0, 0, 0, 30))
        button_shadow.setOffset(0, 3)
        button_frame.setGraphicsEffect(button_shadow)
        
        # Layout for buttons
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)
        
        svg_data = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>"""

        # Create icon from SVG data
        buy_icon = QIcon()
        renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        buy_icon.addPixmap(pixmap)

        # Create button with icon
        self.btn_buy_order = QPushButton("Buy Order")  # Remove the emoji
        self.btn_buy_order.setIcon(buy_icon)
        self.btn_buy_order.setIconSize(QSize(24, 24))
        self.btn_buy_order.setStyleSheet("""
            QPushButton {
                background-color: rgba(16, 185, 129, 0.2);
                color: #10B981;
                border: none;
                border-radius: 10px;
                padding: 15px 20px;
                padding-left: 15px;  /* Adjust padding for icon */
                font-size: 16px;
                font-weight: 600;
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgba(16, 185, 129, 0.3);
            }
        """)
        self.btn_buy_order.clicked.connect(self.presenter.open_buy_order)
        
        svg_data_sell = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F77070" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trending-down h-5 w-5 text-red-400 mr-2"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline><polyline points="16 17 22 17 22 11"></polyline></svg>"""

        # Create icon from SVG data for sell button
        sell_icon = QIcon()
        renderer_sell = QSvgRenderer(QByteArray(svg_data_sell.encode()))
        pixmap_sell = QPixmap(24, 24)
        pixmap_sell.fill(Qt.transparent)
        painter_sell = QPainter(pixmap_sell)
        renderer_sell.render(painter_sell)
        painter_sell.end()
        sell_icon.addPixmap(pixmap_sell)

        self.btn_sell_order = QPushButton("Sell Order")
        self.btn_sell_order.setIcon(sell_icon)
        self.btn_sell_order.setIconSize(QSize(24, 24))
        self.btn_sell_order.setStyleSheet("""
        QPushButton {
            background-color: rgba(239, 68, 68, 0.2);
            color: #FCA5A5;
            border: none;
            border-radius: 10px;
            padding: 15px 20px;
            padding-left: 15px;  /* Adjust padding for icon */
            font-size: 16px;
            font-weight: 600;
            text-align: center;
        }
        QPushButton:hover {
            background-color: rgba(239, 68, 68, 0.3);
        }
    """)
        self.btn_sell_order.clicked.connect(self.presenter.open_sell_order)
        
        svg_data_ai = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-brain h-5 w-5 text-blue-400 mr-2"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"></path><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"></path><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"></path><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"></path><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"></path><path d="M3.477 10.896a4 4 0 0 1 .585-.396"></path><path d="M19.938 10.5a4 4 0 0 1 .585.396"></path><path d="M6 18a4 4 0 0 1-1.967-.516"></path><path d="M19.967 17.484A4 4 0 0 1 18 18"></path></svg>"""

        # Create icon from SVG data for AI Advisor button
        ai_icon = QIcon()
        renderer_ai = QSvgRenderer(QByteArray(svg_data_ai.encode()))
        pixmap_ai = QPixmap(24, 24)
        pixmap_ai.fill(Qt.transparent)
        painter_ai = QPainter(pixmap_ai)
        renderer_ai.render(painter_ai)
        painter_ai.end()
        ai_icon.addPixmap(pixmap_ai)

        self.btn_ai_advisor = QPushButton("AI Advisor")
        self.btn_ai_advisor.setIcon(ai_icon)
        self.btn_ai_advisor.setIconSize(QSize(24, 24))
        self.btn_ai_advisor.setStyleSheet("""
        QPushButton {
            background-color: rgba(59, 130, 246, 0.2);
            color: #93C5FD;
            border: none;
            border-radius: 10px;
            padding: 15px 20px;
            padding-left: 15px;  /* Adjust padding for icon */
            font-size: 16px;
            font-weight: 600;
            text-align: center;
        }
        QPushButton:hover {
            background-color: rgba(59, 130, 246, 0.3);
        }
    """)
        self.btn_ai_advisor.clicked.connect(self.presenter.open_ai_advisor)
        svg_data_history = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#CBA2F3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-history h-5 w-5 text-purple-400 mr-2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path><path d="M12 7v5l4 2"></path></svg>"""

        # Create icon from SVG data for Trade History button
        history_icon = QIcon()
        renderer_history = QSvgRenderer(QByteArray(svg_data_history.encode()))
        pixmap_history = QPixmap(24, 24)
        pixmap_history.fill(Qt.transparent)
        painter_history = QPainter(pixmap_history)
        renderer_history.render(painter_history)
        painter_history.end()
        history_icon.addPixmap(pixmap_history)

        self.btn_trade_history = QPushButton("Trade History")
        self.btn_trade_history.setIcon(history_icon)
        self.btn_trade_history.setIconSize(QSize(24, 24))

        self.btn_trade_history.setStyleSheet("""
    QPushButton {
        background-color: rgba(168, 85, 247, 0.2);
        color: #C4B5FD;
        border: none;
        border-radius: 10px;
        padding: 15px 20px;
        padding-left: 15px;  /* Adjust padding for icon */
        font-size: 16px;
        font-weight: 600;
        text-align: center;
    }
    QPushButton:hover {
        background-color: rgba(168, 85, 247, 0.3);
    }
""")
        self.btn_trade_history.clicked.connect(self.presenter.open_trade_history)
        
        # Add buttons to layout
        button_layout.addWidget(self.btn_buy_order)
        button_layout.addWidget(self.btn_sell_order)
        button_layout.addWidget(self.btn_ai_advisor)
        button_layout.addWidget(self.btn_trade_history)
        
        self.main_layout.addWidget(button_frame)

    def create_portfolio_view(self):
        """Create portfolio view with tabs and table"""
        # Section title
        portfolio_title = QLabel("Your Portfolio")
        portfolio_title.setObjectName("section-title")
        self.main_layout.addWidget(portfolio_title)
        
        # Create card for portfolio
        portfolio_card = QFrame()
        portfolio_card.setObjectName("card")
        portfolio_card.setStyleSheet("QFrame#card { padding: 0; }")
        
        # Shadow effect
        portfolio_shadow = QGraphicsDropShadowEffect(portfolio_card)
        portfolio_shadow.setBlurRadius(8)
        portfolio_shadow.setColor(QColor(0, 0, 0, 20))
        portfolio_shadow.setOffset(0, 2)
        portfolio_card.setGraphicsEffect(portfolio_shadow)
        
        # Layout for portfolio card
        portfolio_layout = QVBoxLayout(portfolio_card)
        portfolio_layout.setContentsMargins(0, 0, 0, 0)
        portfolio_layout.setSpacing(0)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Portfolio tab
        portfolio_tab = QWidget()
        tab_layout = QVBoxLayout(portfolio_tab)
        tab_layout.setContentsMargins(15, 15, 15, 15)
        
        # Portfolio summary
        summary_frame = QFrame()
        summary_frame.setObjectName("summary-card")
        
        summary_layout = QHBoxLayout(summary_frame)
        
        # Portfolio value
        value_layout = QVBoxLayout()
        value_label = QLabel("Total Portfolio Value")
        value_label.setStyleSheet("color: #666666; font-size: 13px;")
        value_amount = QLabel("$157,384.25")
        value_amount.setObjectName("large-value")
        value_layout.addWidget(value_label)
        value_layout.addWidget(value_amount)
        
        # Daily change
        change_layout = QVBoxLayout()
        change_label = QLabel("Today's Change")
        change_label.setStyleSheet("color: #666666; font-size: 13px;")
        change_amount = QLabel("+$2,157.83 (+1.39%)")
        change_amount.setStyleSheet("color: #34C759; font-size: 16px; font-weight: bold;")
        change_layout.addWidget(change_label)
        change_layout.addWidget(change_amount)
        
        # Cash balance
        cash_layout = QVBoxLayout()
        cash_label = QLabel("Cash Balance")
        cash_label.setStyleSheet("color: #666666; font-size: 13px;")
        cash_amount = QLabel("$24,325.00")
        cash_amount.setObjectName("value-text")
        cash_layout.addWidget(cash_label)
        cash_layout.addWidget(cash_amount)
        
        summary_layout.addLayout(value_layout, 4)
        summary_layout.addLayout(change_layout, 3)
        summary_layout.addLayout(cash_layout, 3)
        
        tab_layout.addWidget(summary_frame)
        
        # Create portfolio table with enhanced styling
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels(["Stock", "Current Price", "Daily Change", "Quantity", "Portfolio Value"])
        self.stock_table.setMinimumHeight(250)
        
        # Enhanced table styling
        self.stock_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f8f9fa;
                gridline-color: #e4e6eb;
                border: 1px solid #e4e6eb;
                border-radius: 6px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #e4e6eb;
            }
            
            QTableWidget::item:selected {
                background-color: #e7f3ff;
                color: #0066cc;
            }
            
            QHeaderView::section {
                background-color: #f1f2f6;
                color: #555;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e4e6eb;
                font-size: 13px;
            }
            
            QHeaderView::section:horizontal {
                text-align: center;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.verticalHeader().setVisible(False)
        self.stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.stock_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Remove shadow effect for a cleaner look
        # (The CSS border and styling already provides a nice visual separation)
        
        tab_layout.addWidget(self.stock_table)
        
        # Add tabs to tab widget
        self.tabs.addTab(portfolio_tab, "Portfolio")
        
        portfolio_layout.addWidget(self.tabs)
        self.main_layout.addWidget(portfolio_card)



    def create_market_overview(self):
        """Create market overview section"""
        # Section title
        market_title = QLabel("Market Indices")
        market_title.setObjectName("section-title")
        self.main_layout.addWidget(market_title)
        
        # Market card container
        market_container = QFrame()
        market_container.setObjectName("card")
        
        # Layout for market cards
        market_layout = QHBoxLayout(market_container)
        market_layout.setContentsMargins(15, 15, 15, 15)
        market_layout.setSpacing(15)
        
        # Create market index cards
        self.create_market_card(market_layout, "S&P 500", "4,827.35", "+1.2%", True)
        self.create_market_card(market_layout, "NASDAQ", "15,425.62", "+0.8%", True)
        self.create_market_card(market_layout, "DOW", "38,256.98", "+0.5%", True)
        self.create_market_card(market_layout, "Bitcoin", "$41,235.78", "-2.3%", False)
        
        # Add subtle shadow
        market_shadow = QGraphicsDropShadowEffect(market_container)
        market_shadow.setBlurRadius(8)
        market_shadow.setColor(QColor(0, 0, 0, 20))
        market_shadow.setOffset(0, 2)
        market_container.setGraphicsEffect(market_shadow)
        
        self.main_layout.addWidget(market_container)

    def create_market_card(self, parent_layout, title, value, change, is_positive):
        """Create a market index card"""
        card = QFrame()
        card.setObjectName("market-card")
        
        # Layout for card
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(5)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("accent-text")
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value-text")
        
        # Change
        change_label = QLabel(change)
        if is_positive:
            change_label.setStyleSheet("color: #34C759; font-size: 14px;")
        else:
            change_label.setStyleSheet("color: #FF3B30; font-size: 14px;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addWidget(change_label)
        card_layout.addStretch()
        
        # Add subtle shadow
        card_shadow = QGraphicsDropShadowEffect(card)
        card_shadow.setBlurRadius(4)
        card_shadow.setColor(QColor(0, 0, 0, 15))
        card_shadow.setOffset(0, 1)
        card.setGraphicsEffect(card_shadow)
        
        parent_layout.addWidget(card)

    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Loading market data...")

    def update_header(self, text):
        """Update header text"""
        self.label.setText(text)

    def update_status_bar(self, message):
        """Update status bar message"""
        self.status_bar.showMessage(message)
        
    def update_portfolio_summary(self, total_value, total_unrealized_pl):
        """Update the portfolio summary section with total value and P/L"""
        print(f"Updating portfolio summary: Value=${total_value:.2f}, P/L=${total_unrealized_pl:.2f}")
        
        # Update the total portfolio value
        for widget in self.findChildren(QLabel):
            if widget.objectName() == "large-value":
                widget.setText(f"${total_value:,.2f}")
        
        # Update the unrealized P/L instead of daily change
        # Find the change_amount label (which currently shows daily change)
        for widget in self.findChildren(QLabel):
            if widget.text().startswith("+$") or widget.text().startswith("-$"):
                # Format with appropriate color
                if total_unrealized_pl >= 0:
                    widget.setText(f"+${total_unrealized_pl:,.2f}")
                    widget.setStyleSheet("color: #34C759; font-size: 16px; font-weight: bold;")
                else:
                    widget.setText(f"-${abs(total_unrealized_pl):,.2f}")
                    widget.setStyleSheet("color: #FF3B30; font-size: 16px; font-weight: bold;")
                break
        
        # Update the label text above the P/L value
        for widget in self.findChildren(QLabel):
            if widget.text() == "Today's Change":
                widget.setText("Total Profit/Loss")
                break
                
    def get_portfolio_total_value(self, portfolio_data=None):
        print("DEBUGGING: get_portfolio_total_value method called")
        portfolio_items = portfolio_data if portfolio_data is not None else self.get_portfolio_data()
        # Sum up the market values and unrealized P/L
        total_value = sum(item["market_value"] for item in portfolio_items)
        total_unrealized_pl = sum(item["unrealized_pl"] for item in portfolio_items)
        
        print(f"Total portfolio value calculated: ${total_value:.2f}")
        print(f"Total unrealized P/L calculated: ${total_unrealized_pl:.2f}")
        
        return total_value, total_unrealized_pl
    
    def update_portfolio_table(self, portfolio_data):
        """Update portfolio table with enhanced data"""
        headers = ["Symbol", "Qty", "Avg Buy Price", "Current Price","Market Value", "Unrealized P/L", "Allocation %"]
        self.stock_table.setColumnCount(len(headers))
        self.stock_table.setHorizontalHeaderLabels(headers)
        self.stock_table.setRowCount(len(portfolio_data))
        for row, data in enumerate(portfolio_data):
            # נעבור על כל עמודה לפי סדר הנתונים
            symbol_item = QTableWidgetItem(data["symbol"])
            qty_item = QTableWidgetItem(str(data["quantity"]))
            avg_price_item = QTableWidgetItem(f"${data['avg_buy_price']:.2f}")
            current_price_item = QTableWidgetItem(f"${data['current_price']:.2f}")
            daily_change_val = data["daily_change"] if data["daily_change"] is not None else "-"
            market_value_item = QTableWidgetItem(f"${data['market_value']:.2f}")
            unrealized_pl_item = QTableWidgetItem(f"${data['unrealized_pl']:.2f}")
            allocation_item = QTableWidgetItem(f"{data['allocation']:.1f}%")
            
            # ניתן להוסיף עיצוב: למשל, אם unrealized_pl חיובי להציג בירוק, ואם שלילי באדום
            if data["unrealized_pl"] >= 0:
                unrealized_pl_item.setForeground(QColor("#34C759"))
            else:
                unrealized_pl_item.setForeground(QColor("#FF3B30"))

            items = [symbol_item,qty_item, avg_price_item, current_price_item, market_value_item, unrealized_pl_item, allocation_item]
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.stock_table.setItem(row, col, item)

    def open_dashboard(self):
        print("Opening Dashboard")

    def open_portfolio(self):
        print("Opening Portfolio")

    def open_market_overview(self):
        print("Opening Market Overview")

    def open_reports(self):
        print("Opening Reports & Analysis")

    def open_account_settings(self):
        print("Opening Account Settings")

    def open_performance(self):
        print("Opening Performance")

    def open_risk_analysis(self):
        print("Opening Risk Analysis")

    def open_documentation(self):
        print("Opening Documentation")

    def open_support(self):
        print("Opening Support")

    def open_about(self):
        print("Opening About")