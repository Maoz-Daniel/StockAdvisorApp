from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QLineEdit, QSpinBox, QComboBox, QApplication,
    QScrollArea, QSizePolicy, QHBoxLayout, QStatusBar, QMessageBox, QDialog
)
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QColor, QFont
from presenters.buy_order_presenter import BuyOrderPresenter

class OrderPreviewDialog(QDialog):
    """Dialog to preview order details before confirming"""
    def __init__(self, preview_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Order Preview")
        self.resize(400, 300)
        
        # Apply dark theme styling
        self.setStyleSheet("""
            QDialog {
                background-color: #112240;
                color: #E8E8E8;
                font-family: 'Segoe UI', 'Roboto', 'Open Sans', sans-serif;
            }
            QLabel {
                color: #E8E8E8;
                font-size: 14px;
            }
            QFrame {
                background-color: #1E3A5F;
                border-radius: 8px;
                border: 1px solid #2C5A8C;
            }
            QPushButton {
                background-color: #1E3A5F;
                color: #E8E8E8;
                border: 1px solid #2C5A8C;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2C5A8C;
                color: #78BEFF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Order Preview")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #78BEFF;")
        layout.addWidget(header)
        
        # Order details
        details = QFrame()
        details.setObjectName("gold-card")
        details.setStyleSheet("""
            background-color: rgba(44, 90, 140, 0.3);
            border-radius: 8px;
            border: 1px solid #FFE866;
            border-left: 3px solid #FFE866;
            padding: 15px;
        """)
        details_layout = QVBoxLayout(details)
        
        stock_label = QLabel(f"Stock: {preview_info['stock']}")
        quantity_label = QLabel(f"Quantity: {preview_info['quantity']}")
        price_label = QLabel(f"Price per share: ${preview_info['price_per_share']:.2f}")
        order_type_label = QLabel(f"Order type: {preview_info['order_type']}")
        subtotal_label = QLabel(f"Subtotal: ${preview_info['estimated_total']:.2f}")
        commission_label = QLabel(f"Commission: ${preview_info['commission']:.2f}")
        
        total_label = QLabel(f"Total: ${preview_info['total_with_commission']:.2f}")
        total_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #FFE866;")
        
        details_layout.addWidget(stock_label)
        details_layout.addWidget(quantity_label)
        details_layout.addWidget(price_label)
        details_layout.addWidget(order_type_label)
        details_layout.addWidget(subtotal_label)
        details_layout.addWidget(commission_label)
        details_layout.addWidget(total_label)
        
        layout.addWidget(details)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        confirm_button = QPushButton("Confirm Order")
        confirm_button.setObjectName("gold-button")
        confirm_button.setStyleSheet("""
            background-color: #1E3A5F;
            color: #FFE866;
            border: 1px solid #FFE866;
            border-left: 3px solid #FFD700;
            border-right: 3px solid #FFD700;
        """)
        confirm_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(confirm_button)
        layout.addLayout(buttons_layout)

class BuyOrderWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("Buy Order - SmartInvest Pro")
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
            
            /* Portfolio section */
            QFrame#portfolio-frame {
                background-color: rgba(44, 90, 140, 0.3);
                border-radius: 8px;
                border: 1px solid rgba(120, 190, 255, 0.2);
                border-top: 2px solid #FFE866;
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

        title_label = QLabel("📈 Buy Order")
        title_label.setObjectName("welcome-label")
        title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle-label")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **תיבה להזנת פרטי קנייה**
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
        self.price_input.setPlaceholderText("Enter price per unit")
        price_row = create_form_row("Set Buy Price ($):", self.price_input)
        
        # הוספת שדה נוסף לסוג הזמנה
        self.order_type_combo = QComboBox()
        self.order_type_combo.addItems(["Market Order", "Limit Order", "Stop Order", "Stop-Limit Order"])
        order_type_row = create_form_row("Order Type:", self.order_type_combo)
        
        # הוספת השורות לטופס
        form_layout.addWidget(stock_row)
        form_layout.addWidget(quantity_row)
        form_layout.addWidget(price_row)
        form_layout.addWidget(order_type_row)
        
        # Portfolio summary section
        portfolio_section = QFrame()
        portfolio_section.setObjectName("portfolio-frame")
        portfolio_layout = QVBoxLayout(portfolio_section)
        
        portfolio_title = QLabel("Portfolio Summary")
        portfolio_title.setObjectName("section-title")
        
        self.portfolio_value = QLabel("Total Value: $0.00")
        self.portfolio_value.setStyleSheet("color: #66CFA6; font-weight: bold;")
        
        portfolio_layout.addWidget(portfolio_title)
        portfolio_layout.addWidget(self.portfolio_value)
        
        form_layout.addWidget(portfolio_section)
        
        # הוספת מרווח אוטומטי בתחתית הטופס
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addWidget(spacer)
        
        self.main_layout.addWidget(self.form_frame)

        # 🔹 **כפתורי פעולה**
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        self.preview_button = QPushButton("👁️ Preview Order")
        self.preview_button.setCursor(Qt.PointingHandCursor)
        self.preview_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.preview_button.clicked.connect(self.preview_order)
        
        self.buy_button = QPushButton("✅ Confirm Buy Order")
        self.buy_button.setObjectName("gold-button")
        self.buy_button.setCursor(Qt.PointingHandCursor)
        self.buy_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.buy_button.clicked.connect(self.confirm_buy)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addSpacing(15)
        buttons_layout.addWidget(self.buy_button)
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
        
        # Initialize presenter
        self.presenter = BuyOrderPresenter(self, self.model)

    def update_user_info(self, username):
        """Update username in the UI"""
        self.subtitle_label.setText(f"Manage your buy orders - {username}")
        self.status_bar.showMessage(
            f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30"
        )
        
        # Update portfolio value
        total_value = sum(stock["price"] * stock["quantity"] for stock in self.model.portfolio.values())
        self.portfolio_value.setText(f"Total Value: ${total_value:.2f}")

    def update_stock_list(self, stocks):
        """Update the stock dropdown with available stocks"""
        self.stock_combo.clear()
        self.stock_combo.addItems(stocks)

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

    def display_order_preview(self, preview_info):
        """Display order preview dialog"""
        preview_dialog = OrderPreviewDialog(preview_info, self)
        return preview_dialog.exec()

    def preview_order(self):
        """Preview the buy order"""
        stock = self.stock_combo.currentText()
        quantity = self.quantity_input.value()
        price = self.price_input.text() if self.price_input.text() else "Market Price"
        order_type = self.order_type_combo.currentText()
        
        self.presenter.preview_order(stock, quantity, price, order_type)

    def confirm_buy(self):
        """Execute the buy order"""
        stock = self.stock_combo.currentText()
        quantity = self.quantity_input.value()
        price = self.price_input.text() if self.price_input.text() else "Market Price"
        order_type = self.order_type_combo.currentText()
        
        success = self.presenter.process_buy_order(stock, quantity, price, order_type)
        if success:
            self.close()