# sell_order_view.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class SellOrderWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Sell Order - SmartInvest Pro")
        self.resize(800, 600)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background-color: #D0D4DA;
            }
            QLabel {
                color: #2C3E50;
                font-size: 24px;
            }
        """)
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        info_label = QLabel("Sell Order Interface (Demo Data)")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        # הוסף כאן את שדות המסך לפי הצורך
        self.setCentralWidget(central_widget)
