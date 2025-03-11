from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMenuBar, QStatusBar,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QMenu,
    QHeaderView, QFrame, QTabWidget, QGraphicsDropShadowEffect, QApplication, QScrollArea,
    QMessageBox
)
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Qt, QDate, QSize

from buy_order_view import BuyOrderWindow
from sell_order_view import SellOrderWindow
from ai_advisor_view import AIAdvisorWindow
from trade_history_view import TradeHistoryWindow


class MainView(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"SmartInvest Pro - {username}")

        # 📌 קבלת גודל המסך והגדרת גודל החלון ביחס אליו
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        print(f"🔹 Screen size detected: Width = {screen_size.width()}, Height = {screen_size.height()}")

        # קביעת גודל חלון דינמי – 85% מרוחב המסך ו-85% מהגובה
        self.resize(int(screen_size.width() * 0.85), int(screen_size.height() * 0.85))

        # 📌 עיצוב כללי עם הכחולים החדשים (gradient #2956B2-#4A7CE0, כפתורים #2956B2→#3A6ED5 וכו')
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                /* רקע כללי נשאר כמו במקור - אפור בהיר (#D0D4DA). אם תרצה להחליף ל-F0F5FF, אפשר. */
                background-color: #F0F5FF;
            }
            QLabel {
                color: #2C3E50;
            }

            /* סטטוס-בר עם גרדיאנט בכחול כהה */
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #2956B2, stop:1 #4A7CE0);
                color: white;
                padding: 8px;
                font-size: 14px;
            }

            /* כפתורים בכחול #2956B2, ועובר ל-#3A6ED5 בהובר */
            QPushButton {
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
                padding: 12px;
                min-width: 160px;
                background-color: #2956B2; /* במקום #2C82D5 */
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #3A6ED5; /* במקום #2371BA */
            }

            /* טבלת מניות */
            QTableWidget {
                background-color: #F2F4F6;
                alternate-background-color: #E9ECF0;
                border: 1px solid #CCD1D9;
                border-radius: 5px;
                gridline-color: #E0E6ED;
                selection-background-color: #D0E8F2;
                selection-color: #2C3E50;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #D0E8F2;
            }

            /* כותרות העמודות בכחול #2956B2 */
            QHeaderView::section {
                background-color: #2956B2;  /* במקום #1F3B73 */
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            /* מסגרת הטאבים בכחול כהה (#2956B2), רקע הטאב */
            QTabWidget::pane {
                border: 1px solid #2956B2;  /* במקום #1F3B73 */
                border-radius: 5px;
                background-color: #F2F4F6;
            }
            QTabBar::tab {
                background-color: #E9ECF0;
                border: 1px solid #CCD1D9;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 10px 20px;
                margin-right: 2px;
                color: #2C3E50;
            }
            QTabBar::tab:selected {
                background-color: #F2F4F6;
                border-bottom: 2px solid #2956B2; /* במקום #1F3B73 */
                font-weight: bold;
            }
        """)

        # 🔹 **יצירת תפריט עליון (MenuBar)**
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.file_menu = QMenu("Main Menu", self)
        self.menu_bar.addMenu(self.file_menu)

        self.dashboard_action = QAction("Dashboard", self)
        self.portfolio_action = QAction("My Portfolio", self)
        self.market_action = QAction("Market Overview", self)
        self.reports_action = QAction("Reports & Analysis", self)
        self.settings_action = QAction("Account Settings", self)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        self.file_menu.addAction(self.dashboard_action)
        self.file_menu.addAction(self.portfolio_action)
        self.file_menu.addAction(self.market_action)
        self.file_menu.addAction(self.reports_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addAction(self.exit_action)

        # תפריט Tools
        self.tools_menu = QMenu("Tools", self)
        self.menu_bar.addMenu(self.tools_menu)
        self.analyzer_action = QAction("Stock Analyzer", self)
        self.calculator_action = QAction("Investment Calculator", self)
        self.alerts_action = QAction("Price Alerts", self)
        self.tools_menu.addAction(self.analyzer_action)
        self.tools_menu.addAction(self.calculator_action)
        self.tools_menu.addAction(self.alerts_action)

        # תפריט Help
        self.help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(self.help_menu)
        self.guide_action = QAction("User Guide", self)
        self.contact_action = QAction("Contact Us", self)
        self.help_menu.addAction(self.guide_action)
        self.help_menu.addAction(self.contact_action)

        # 🔹 **פריסה ראשית**
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 🔹 **כותרת ראשית (header)**
        self.header_frame = QFrame()
        # במקום צבע אחיד (#1F3B73) – נעשה גרדיאנט (אם תרצה אפשר להשאיר אחיד):
        self.header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #2956B2, stop:1 #4A7CE0);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(self.header_frame)

        self.label = QLabel(f"Welcome, {self.username}!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")

        header_layout.addWidget(self.label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **אזור כפתורים**
        self.create_buttons()

        # 🔹 **טבלה ותוכן נוסף**
        self.create_tabs()

        # 🔹 **התאמה לגודל דינמי וגלילה**
        container = QWidget()
        container.setLayout(self.main_layout)
        container.setMaximumWidth(1200)

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addWidget(container)
        outer_layout.addStretch()

        central_widget = QWidget()
        central_widget.setLayout(outer_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(central_widget)
        self.setCentralWidget(self.scroll_area)

        # 🔹 **סטטוס בר** (עכשיו עם גרדיאנט)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #2956B2, stop:1 #4A7CE0);
                color: white;
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.status_bar.showMessage(
            f"Logged in as: {self.username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30"
        )

    def create_buttons(self):
        """ יוצר אזור כפתורים נוח לשימוש """
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #F2F4F6;
                border-radius: 10px;
                padding: 20px;
                border: 2px solid #2956B2; /* במקום #1F3B73 */
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)

        self.btn_buy_order = QPushButton("📈 Buy Order")
        self.btn_buy_order.setToolTip("Place a buy order")
        self.btn_buy_order.clicked.connect(self.open_buy_order)

        self.btn_sell_order = QPushButton("📉 Sell Order")
        self.btn_sell_order.setToolTip("Place a sell order")
        self.btn_sell_order.clicked.connect(self.open_sell_order)

        self.btn_ai_advisor = QPushButton("🤖 AI Advisor")
        self.btn_ai_advisor.setToolTip("Get AI-powered investment advice")
        self.btn_ai_advisor.clicked.connect(self.open_ai_advisor)

        self.btn_trade_history = QPushButton("📊 Trade History")
        self.btn_trade_history.setToolTip("View trade history")
        self.btn_trade_history.clicked.connect(self.open_trade_history)

        button_layout.addWidget(self.btn_buy_order)
        button_layout.addWidget(self.btn_sell_order)
        button_layout.addWidget(self.btn_ai_advisor)
        button_layout.addWidget(self.btn_trade_history)

        self.main_layout.addWidget(button_frame)

    def create_tabs(self):
        """ יוצר טאבים דינמיים עם טבלה """
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("font-size: 15px;")

        portfolio_tab = QWidget()
        portfolio_layout = QVBoxLayout(portfolio_tab)
        portfolio_layout.setContentsMargins(20, 20, 20, 20)

        portfolio_header = QLabel("My Portfolio")
        portfolio_header.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        portfolio_header.setAlignment(Qt.AlignCenter)
        portfolio_layout.addWidget(portfolio_header)

        self.stock_table = QTableWidget()
        self.stock_table.setRowCount(5)
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels(["Stock", "Current Price", "Daily Change", "Quantity", "Portfolio Value"])
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.verticalHeader().setVisible(False)

        stocks_data = [
            ("AAPL", "$182.30", "+1.2%", "35", "$6,380.50"),
            ("GOOGL", "$2,835.55", "-0.3%", "5", "$14,177.75"),
            ("MSFT", "$419.20", "+0.8%", "10", "$4,192.00"),
            ("TSLA", "$167.50", "+2.1%", "12", "$2,010.00"),
            ("AMZN", "$183.80", "+0.6%", "8", "$1,470.40")
        ]

        for row, (stock, price, change, quantity, value) in enumerate(stocks_data):
            self.stock_table.setItem(row, 0, QTableWidgetItem(stock))

            price_item = QTableWidgetItem(price)
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.stock_table.setItem(row, 1, price_item)

            change_item = QTableWidgetItem(change)
            change_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if "+" in change:
                change_item.setForeground(QColor("#00B894"))
            else:
                change_item.setForeground(QColor("#E74C3C"))
            self.stock_table.setItem(row, 2, change_item)

            quantity_item = QTableWidgetItem(quantity)
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.stock_table.setItem(row, 3, quantity_item)

            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.stock_table.setItem(row, 4, value_item)

        portfolio_layout.addWidget(self.stock_table)
        self.tabs.addTab(portfolio_tab, "Portfolio")

        self.main_layout.addWidget(self.tabs)

    # 🔻 פונקציות שמופעלות כשלוחצים על הכפתורים 🔻
    def open_buy_order(self):
        self.buy_order_window = BuyOrderWindow(self.username)
        self.buy_order_window.show()

    def open_sell_order(self):
        self.sell_order_window = SellOrderWindow(self.username)
        self.sell_order_window.show()

    def open_ai_advisor(self):
        self.ai_advisor_window = AIAdvisorWindow(self.username)
        self.ai_advisor_window.show()

    def open_trade_history(self):
        self.trade_history_window = TradeHistoryWindow(self.username)
        self.trade_history_window.show()


# ✅ **הרצת החלון לצורך בדיקה**
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainView("John Doe")
    window.show()
    sys.exit(app.exec())
