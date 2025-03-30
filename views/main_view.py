import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMenuBar, QStatusBar,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QMenu,
    QHeaderView, QFrame, QTabWidget, QGraphicsDropShadowEffect, QApplication, QScrollArea,
    QMessageBox, QSizePolicy, QGraphicsOpacityEffect
)
from PySide6.QtGui import QAction, QColor, QFont, QPalette, QBrush, QGradient, QLinearGradient, QPixmap, QIcon
from PySide6.QtCore import Qt, QDate, QSize, QPropertyAnimation, QEasingCurve, QTimer

from buy_order_view import BuyOrderWindow
from sell_order_view import SellOrderWindow
from ai_advisor_view import AIAdvisorWindow
from trade_history_view import TradeHistoryWindow

from presenters.main_presenter import MainPresenter

# Import the theme
from assets.theme import LuxuryTheme


class MainView(QMainWindow):
    def __init__(self, username, model, parent=None):
        super().__init__()
        self.username = username
        self.model = model

        self.setWindowTitle(f"SmartInvest Pro - {username}")

        # Connect the Presenter
        self.presenter = MainPresenter(self, model)

        # Set window size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() * 0.85), int(screen_size.height() * 0.85))

        # Apply luxury theme
        self.setStyleSheet(LuxuryTheme.STYLE_SHEET)

        # Create UI components
        self.setup_menu_bar()
        self.setup_main_layout()
        self.create_header()
        self.create_action_buttons()
        self.create_portfolio_view()
        self.create_market_overview()
        self.setup_status_bar()

        # Load data from presenter
        self.presenter.load_user_data()
        self.presenter.load_portfolio_data()

        print(f"MainView.__init__: Received model with username: {model.get_username()}")

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

    def setup_main_layout(self):
        """Setup the main layout with scroll area"""
        # Main container
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)

        container = QWidget()
        container.setLayout(self.main_layout)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(container)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(self.scroll_area)

    def create_header(self):
        """Create elegant header with user greeting"""
        # Create header frame
        self.header_frame = QFrame()
        self.header_frame.setObjectName("header-frame")
        
        # Add blue glow shadow effect with gold tint
        shadow = QGraphicsDropShadowEffect(self.header_frame)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(255, 215, 0, 30))  # Subtle gold glow
        shadow.setOffset(0, 2)
        self.header_frame.setGraphicsEffect(shadow)
        
        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(25, 25, 25, 25)
        
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
        
        # Right side with account summary and smart quote
        right_frame = QFrame()
        right_frame.setObjectName("gold-card")
        
        right_layout = QVBoxLayout(right_frame)
        
        account_label = QLabel("Premium Account")
        account_label.setObjectName("gold-text")
        
        last_login = QLabel("Last login: Today, 09:15 AM")
        last_login.setStyleSheet("color: #C0C0C0; font-size: 12px;")
        
        # Smart quote
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
        """Create elegant action buttons"""
        # Section title
        action_title = QLabel("Investment Actions")
        action_title.setObjectName("section-title")
        self.main_layout.addWidget(action_title)
        
        # Button container
        button_frame = QFrame()
        button_frame.setObjectName("card")
        button_frame.setStyleSheet("QFrame#card { padding: 20px; }")
        
        # Gold-tinted glow shadow effect
        button_shadow = QGraphicsDropShadowEffect(button_frame)
        button_shadow.setBlurRadius(15)
        button_shadow.setColor(QColor(255, 215, 0, 20))
        button_shadow.setOffset(0, 3)
        button_frame.setGraphicsEffect(button_shadow)
        
        # Layout for buttons
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)
        
        # Create action buttons with reflective styling
        self.btn_buy_order = QPushButton("📈 Buy Order")
        self.btn_buy_order.clicked.connect(self.presenter.open_buy_order)
        
        self.btn_sell_order = QPushButton("📉 Sell Order")
        self.btn_sell_order.clicked.connect(self.presenter.open_sell_order)
        
        self.btn_ai_advisor = QPushButton("🤖 AI Advisor")
        self.btn_ai_advisor.setObjectName("gold-button")
        self.btn_ai_advisor.clicked.connect(self.presenter.open_ai_advisor)
        
        self.btn_trade_history = QPushButton("📊 Trade History")
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
        
        # Gold-tinted glow shadow effect
        portfolio_shadow = QGraphicsDropShadowEffect(portfolio_card)
        portfolio_shadow.setBlurRadius(15)
        portfolio_shadow.setColor(QColor(255, 215, 0, 20))
        portfolio_shadow.setOffset(0, 3)
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
        portfolio_tab.setStyleSheet("background-color: #1E3A5F;")
        tab_layout = QVBoxLayout(portfolio_tab)
        tab_layout.setContentsMargins(20, 20, 20, 20)
        
        # Portfolio summary
        summary_frame = QFrame()
        summary_frame.setObjectName("summary-card")
        
        summary_layout = QHBoxLayout(summary_frame)
        
        # Portfolio value
        value_layout = QVBoxLayout()
        value_label = QLabel("Total Portfolio Value")
        value_label.setStyleSheet("color: #C0C0C0; font-size: 13px;")
        value_amount = QLabel("$157,384.25")
        value_amount.setObjectName("large-value")
        value_layout.addWidget(value_label)
        value_layout.addWidget(value_amount)
        
        # Daily change
        change_layout = QVBoxLayout()
        change_label = QLabel("Today's Change")
        change_label.setStyleSheet("color: #C0C0C0; font-size: 13px;")
        change_amount = QLabel("+$2,157.83 (+1.39%)")
        change_amount.setStyleSheet("color: #66CFA6; font-size: 16px; font-weight: bold;")
        change_layout.addWidget(change_label)
        change_layout.addWidget(change_amount)
        
        # Cash balance
        cash_layout = QVBoxLayout()
        cash_label = QLabel("Cash Balance")
        cash_label.setStyleSheet("color: #C0C0C0; font-size: 13px;")
        cash_amount = QLabel("$24,325.00")
        cash_amount.setObjectName("value-text")
        cash_layout.addWidget(cash_label)
        cash_layout.addWidget(cash_amount)
        
        summary_layout.addLayout(value_layout, 4)
        summary_layout.addLayout(change_layout, 3)
        summary_layout.addLayout(cash_layout, 3)
        
        tab_layout.addWidget(summary_frame)
        
        # Create portfolio table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels(["Stock", "Current Price", "Daily Change", "Quantity", "Portfolio Value"])
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.verticalHeader().setVisible(False)
        self.stock_table.setMinimumHeight(250)
        
        # Add subtle glow effect to table with gold tint
        table_shadow = QGraphicsDropShadowEffect(self.stock_table)
        table_shadow.setBlurRadius(10)
        table_shadow.setColor(QColor(255, 215, 0, 20))
        table_shadow.setOffset(0, 1)
        self.stock_table.setGraphicsEffect(table_shadow)
        
        tab_layout.addWidget(self.stock_table)
        
        # Create additional tabs (placeholders)
        performance_tab = QWidget()
        performance_tab.setStyleSheet("background-color: #1E3A5F;")
        
        watchlist_tab = QWidget()
        watchlist_tab.setStyleSheet("background-color: #1E3A5F;")
        
        history_tab = QWidget()
        history_tab.setStyleSheet("background-color: #1E3A5F;")
        
        # Add tabs to tab widget
        self.tabs.addTab(portfolio_tab, "Portfolio")
        self.tabs.addTab(performance_tab, "Performance")
        self.tabs.addTab(watchlist_tab, "Watchlist")
        self.tabs.addTab(history_tab, "History")
        
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
        market_layout.setContentsMargins(20, 20, 20, 20)
        market_layout.setSpacing(20)
        
        # Create market index cards
        self.create_market_card(market_layout, "S&P 500", "4,827.35", "+1.2%", True)
        self.create_market_card(market_layout, "NASDAQ", "15,425.62", "+0.8%", True)
        self.create_market_card(market_layout, "DOW", "38,256.98", "+0.5%", True)
        self.create_market_card(market_layout, "Bitcoin", "$41,235.78", "-2.3%", False)
        
        # Add subtle gold glow
        market_shadow = QGraphicsDropShadowEffect(market_container)
        market_shadow.setBlurRadius(15)
        market_shadow.setColor(QColor(255, 215, 0, 20))
        market_shadow.setOffset(0, 3)
        market_container.setGraphicsEffect(market_shadow)
        
        self.main_layout.addWidget(market_container)

    def create_market_card(self, parent_layout, title, value, change, is_positive):
        """Create a market index card"""
        card = QFrame()
        card.setObjectName("market-card")
        
        # Layout for card
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setObjectName("gold-accent-text")
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("value-text")
        
        # Change
        change_label = QLabel(change)
        if is_positive:
            change_label.setStyleSheet("color: #66CFA6; font-size: 14px;")
        else:
            change_label.setStyleSheet("color: #F87171; font-size: 14px;")
        
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card_layout.addWidget(change_label)
        card_layout.addStretch()
        
        # Add subtle inner glow with gold tint
        card_shadow = QGraphicsDropShadowEffect(card)
        card_shadow.setBlurRadius(8)
        card_shadow.setColor(QColor(255, 215, 0, 20))
        card_shadow.setOffset(0, 0)
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
                    widget.setStyleSheet("color: #66CFA6; font-size: 16px; font-weight: bold;")
                else:
                    widget.setText(f"-${abs(total_unrealized_pl):,.2f}")
                    widget.setStyleSheet("color: #F87171; font-size: 16px; font-weight: bold;")
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
        headers = ["Symbol", "Company", "Qty", "Avg Buy Price", "Current Price", "Daily Change", "Market Value", "Unrealized P/L", "Allocation %"]
        self.stock_table.setColumnCount(len(headers))
        self.stock_table.setHorizontalHeaderLabels(headers)
        self.stock_table.setRowCount(len(portfolio_data))
        for row, data in enumerate(portfolio_data):
            # נעבור על כל עמודה לפי סדר הנתונים
            symbol_item = QTableWidgetItem(data["symbol"])
            company_item = QTableWidgetItem(data["company_name"] if data["company_name"] else "-")
            qty_item = QTableWidgetItem(str(data["quantity"]))
            avg_price_item = QTableWidgetItem(f"${data['avg_buy_price']:.2f}")
            current_price_item = QTableWidgetItem(f"${data['current_price']:.2f}")
            daily_change_val = data["daily_change"] if data["daily_change"] is not None else "-"
            daily_change_item = QTableWidgetItem(str(daily_change_val))
            market_value_item = QTableWidgetItem(f"${data['market_value']:.2f}")
            unrealized_pl_item = QTableWidgetItem(f"${data['unrealized_pl']:.2f}")
            allocation_item = QTableWidgetItem(f"{data['allocation']:.1f}%")
            
            # ניתן להוסיף עיצוב: למשל, אם unrealized_pl חיובי להציג בירוק, ואם שלילי באדום
            if data["unrealized_pl"] >= 0:
                unrealized_pl_item.setForeground(QColor("#66CFA6"))
            else:
                unrealized_pl_item.setForeground(QColor("#F87171"))
            
            # נניח daily_change_item יעוצב בדומה, אם ערך מספרי
            # (ניתן להוסיף לוגיקה נוספת כאן)
            
            items = [symbol_item, company_item, qty_item, avg_price_item, current_price_item, daily_change_item, market_value_item, unrealized_pl_item, allocation_item]
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                self.stock_table.setItem(row, col, item)
