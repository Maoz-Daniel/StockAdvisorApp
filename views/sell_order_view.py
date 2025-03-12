from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QLineEdit, QSpinBox, QComboBox, QApplication,
    QScrollArea, QSizePolicy, QHBoxLayout, QStatusBar
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QColor, QFont

class SellOrderWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Sell Order - SmartInvest Pro")
        self.resize(900, 650)

        # 📌 עיצוב כללי
        self.setStyleSheet("""
            QMainWindow, QWidget {
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background-color: #F0F5FF;
            }
            QLabel {
                color: #2C3E50;
                font-size: 22px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2956B2;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                border: none;
                font-size: 16px;
                min-height: 48px;
                max-width: 300px;
            }
            QPushButton:hover {
                background-color: #3A6ED5;
            }
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #D0E1FF;
            }
            QLineEdit, QSpinBox, QComboBox {
                background-color: white;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 8px;
                min-height: 38px;
                font-size: 14px;
                color: #334155;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #2956B2;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #F0F5FF;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #B8C9E6;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #97B0D9;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # 🔹 **יצירת ממשק מרכזי עם תמיכה בגלילה**
        central_widget = QWidget()
        main_container_layout = QVBoxLayout(central_widget)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)
        
        # יצירת ScrollArea לתמיכה בגלילה
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # יצירת widget פנימי לתוכן הגלילה
        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        # 🔹 **תיבה עליונה עם כותרת (Header)**
        self.header_frame = QFrame()
        self.header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header_frame.setMinimumHeight(140)
        self.header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2956B2, stop:1 #4A7CE0);
                border-radius: 12px;
                border: none;
                padding: 5px;
            }
        """)
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel("📉 Sell Order")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")

        subtitle_label = QLabel(f"Manage your sell orders - {self.username}")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 16px; color: rgba(255, 255, 255, 0.8);")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **תיבה להזנת פרטי מכירה**
        self.form_frame = QFrame()
        self.form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(20, 20, 20, 20)

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

        # מכיל לייבל ושדה קלט
        def create_form_row(label_text, input_widget):
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            
            label = QLabel(label_text)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            
            return row_widget

        # יצירת רכיבי הטופס
        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"])
        stock_row = create_form_row("Select Stock:", self.stock_combo)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)
        quantity_row = create_form_row("Enter Quantity:", self.quantity_input)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price per unit")
        price_row = create_form_row("Set Selling Price ($):", self.price_input)
        
        # הוספת השורות לטופס
        form_layout.addWidget(stock_row)
        form_layout.addWidget(quantity_row)
        form_layout.addWidget(price_row)
        
        # הוספת מרווח אוטומטי בתחתית הטופס
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addWidget(spacer)
        
        self.main_layout.addWidget(self.form_frame)

        # 🔹 **כפתור ביצוע מכירה**
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        self.sell_button = QPushButton("✅ Confirm Sell Order")
        self.sell_button.setCursor(Qt.PointingHandCursor)
        self.sell_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sell_button.clicked.connect(self.process_sell_order)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.sell_button)
        buttons_layout.addStretch()
        
        self.main_layout.addWidget(buttons_container)
        
        # הוספת מרווח בתחתית המסך
        bottom_spacer = QWidget()
        bottom_spacer.setMinimumHeight(20)
        self.main_layout.addWidget(bottom_spacer)

        # סידור ScrollArea והתוכן שלו
        scroll_area.setWidget(scroll_content)
        main_container_layout.addWidget(scroll_area)
        
        self.setCentralWidget(central_widget)

    def process_sell_order(self):
        """ תהליך אישור מכירת מניות """
        stock = self.stock_combo.currentText()
        quantity = self.quantity_input.value()
        price = self.price_input.text()

        if not price:
            price = "Market Price"
        
        confirmation_msg = f"📉 You are selling {quantity} shares of {stock} at {price} per unit."
        print(confirmation_msg)  # ✅ להדפסה למסוף (אפשר לשדרג עם QMessageBox)
        
    # אירוע שינוי גודל - מעדכן את הממשק בהתאם לגודל החדש
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # אפשר להוסיף כאן לוגיקה נוספת בעת שינוי גודל החלון

# ✅ **הרצת החלון**
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SellOrderWindow("John Doe")
    window.show()

    # תמיכה ב-High DPI
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    sys.exit(app.exec())