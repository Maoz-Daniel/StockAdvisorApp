from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QLineEdit, QSpinBox, QComboBox, QApplication,
    QScrollArea, QSizePolicy, QHBoxLayout, QStatusBar, QMessageBox, QDialog,
    QCompleter, QProgressBar, QTextEdit, QListWidget, QListWidgetItem,QMenu
)
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QSize, QDate, QMargins, QDateTime, QTimer,QByteArray
from PySide6.QtGui import QColor, QFont, QPainter, QPen,QIcon, QPixmap, QPainter, QFont, QPen, QColor
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
# Import the FaceID6 theme
from assets.theme import FaceID6Theme
from assets.theme import LuxuryTheme
from assets.theme import DarkLuxuryTheme

from presenters.sell_order_presenter import SellOrderPresenter

class OrderPreviewDialog(QDialog):
    """Dialog to preview order details before confirming"""
    def __init__(self, preview_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sell Order Preview")
        self.resize(400, 300)
        
        # Apply FaceID6 theme styling
        self.setStyleSheet(FaceID6Theme.STYLE_SHEET)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Sell Order Preview")
        header.setObjectName("section-title")
        layout.addWidget(header)
        
        # Order details
        details = QFrame()
        details.setObjectName("order-summary")
        details_layout = QVBoxLayout(details)
        
        stock_label = QLabel(f"Stock: {preview_info['stock']}")
        quantity_label = QLabel(f"Quantity to Sell: {preview_info['quantity']}")
        price_label = QLabel(f"Current Price per share: ${preview_info['price_per_share']:.2f}")
        total_label = QLabel(f"Total Value: ${preview_info['estimated_total']:.2f}")
        commission_label = QLabel(f"Commission Fee: ${preview_info['commission']:.2f}")
        net_value_label = QLabel(f"Net Proceeds: ${preview_info['total_after_commission']:.2f}")
        remaining_label = QLabel(f"Shares Remaining After Sale: {preview_info['shares_remaining']}")
        
        total_label.setObjectName("value-text")
        net_value_label.setObjectName("value-text")
        
        details_layout.addWidget(stock_label)
        details_layout.addWidget(quantity_label)
        details_layout.addWidget(price_label)
        details_layout.addWidget(total_label)
        details_layout.addWidget(commission_label)
        details_layout.addWidget(net_value_label)
        details_layout.addWidget(remaining_label)
        
        layout.addWidget(details)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        confirm_button = QPushButton("Confirm Sale")
        confirm_button.setObjectName("highlight-button")
        confirm_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(confirm_button)
        layout.addLayout(buttons_layout)

class SellOrderWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("Sell Stock - SmartInvest Pro")
        self.resize(900, 800)

        # Apply FaceID6 theme styling
        self.setStyleSheet(FaceID6Theme.STYLE_SHEET)
        
        self.showFullScreen()

        # Main structure with scrolling support
        central_widget = QWidget()
        main_container_layout = QVBoxLayout(central_widget)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)

        # Create and add header bar
        header_bar = self.create_header_bar()
        main_container_layout.addWidget(header_bar)
        
        # Create ScrollArea for scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Create inner widget for scroll content
        scroll_content = QWidget()
        self.main_layout = QVBoxLayout(scroll_content)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignTop)
        
        # Header section
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
        
        # Portfolio section
        portfolio_section = QFrame()
        portfolio_section.setObjectName("card")
        portfolio_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        portfolio_layout = QVBoxLayout(portfolio_section)
        
        portfolio_title = QLabel("Your Portfolio")
        portfolio_title.setObjectName("section-title")
        portfolio_layout.addWidget(portfolio_title)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        portfolio_layout.addWidget(self.progress_bar)
        
        # Portfolio List
        self.portfolio_list = QListWidget()
        self.portfolio_list.setMinimumHeight(200)
        self.portfolio_list.currentItemChanged.connect(self.on_portfolio_item_selected)
        portfolio_layout.addWidget(self.portfolio_list)
        
        # Error and success messages
        self.error_message = QLabel("")
        self.error_message.setObjectName("error-message")
        self.error_message.setVisible(False)
        portfolio_layout.addWidget(self.error_message)
        
        self.success_message = QLabel("")
        self.success_message.setObjectName("success-message")
        self.success_message.setVisible(False)
        portfolio_layout.addWidget(self.success_message)
        
        self.main_layout.addWidget(portfolio_section)
        
        # Chart section
        chart_section = QFrame()
        chart_section.setObjectName("card")
        chart_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart_layout = QVBoxLayout(chart_section)
        
        chart_title = QLabel("Stock Price History (52 Weeks)")
        chart_title.setObjectName("section-title")
        
        self.chart_view = QChartView()
        self.chart_view.setMinimumHeight(300)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setObjectName("chart-container")
        
        # Setup empty chart
        empty_chart = QChart()
        empty_chart.setTitle("No Stock Selected")
        empty_chart.setBackgroundVisible(False)
        empty_chart.setTitleFont(QFont("SF Pro Display", 12, QFont.Bold))
        empty_chart.setTitleBrush(QColor(FaceID6Theme.PRIMARY_COLOR))
        self.chart_view.setChart(empty_chart)
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.chart_view)
        
        self.current_price_label = QLabel("Current Price: $0.00")
        self.current_price_label.setAlignment(Qt.AlignCenter)
        self.current_price_label.setObjectName("accent-text")
        chart_layout.addWidget(self.current_price_label)
        
        self.main_layout.addWidget(chart_section)

        # Sell order form section
        self.form_frame = QFrame()
        self.form_frame.setObjectName("card")
        self.form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # Form title
        form_title = QLabel("Sell Order Details")
        form_title.setObjectName("section-title")
        form_layout.addWidget(form_title)

        # Create a helper function for form rows
        def create_form_row(label_text, input_widget):
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            
            label = QLabel(label_text)
            label.setObjectName("accent-text")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            
            return row_widget

        # Form elements
        self.stock_display = QLabel("Selected Stock: None")
        self.stock_display.setObjectName("value-text")
        
        self.shares_owned_label = QLabel("Shares Owned: 0")
        self.shares_owned_label.setObjectName("accent-text")
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setObjectName("quantity-spinner")
        self.quantity_input.setRange(1, 1000)
        quantity_row = create_form_row("Enter Quantity to Sell:", self.quantity_input)
        
        # Stock price display (read-only)
        self.price_display = QLabel("Current Price: $0.00")
        self.price_display.setObjectName("accent-text")
        
        # Add all elements to form layout
        form_layout.addWidget(self.stock_display)
        form_layout.addWidget(self.shares_owned_label)
        form_layout.addWidget(quantity_row)
        form_layout.addWidget(self.price_display)
        
        self.main_layout.addWidget(self.form_frame)

        # Buttons section
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        self.preview_button = QPushButton("👁️ Preview Sale")
        self.preview_button.setCursor(Qt.PointingHandCursor)
        self.preview_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.preview_button.clicked.connect(self.preview_order)
        
        self.sell_button = QPushButton("✅ Confirm Sell Order")
        self.sell_button.setObjectName("highlight-button")
        self.sell_button.setCursor(Qt.PointingHandCursor)
        self.sell_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sell_button.clicked.connect(self.confirm_sell)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addSpacing(15)
        buttons_layout.addWidget(self.sell_button)
        buttons_layout.addStretch()
        
        self.main_layout.addWidget(buttons_container)
        
        # Add a spacer at the bottom
        bottom_spacer = QWidget()
        bottom_spacer.setMinimumHeight(20)
        self.main_layout.addWidget(bottom_spacer)

        # Set up scroll area and status bar
        scroll_area.setWidget(scroll_content)
        main_container_layout.addWidget(scroll_area)
        
        self.setCentralWidget(central_widget)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Initialize presenter
        self.presenter = SellOrderPresenter(self, self.model)
        
        # Initially disable sell buttons until a stock is selected
        self.preview_button.setEnabled(False)
        self.sell_button.setEnabled(False)
        
        # Setup loading animation timer
        self.loading_dots = 0
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_message)


    def create_header_bar(self):
        """Create a visible header bar with logo and navigation buttons"""
        # Create header frame
        header_frame = QFrame()
        header_frame.setObjectName("header-bar")
        header_frame.setFixedHeight(60)
        
        # Header layout
        header_layout = QHBoxLayout(header_frame)
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
        
        # App name (clickable)
        app_name = QPushButton("InvestPro")
        app_name.setStyleSheet("""
            QPushButton {
                color: white; 
                font-size: 20px; 
                font-weight: bold; 
                margin-left: 10px;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #E5E5EA;
            }
        """)
        app_name.setCursor(Qt.PointingHandCursor)
        app_name.clicked.connect(self.close)  # Close to return to home
        
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
                ("Dashboard", self.close),
                ("My Portfolio", self.close),
                ("Market Overview", self.close),
                ("Reports & Analysis", self.close),
                ("Account Settings", self.close),
                ("Exit", self.close)
            ]),
            ("Trading", [
                ("Buy Assets", self.close),
                ("Sell Assets", lambda: None),  # Already in Sell window, do nothing
                ("Order History", self.close)
            ]),
            ("Analytics", [
                ("Performance", self.close),
                ("Risk Analysis", self.close),
                ("AI Insights", self.close)
            ]),
            ("Help", [
                ("Documentation", self.close),
                ("Support", self.close),
                ("About", self.close)
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
        header_layout.addLayout(nav_layout)  # Add the navigation menu
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Overall frame styling - match the main window style
        header_frame.setStyleSheet(f"""
        QFrame#header-bar {{
            background-color: {FaceID6Theme.PRIMARY_COLOR};
            color: white;
        }}
    """)
        
        return header_frame

    def update_user_info(self, username):
        """Update username in the UI"""
        self.subtitle_label.setText(f"Manage your sell orders - {username}")
        self.status_bar.showMessage(
            f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30"
        )
    
    def update_portfolio_list(self, portfolio_data):
        """Update the portfolio list with user's stock holdings"""
        self.portfolio_list.clear()
        
        if not portfolio_data:
            # No stocks in portfolio
            no_stocks_item = QListWidgetItem("No stocks in your portfolio")
            no_stocks_item.setFlags(Qt.NoItemFlags)  # Make it non-selectable
            self.portfolio_list.addItem(no_stocks_item)
            return
        
        # Format and add each portfolio item
        for item in portfolio_data:
            symbol = item["symbol"]
            shares = item["shares"]
            price = item["current_price"]
            total_value = item["total_value"]
            
            # Create formatted display text
            display_text = f"{symbol} - {shares} shares | Current: ${price:.2f} | Value: ${total_value:.2f}"
            
            # Create and add list item
            list_item = QListWidgetItem(display_text)
            # Store the stock symbol and shares as data with the item
            list_item.setData(Qt.UserRole, {"symbol": symbol, "shares": shares})
            self.portfolio_list.addItem(list_item)
        
        self.status_bar.showMessage("Portfolio loaded successfully")
    
    def on_portfolio_item_selected(self, current, previous):
        """Handle portfolio item selection"""
        if not current:
            return
            
        # Get the stock data attached to the item
        stock_data = current.data(Qt.UserRole)
        if not stock_data:
            return
            
        symbol = stock_data["symbol"]
        shares = stock_data["shares"]
        
        # Update the quantity input's maximum value
        self.quantity_input.setMaximum(shares)
        self.quantity_input.setValue(1)  # Default to 1 share
        
        # Call the presenter to load the selected stock
        self.presenter.select_stock(symbol, shares)
    
    def update_shares_owned(self, shares):
        """Update the shares owned display"""
        self.shares_owned_label.setText(f"Shares Owned: {shares}")
        # Update the quantity spinner
        self.quantity_input.setMaximum(shares)
        if shares > 0:
            self.quantity_input.setEnabled(True)
        else:
            self.quantity_input.setEnabled(False)
    
    def set_loading_state(self, is_loading, message=None):
        """Set the UI to loading state when waiting for API response"""
        if is_loading:
            # Show loading UI
            self.progress_bar.setVisible(True)
            self.portfolio_list.setEnabled(False)
            
            # Start the loading animation
            if message:
                self.base_loading_message = message
                self.status_bar.showMessage(message)
            self.loading_dots = 0
            self.loading_timer.start(500)  # Update every 500ms
        else:
            # Hide loading UI
            self.progress_bar.setVisible(False)
            self.portfolio_list.setEnabled(True)
            self.loading_timer.stop()
            
            # Reset the status bar if it was showing loading dots
            if hasattr(self, 'base_loading_message'):
                self.status_bar.showMessage("Ready")
    
    def update_loading_message(self):
        """Update loading animation in status bar"""
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * self.loading_dots
        self.status_bar.showMessage(f"{self.base_loading_message}{dots}")
    
    def show_error(self, message):
        """Display error message"""
        self.error_message.setText(message)
        self.error_message.setVisible(True)
        self.success_message.setVisible(False)
    
    def show_success(self, message):
        """Display success message"""
        self.success_message.setText(message)
        self.success_message.setVisible(True)
        self.error_message.setVisible(False)
    
    def clear_messages(self):
        """Clear all status messages"""
        self.error_message.setVisible(False)
        self.success_message.setVisible(False)

    def stock_selected(self, symbol, price, chart_data):
        """Handle successful stock selection"""
        # Update UI elements
        self.stock_display.setText(f"Selected Stock: {symbol}")
        self.price_display.setText(f"Current Price: ${price:.2f}")
        
        # Show success message
        self.show_success(f"Selected: {symbol}")
        
        # Update status bar
        self.status_bar.showMessage(f"Stock selected: {symbol} - Ready to place sell order")
        
        # Enable buttons
        self.preview_button.setEnabled(True)
        self.sell_button.setEnabled(True)
        self.current_price_label.setText(f"Current Price: ${price:.2f}")
        
        # Update chart with the data
        self.update_stock_chart(symbol, chart_data)
    
    def display_order_preview(self, preview_info):
        """Display order preview dialog"""
        preview_dialog = OrderPreviewDialog(preview_info, self)
        return preview_dialog.exec()

    def preview_order(self):
        """Preview the sell order"""
        stock = self.stock_display.text().replace("Selected Stock: ", "")
        quantity = self.quantity_input.value()
        
        if stock == "None":
            self.show_error("Please select a stock from your portfolio first.")
            return
            
        self.presenter.preview_order(stock, quantity)

    def confirm_sell(self):
        """Execute the sell order"""
        stock = self.stock_display.text().replace("Selected Stock: ", "")
        quantity = self.quantity_input.value()
        
        if stock == "None":
            self.show_error("Please select a stock from your portfolio first.")
            return
            
        success = self.presenter.process_sell_order(stock, quantity)
        if success:
            # Reload the portfolio data to show updated quantities
            self.presenter.load_portfolio_data()
            # Do not close window to allow for more sales
    
    def show_success_message(self, message):
        """Display success message dialog"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()

    def show_error_message(self, message):
        """Display error message dialog"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()
        
    def update_stock_chart(self, stock_symbol, chart_data):
        """Update the stock chart with historical data"""
        # Create a new chart
        chart = QChart()
        chart.setTitle(f"{stock_symbol} - 52 Week History")
        chart.setTitleFont(QFont("SF Pro Display", 12, QFont.Bold))
        chart.setTitleBrush(QColor(FaceID6Theme.PRIMARY_COLOR))  # Use theme color
        chart.setBackgroundVisible(False)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create data series
        series = QLineSeries()
        series.setName(f"{stock_symbol} Price")
        
        # Add data points
        for date_timestamp, price in chart_data:
            series.append(date_timestamp, price)
        
        # Style the line with theme color
        pen = QPen(QColor(FaceID6Theme.PRIMARY_COLOR))
        pen.setWidth(3)
        series.setPen(pen)
        
        chart.addSeries(series)
        
        # Set up axes
        date_axis = QDateTimeAxis()
        date_axis.setFormat("MMM yyyy")
        date_axis.setTitleText("Date")
        date_axis.setTitleFont(QFont("SF Pro Display", 10))
        date_axis.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))  # Use theme color
        date_axis.setGridLineVisible(True)
        date_axis.setGridLineColor(QColor("#E5E5EA"))  # Light grid lines
        
        value_axis = QValueAxis()
        value_axis.setTitleText("Price ($)")
        value_axis.setTitleFont(QFont("SF Pro Display", 10))
        value_axis.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))  # Use theme color
        value_axis.setGridLineVisible(True)
        value_axis.setGridLineColor(QColor("#E5E5EA"))  # Light grid lines
        
        # Calculate appropriate axis ranges
        if chart_data:
            min_x = min(date for date, _ in chart_data)
            max_x = max(date for date, _ in chart_data)
            min_y = min(price for _, price in chart_data)
            max_y = max(price for _, price in chart_data)
            
            # Add padding to y-axis
            y_padding = (max_y - min_y) * 0.1
            value_axis.setRange(min_y - y_padding, max_y + y_padding)
            date_axis.setRange(QDateTime.fromMSecsSinceEpoch(min_x), QDateTime.fromMSecsSinceEpoch(max_x))
        
        chart.addAxis(date_axis, Qt.AlignBottom)
        chart.addAxis(value_axis, Qt.AlignLeft)
        series.attachAxis(date_axis)
        series.attachAxis(value_axis)