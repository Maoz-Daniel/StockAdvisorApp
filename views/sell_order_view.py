# sell_order_view.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QLineEdit, QSpinBox, QComboBox, QApplication,
    QScrollArea, QSizePolicy, QHBoxLayout, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QColor, QFont
from presenters.sell_order_presenter import SellOrderPresenter

class SellOrderWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("Sell Order - SmartInvest Pro")
        self.resize(900, 650)

        # 📌 Apply luxury dark theme styling
        self.setStyleSheet("""
            /* Main window and backgrounds */
            QMainWindow, QWidget {
                font-family: 'Segoe UI', 'Roboto', 'Open Sans', sans-serif;
                background-color: #112240;
                color: #E8E8E8;
            }
            
            /* Header styling */
            QFrame#header-frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                             stop:0 #112240, stop:1 #1E3A5F);
                border-radius: 10px;
                padding: 20px;
                min-height: 120px;
                border: 1px solid #2C5A8C;
                border-bottom: 2px solid #FFE866;
            }
            
            /* Card frames */
            QFrame {
                background-color: #1E3A5F;
                border-radius: 8px;
                border: 1px solid #2C5A8C;
            }
            
            /* Labels */
            QLabel {
                color: #E8E8E8;
                font-size: 14px;
            }
            
            QLabel#welcome-label {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
                letter-spacing: 0.5px;
            }
            
            QLabel#subtitle-label {
                color: #C0C0C0;
                font-size: 15px;
                font-weight: normal;
            }
            
            QLabel#section-title {
                font-size: 18px;
                font-weight: bold;
                color: #78BEFF;
                margin-top: 10px;
                margin-bottom: 5px;
                border-left: 3px solid #FFE866;
                padding-left: 10px;
            }
            
            /* Action Buttons */
            QPushButton {
                background-color: #1E3A5F;
                color: #E8E8E8;
                border: 1px solid #2C5A8C;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
                min-width: 160px;
                min-height: 45px;
            }
            
            QPushButton:hover {
                background-color: #2C5A8C;
                color: #78BEFF;
            }
            
            QPushButton:pressed {
                background-color: #112240;
                border: 1px solid #78BEFF;
            }
            
            QPushButton#gold-button {
                background-color: #1E3A5F;
                color: #FFE866;
                border: 1px solid #FFE866;
                border-left: 3px solid #FFD700;
                border-right: 3px solid #FFD700;
            }
            
            QPushButton#gold-button:hover {
                background-color: rgba(255, 232, 102, 0.1);
                color: #FFD700;
            }
            
            /* Form inputs */
            QLineEdit, QSpinBox, QComboBox {
                background-color: #1E3A5F;
                color: #E8E8E8;
                border: 1px solid #2C5A8C;
                border-radius: 6px;
                padding: 8px;
                min-height: 38px;
                font-size: 14px;
            }
            
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #78BEFF;
            }
            
            /* Status bar */
            QStatusBar {
                background-color: #112240;
                color: #C0C0C0;
                padding: 8px;
                font-size: 13px;
                border-top: 1px solid #2C5A8C;
            }
            
            /* Scroll Area */
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                background: #112240;
                width: 10px;
                margin: 0;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: #2C5A8C;
                min-height: 30px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #78BEFF;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            
            /* Holdings section */
            QFrame#holdings-frame {
                background-color: rgba(44, 90, 140, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(120, 190, 255, 0.2);
                border-left: 2px solid #FFE866;
                padding: 15px;
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
        self.header_frame.setObjectName("header-frame")
        self.header_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.header_frame.setMinimumHeight(140)
        
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel("📉 Sell Order")
        title_label.setObjectName("welcome-label")
        title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle-label")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **תיבה להזנת פרטי מכירה**
        self.form_frame = QFrame()
        self.form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(20, 20, 20, 20)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # מכיל לייבל ושדה קלט
        def create_form_row(label_text, input_widget):
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            # continued from previous code for the SellOrderWindow class

            label = QLabel(label_text)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            
            return row_widget

        # יצירת רכיבי הטופס
        self.stock_combo = QComboBox()
        stock_row = create_form_row("Select Stock:", self.stock_combo)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)
        quantity_row = create_form_row("Enter Quantity:", self.quantity_input)
        
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price per unit or leave empty for market price")
        price_row = create_form_row("Set Selling Price ($):", self.price_input)
        
        # הוספת השורות לטופס
        form_layout.addWidget(stock_row)
        form_layout.addWidget(quantity_row)
        form_layout.addWidget(price_row)
        
        # Add holdings information section
        holdings_section = QFrame()
        holdings_section.setObjectName("holdings-frame")
        holdings_layout = QVBoxLayout(holdings_section)
        
        holdings_title = QLabel("Your Holdings")
        holdings_title.setObjectName("section-title")
        
        self.selected_stock_info = QLabel("Select a stock to see your holdings")
        
        self.potential_value = QLabel("Potential sale value: $0.00")
        self.potential_value.setStyleSheet("color: #66CFA6; font-weight: bold;")
        
        holdings_layout.addWidget(holdings_title)
        holdings_layout.addWidget(self.selected_stock_info)
        holdings_layout.addWidget(self.potential_value)
        
        form_layout.addWidget(holdings_section)
        
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
        self.sell_button.setObjectName("gold-button")
        self.sell_button.setCursor(Qt.PointingHandCursor)
        self.sell_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sell_button.clicked.connect(self.confirm_sell)
        
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
        

        self.presenter = SellOrderPresenter(self, self.model)
        self.presenter.initialize()
        self.stock_combo.currentTextChanged.connect(self.on_stock_selected)

        if self.stock_combo.count() > 0:
         self.on_stock_selected(self.stock_combo.currentText())


    def update_user_info(self, username):
        """Update username in the UI"""
        self.subtitle_label.setText(f"Manage your sell orders - {username}")
        self.status_bar.showMessage(
            f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30"
        )

    def update_stock_list(self, stocks):
        """Update the stock dropdown with owned stocks"""
        self.stock_combo.clear()
        self.stock_combo.addItems(stocks)
        
        # Update selected stock info if any stocks are available
        if stocks:
            self.on_stock_selected(stocks[0])

    def update_quantity_max(self, max_quantity):
        """Update the maximum quantity that can be sold"""
        if max_quantity > 0:
            self.quantity_input.setRange(1, max_quantity)
            self.quantity_input.setEnabled(True)
            self.sell_button.setEnabled(True)
        else:
            self.quantity_input.setValue(0)
            self.quantity_input.setEnabled(False)
            self.sell_button.setEnabled(False)

    def update_price_placeholder(self, text):
        """Update the price input placeholder"""
        self.price_input.setPlaceholderText(text)
        
        # Also update the selected stock info
        if self.stock_combo.currentText() in self.model.portfolio:
            stock = self.stock_combo.currentText()
            quantity = self.model.portfolio[stock]["quantity"]
            price = self.model.portfolio[stock]["price"]
            total_value = quantity * price
            
            self.selected_stock_info.setText(f"You own {quantity} shares of {stock} at ${price:.2f} per share")
            self.potential_value.setText(f"Potential sale value: ${total_value:.2f}")
        else:
            self.selected_stock_info.setText("Select a stock to see your holdings")
            self.potential_value.setText("Potential sale value: $0.00")

    def show_success_message(self, message):
        """Display success message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()

    def show_error_message(self, message):
        """Display error message"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()

    def on_stock_selected(self, stock):
        """Handle stock selection"""
        self.presenter.on_stock_selected(stock)

    def confirm_sell(self):
        """Execute the sell order"""
        stock = self.stock_combo.currentText()
        quantity = self.quantity_input.value()
        price = self.price_input.text() if self.price_input.text() else "Market Price"
        
        success = self.presenter.process_sell_order(stock, quantity, price)
        if success:
            self.close()