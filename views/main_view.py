import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMenuBar, QStatusBar,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QComboBox, QMenu,
    QHeaderView, QFrame, QTabWidget, QGraphicsDropShadowEffect, QApplication, QScrollArea,
    QMessageBox, QSizePolicy
)
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Qt, QDate, QSize

from buy_order_view import BuyOrderWindow
from sell_order_view import SellOrderWindow
from ai_advisor_view import AIAdvisorWindow
from trade_history_view import TradeHistoryWindow

from presenters.main_presenter import MainPresenter


class MainView(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"SmartInvest Pro - {username}")

        # חיבור ה-Presenter
        self.presenter = MainPresenter(self)

        # 📌 קבלת גודל המסך והגדרת גודל החלון ביחס אליו
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(int(screen_size.width() * 0.85), int(screen_size.height() * 0.85))

        # 📌 עיצוב כללי
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background-color: #F0F5FF;
            }
            QLabel {
                color: #2C3E50;
            }
            QMenuBar {
                background-color: #2956B2;
                color: white;
                font-size: 15px;
                padding: 8px;
            }
            QMenuBar::item:selected {
                background-color: #3A6ED5;
            }
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #2956B2, stop:1 #4A7CE0);
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton {
                font-size: 15px;
                font-weight: bold;
                border-radius: 6px;
                padding: 12px;
                min-width: 160px;
                background-color: #2956B2;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #3A6ED5;
            }
            QTableWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 14px;
                background-color: #F2F4F6;
                border: 1px solid #CCD1D9;
                border-radius: 5px;
                gridline-color: #E0E6ED;
            }
            QHeaderView::section {
                background-color: #2956B2;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        # 🔹 **יצירת תפריט עליון**
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

        # 🔹 **פריסה ראשית**
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 🔹 **כותרת ראשית**
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #2956B2, stop:1 #4A7CE0);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        header_layout = QVBoxLayout(self.header_frame)

        self.label = QLabel("Welcome, Loading...")  # יעדכן שם משתמש דרך ה-Presenter
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

        outer_layout = QHBoxLayout()
        outer_layout.addWidget(container)

        central_widget = QWidget()
        central_widget.setLayout(outer_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(central_widget)
        self.setCentralWidget(self.scroll_area)

        # 🔹 **סטטוס בר**
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Loading...")

        # 🔹 **טעינת נתונים**
        self.presenter.load_user_data()
        self.presenter.load_portfolio_data()

    def create_buttons(self):
        """ יוצר אזור כפתורים נוח לשימוש """
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(20)

        self.btn_buy_order = QPushButton("📈 Buy Order")
        self.btn_buy_order.clicked.connect(self.presenter.open_buy_order)

        self.btn_sell_order = QPushButton("📉 Sell Order")
        self.btn_sell_order.clicked.connect(self.presenter.open_sell_order)

        self.btn_ai_advisor = QPushButton("🤖 AI Advisor")
        self.btn_ai_advisor.clicked.connect(self.presenter.open_ai_advisor)

        self.btn_trade_history = QPushButton("📊 Trade History")
        self.btn_trade_history.clicked.connect(self.presenter.open_trade_history)

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
        portfolio_layout.setContentsMargins(5, 5, 5, 5)

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels(["Stock", "Current Price", "Daily Change", "Quantity", "Portfolio Value"])
        self.stock_table.setAlternatingRowColors(True)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.verticalHeader().setVisible(False)

        portfolio_layout.addWidget(self.stock_table)
        self.tabs.addTab(portfolio_tab, "Portfolio")
        self.main_layout.addWidget(self.tabs)

    def update_header(self, text):
        """ מעדכן את הכותרת הראשית """
        self.label.setText(text)

    def update_status_bar(self, message):
        """ מעדכן את הסטטוס בר עם מידע חדש """
        self.status_bar.showMessage(message)
        
    def update_portfolio_table(self, portfolio_data):
        """ מעדכן את הטבלה עם הנתונים החדשים """
        self.stock_table.setRowCount(len(portfolio_data))
        for row, stock_data in enumerate(portfolio_data):
            for col, value in enumerate(stock_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.stock_table.setItem(row, col, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainView("John Doe")
    window.show()
    sys.exit(app.exec())
