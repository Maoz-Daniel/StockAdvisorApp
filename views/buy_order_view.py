from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QLineEdit, QSpinBox, QComboBox, QApplication,
    QScrollArea, QSizePolicy, QHBoxLayout, QStatusBar, QMessageBox, QDialog,
    QCompleter, QProgressBar, QTextEdit, QDialogButtonBox, QSpacerItem, QGridLayout, QMenu
)

from PySide6.QtCore import Qt, QSize, QDate, QDateTime, QTimer, QByteArray, QUrl, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QIcon, QPixmap
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from presenters.buy_order_presenter import BuyOrderPresenter
from assets.theme import FaceID6Theme


class OrderPreviewDialog(QDialog):
    """Dialog to preview order details before confirming"""
    def __init__(self, preview_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Order Preview")
        self.resize(400, 300)
        
        # Get theme colors
        theme = FaceID6Theme()
        
        # Apply iOS-inspired light theme styling using theme variables
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme.BACKGROUND_COLOR};
                color: {theme.TEXT_PRIMARY};
                font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
            }}
            QLabel {{
                color: {theme.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QFrame {{
                background-color: {theme.CARD_COLOR};
                border-radius: 10px;
                border: 1px solid #E5E5EA;
            }}
            QPushButton {{
                background-color: {theme.BACKGROUND_COLOR};
                color: {theme.ACCENT_COLOR};
                border: 1px solid #E5E5EA;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 500;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #E5E5EA;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Order Preview")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000;")
        layout.addWidget(header)
        
        # Order details
        details = QFrame()
        details.setObjectName("order-summary")
        details.setStyleSheet(f"""
            background-color: {theme.BACKGROUND_COLOR};
            border-radius: 10px;
            border: 1px solid #E5E5EA;
            padding: 15px;
        """)
        details_layout = QVBoxLayout(details)
        
        stock_label = QLabel(f"Stock: {preview_info['stock']}")
        quantity_label = QLabel(f"Quantity: {preview_info['quantity']}")
        price_label = QLabel(f"Current Price per share: ${preview_info['price_per_share']:.2f}")
        total_label = QLabel(f"Total Cost: ${preview_info['estimated_total']:.2f}")
        
        # Use theme accent color
        total_label.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {theme.ACCENT_COLOR};")
        
        details_layout.addWidget(stock_label)
        details_layout.addWidget(quantity_label)
        details_layout.addWidget(price_label)
        details_layout.addWidget(total_label)
        
        layout.addWidget(details)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        confirm_button = QPushButton("Confirm Order")
        confirm_button.setObjectName("highlight-button")
        
        # Use theme accent color for the button
        confirm_button.setStyleSheet(f"""
            background-color: {theme.ACCENT_COLOR};
            color: white;
            border: none;
        """)
        confirm_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(confirm_button)
        layout.addLayout(buttons_layout)


class BuyOrderWindow(QMainWindow):
    purchase_completed = Signal()

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("Buy Stock - SmartInvest Pro")
        self.resize(900, 800)
        self.showFullScreen()
        
        # Reference to theme
        self.theme = FaceID6Theme()
        
        # Apply FaceID6 theme styling
        self.setStyleSheet(self.theme.STYLE_SHEET)

        # Main structure with scrolling support
        central_widget = QWidget()
        main_container_layout = QVBoxLayout(central_widget)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.setSpacing(0)
        
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
        self.header_frame.setMinimumHeight(80)
        
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel(" Buy Stock")
        title_label.setObjectName("welcome-label")
        title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle-label")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title_label)
        header_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # Main content with search on right and company info on left
        main_content_layout = QHBoxLayout()
        
        # Left placeholder for company info (will be filled when stock is selected)
        self.company_info_placeholder = QWidget()
        self.company_info_placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Right side - Search section
        search_section = QFrame()
        search_section.setObjectName("card")
        search_section.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        search_section.setMaximumWidth(350)
        search_layout = QVBoxLayout(search_section)
        search_layout.setContentsMargins(20, 20, 20, 20)
        
        search_title = QLabel("Search Stock")
        search_title.setObjectName("section-title")
        
        # Search input with button in vertical layout
        search_input_layout = QVBoxLayout()
        
        self.stock_search = QLineEdit()
        self.stock_search.setObjectName("stock-search")
        self.stock_search.setPlaceholderText("Enter company name (e.g., Apple)...")
        
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("highlight-button")
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.search_stock)
        
        search_input_layout.addWidget(self.stock_search)
        search_input_layout.addWidget(self.search_button)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(False)
        
        # Error message label (initially hidden)
        self.error_message = QLabel("")
        self.error_message.setObjectName("error-message")
        self.error_message.setVisible(False)
        
        # Success message for stock found
        self.success_message = QLabel("")
        self.success_message.setObjectName("success-message")
        self.success_message.setVisible(False)
        
        search_layout.addWidget(search_title)
        search_layout.addLayout(search_input_layout)
        search_layout.addWidget(self.progress_bar)
        search_layout.addWidget(self.error_message)
        search_layout.addWidget(self.success_message)
        
        # Add to main content layout
        main_content_layout.addWidget(self.company_info_placeholder, 3)  # 3:1 ratio for left:right
        main_content_layout.addWidget(search_section, 1)
        
        # Add main content layout to main layout
        self.main_layout.addLayout(main_content_layout)
        
        # Chart section
        chart_section = QFrame()
        chart_section.setObjectName("card")
        chart_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart_layout = QVBoxLayout(chart_section)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        
        chart_title = QLabel("Stock Price History (52 Weeks)")
        chart_title.setObjectName("section-title")
        
        self.chart_view = QChartView()
        self.chart_view.setMinimumHeight(300)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setObjectName("chart-container")
        
        # Add shadow effect to chart
        chart_shadow = QGraphicsDropShadowEffect(self.chart_view)
        chart_shadow.setBlurRadius(15)
        accent_color = QColor(self.theme.ACCENT_COLOR)
        accent_color.setAlpha(30)
        chart_shadow.setColor(accent_color)   
        chart_shadow.setOffset(0, 2)
        self.chart_view.setGraphicsEffect(chart_shadow)
        
        # Setup empty chart
        empty_chart = QChart()
        empty_chart.setTitle("No Stock Selected")
        empty_chart.setBackgroundVisible(False)
        empty_chart.setTitleFont(QFont("SF Pro Display", 12, QFont.Bold))
        empty_chart.setTitleBrush(QColor(self.theme.ACCENT_COLOR))
        self.chart_view.setChart(empty_chart)
        
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.chart_view)
        self.current_price_label = QLabel("Current Price: $0.00")
        self.current_price_label.setAlignment(Qt.AlignCenter)
        self.current_price_label.setObjectName("current-price-label")
        chart_layout.addWidget(self.current_price_label)
        
        self.main_layout.addWidget(chart_section)

        # Buy order form section
        self.form_frame = QFrame()
        self.form_frame.setObjectName("card")
        self.form_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        form_layout = QVBoxLayout(self.form_frame)
        form_layout.setSpacing(18)
        form_layout.setContentsMargins(20, 20, 20, 20)

        # Form elements
        form_title = QLabel("Buy Order Details")
        form_title.setObjectName("section-title")
        form_layout.addWidget(form_title)
        
        self.stock_display = QLabel("Selected Stock: None")
        self.stock_display.setObjectName("stock-display")
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1000)
        quantity_row = self.create_form_row("Enter Quantity to Buy:", self.quantity_input)
        
        # Stock price display (read-only)
        self.price_display = QLabel("Current Price: $0.00")
        self.price_display.setObjectName("price-display")
        
        # Total cost display
        total_cost_layout = QHBoxLayout()
        total_cost_label = QLabel("Estimated Total:")
        total_cost_label.setObjectName("accent-text")
        
        self.total_cost_value = QLabel("$0.00")
        self.total_cost_value.setObjectName("large-value")
        self.total_cost_value.setStyleSheet("font-size: 24px;")
        
        total_cost_layout.addWidget(total_cost_label)
        total_cost_layout.addStretch()
        total_cost_layout.addWidget(self.total_cost_value)
        
        # Connect quantity change to update total cost
        self.quantity_input.valueChanged.connect(self.update_total_cost)
        
        # Add all elements to form layout
        form_layout.addWidget(self.stock_display)
        form_layout.addWidget(quantity_row)
        form_layout.addWidget(self.price_display)
        form_layout.addLayout(total_cost_layout)
        
        self.main_layout.addWidget(self.form_frame)

        # Buttons section
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        
        self.preview_button = QPushButton("Preview Order")  
        preview_svg_data = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#37506D" version="1.1" id="Layer_1" width="800px" height="800px" viewBox="0 0 92 92" enable-background="new 0 0 92 92" xml:space="preserve">
        <path id="XMLID_1239_" d="M91.3,43.8C90.6,42.8,74.4,19,46,19C17.6,19,1.4,42.8,0.7,43.8c-0.9,1.3-0.9,3.1,0,4.5  C1.4,49.2,17.6,73,46,73c28.4,0,44.6-23.8,45.3-24.8C92.2,46.9,92.2,45.1,91.3,43.8z M46,65C26.7,65,13.5,51.4,9,46  c4.5-5.5,17.6-19,37-19c19.3,0,32.5,13.6,37,19C78.4,51.5,65.3,65,46,65z M48.3,29.6c-4.4-0.6-8.7,0.5-12.3,3.2c0,0,0,0,0,0  c-7.3,5.5-8.8,15.9-3.3,23.2c2.7,3.6,6.5,5.8,10.9,6.5c0.8,0.1,1.6,0.2,2.3,0.2c3.6,0,7-1.2,9.9-3.3c7.3-5.5,8.8-15.9,3.3-23.2  C56.6,32.5,52.7,30.2,48.3,29.6z M52.3,54.5c-2.2,1.7-5,2.4-7.8,2c-2.8-0.4-5.3-1.9-7-4.1C34.1,47.7,35,41,39.7,37.5  c2.2-1.7,5-2.4,7.8-2c2.8,0.4,5.3,1.9,7,4.1C57.9,44.3,57,51,52.3,54.5z M51.9,40c0.8,0.7,1.2,1.8,1.2,2.8c0,1-0.4,2.1-1.2,2.8  c-0.7,0.7-1.8,1.2-2.8,1.2c-1.1,0-2.1-0.4-2.8-1.2c-0.8-0.8-1.2-1.8-1.2-2.8c0-1.1,0.4-2.1,1.2-2.8c0.7-0.8,1.8-1.2,2.8-1.2  C50.2,38.9,51.2,39.3,51.9,40z"/>
        </svg>"""
        preview_svg_data = preview_svg_data.replace('<path', '<path style="fill:#37506D;"')
        renderer = QSvgRenderer(QByteArray(preview_svg_data.encode()))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        preview_icon = QIcon(pixmap)

        self.preview_button.setIcon(preview_icon)
        self.preview_button.setIconSize(QSize(24, 24))
        self.preview_button.setCursor(Qt.PointingHandCursor)
        self.preview_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.preview_button.clicked.connect(self.preview_order)

        self.buy_button = QPushButton(" Confirm Buy Order")
        confirm_svg_data = """<svg xmlns="http://www.w3.org/2000/svg" width="800px" height="800px" viewBox="0 0 1024 1024" class="icon" version="1.1"><path d="M511.64164 924.327835c-228.816869 0-414.989937-186.16283-414.989937-414.989937S282.825796 94.347961 511.64164 94.347961c102.396724 0 200.763434 37.621642 276.975315 105.931176 9.47913 8.499272 10.266498 23.077351 1.755963 32.556481-8.488009 9.501656-23.054826 10.266498-32.556481 1.778489-67.723871-60.721519-155.148319-94.156494-246.174797-94.156494-203.396868 0-368.880285 165.482394-368.880285 368.880285S308.243749 878.218184 511.64164 878.218184c199.164126 0 361.089542-155.779033 368.60998-354.639065 0.49556-12.720751 11.032364-22.863359 23.910794-22.177356 12.720751 0.484298 22.649367 11.190043 22.15483 23.910794-8.465484 223.74966-190.609564 399.015278-414.675604 399.015278z" fill="#22C67F"/><path d="M960.926616 327.538868l-65.210232-65.209209-350.956149 350.956149-244.56832-244.566273-65.210233 65.209209 309.745789 309.743741 0.032764-0.031741 0.03174 0.031741z" fill="#74E8AE"/></svg>"""
        renderer = QSvgRenderer(QByteArray(confirm_svg_data.encode()))
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        buy_icon = QIcon(pixmap)
        self.buy_button.setObjectName("highlight-button")
        self.buy_button.setCursor(Qt.PointingHandCursor)
        self.buy_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.buy_button.setIconSize(QSize(24, 24))
        self.buy_button.setIcon(buy_icon) 

        self.buy_button.clicked.connect(self.confirm_buy)

        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addSpacing(15)
        buttons_layout.addWidget(self.buy_button)
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
        self.presenter = BuyOrderPresenter(self, self.model)
        
        # Connect enter key on search box to search function
        self.stock_search.returnPressed.connect(self.search_stock)
        
        # Initially disable buy buttons until a stock is selected
        self.preview_button.setEnabled(False)
        self.buy_button.setEnabled(False)
        
        # Setup loading animation timer
        self.loading_dots = 0
        self.loading_timer = QTimer(self)
        self.loading_timer.timeout.connect(self.update_loading_message)

    def create_form_row(self, label_text, input_widget):
        """Create a form input row with label and input widget"""
        row_widget = QWidget()
        row_layout = QVBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setObjectName("accent-text")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        input_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        input_widget.setObjectName("quantity-spinner")
        
        row_layout.addWidget(label)
        row_layout.addWidget(input_widget)
        
        return row_widget

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
                ("Buy Assets", lambda: None),  # Already in Buy window, do nothing
                ("Sell Assets", self.close),
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
        
        # Overall frame styling
        header_frame.setStyleSheet(f"""
        QFrame#header-bar {{
            background-color: {self.theme.PRIMARY_COLOR};
            color: white;
        }}
    """)
        
        return header_frame
    
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)

    def update_user_info(self, username):
        """Update username in the UI"""
        self.subtitle_label.setText(f"Search and buy stocks - {username}")
        self.status_bar.showMessage(
            f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30"
        )
    
    def update_stock_list(self, stocks):
        """Update stock autocomplete with available stocks"""
        completer = QCompleter(stocks)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.stock_search.setCompleter(completer)

    def update_total_cost(self):
        """Update the total cost based on quantity"""
        try:
            quantity = self.quantity_input.value()
            price_text = self.price_display.text().replace("Current Price: $", "")
            price = float(price_text) if price_text and price_text != "0.00" else 0
            
            total = quantity * price
            self.total_cost_value.setText(f"${total:.2f}")
        except (ValueError, AttributeError):
            self.total_cost_value.setText("$0.00")

    def set_loading_state(self, is_loading, message=None):
        """Set the UI to loading state when waiting for API response"""
        if is_loading:
            # Show loading UI
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.search_button.setEnabled(False)
            self.stock_search.setEnabled(False)
            self.stock_search.setReadOnly(True)  # Explicitly set read-only
            
            # Start the loading animation
            if message:
                self.base_loading_message = message
                self.status_bar.showMessage(message)
            self.loading_dots = 0
            self.loading_timer.start(500)  # Update every 500ms
        else:
            # Hide loading UI and ensure controls are enabled
            self.progress_bar.setVisible(False)
            self.search_button.setEnabled(True)
            self.search_button.clearFocus()
            self.stock_search.setEnabled(True)
            self.stock_search.setReadOnly(False)
            self.stock_search.clearFocus()
            self.loading_timer.stop()
            
            # Process events to ensure UI updates
            QApplication.processEvents()
            
            # Reset the status bar if it was showing loading dots
            if hasattr(self, 'base_loading_message'):
                self.status_bar.showMessage("Ready")
    
    def update_loading_message(self):
        """Update loading animation in status bar"""
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * self.loading_dots
        self.status_bar.showMessage(f"{self.base_loading_message}{dots}")

    def show_error(self, message):
        """Display error message below search box"""
        self.error_message.setText(message)
        self.error_message.setVisible(True)
        self.success_message.setVisible(False)
   
    def show_success(self, message):
        """Display success message below search box"""
        self.success_message.setText(message)
        self.success_message.setVisible(True)
        self.error_message.setVisible(False)

    def clear_messages(self):
        """Clear all status messages"""
        self.error_message.setVisible(False)
        self.success_message.setVisible(False)

    def search_stock(self):
        """Handle stock search by company name"""
        company_name = self.stock_search.text().strip()
        if not company_name:
            self.show_error("Please enter a company name")
            return
            
        # Clear previous messages
        self.clear_messages()
        
        # Call the presenter to search for the stock
        self.presenter.search_stock_by_name(company_name)
    
    def stock_found(self, symbol, price, company_name, chart_data):
        """Handle successful stock search - just update price and chart"""
        # Update UI elements
        self.stock_display.setText(f"Selected Stock: {symbol}")
        self.price_display.setText(f"Current Price: ${price:.2f}")
        
        # Update total cost
        self.update_total_cost()
        
        # Show success message
        self.show_success(f"Found: {company_name} ({symbol})")
        
        # Update status bar
        self.status_bar.showMessage(f"Stock found: {company_name} ({symbol}) - Ready to place order")
        
        # Enable buttons
        self.preview_button.setEnabled(True)
        self.buy_button.setEnabled(True)
        self.current_price_label.setText(f"Current Price: ${price:.2f}")
        
        # Update chart with the data
        self.update_stock_chart(symbol, chart_data)
    
    def stock_not_found(self, company_name, error_message=None):
        """Handle case when stock is not found"""
        # Show error message
        self.show_error(error_message or "The stock name is incorrect or the stock does not exist")
        
        # Update status bar
        self.status_bar.showMessage(f"Stock not found: {company_name}")
        
        # Disable buttons
        self.preview_button.setEnabled(False)
        self.buy_button.setEnabled(False)
        
        # Reset stock display
        self.stock_display.setText("Selected Stock: None")
        self.price_display.setText("Current Price: $0.00")
        self.total_cost_value.setText("$0.00")
        
        # Reset chart
        empty_chart = QChart()
        empty_chart.setTitle("No Stock Selected")
        empty_chart.setBackgroundVisible(False)
        empty_chart.setTitleFont(QFont("SF Pro Display", 12, QFont.Bold))
        empty_chart.setTitleBrush(QColor(self.theme.ACCENT_COLOR))
        self.chart_view.setChart(empty_chart)

    def display_order_preview(self, preview_info):
        """Display order preview dialog"""
        preview_dialog = OrderPreviewDialog(preview_info, self)
        return preview_dialog.exec()

    def preview_order(self):
        """Preview the buy order"""
        stock = self.stock_display.text().replace("Selected Stock: ", "")
        quantity = self.quantity_input.value()
        
        if stock == "None":
            self.show_error("Please search and select a stock first.")
            return
            
        self.presenter.preview_order(stock, quantity)

    def confirm_buy(self):
        """Execute the buy order"""
        stock = self.stock_display.text().replace("Selected Stock: ", "")
        quantity = self.quantity_input.value()
        
        if stock == "None":
            self.show_error("Please search and select a stock first.")
            return
            
        success = self.presenter.process_buy_order(stock, quantity)
        if success:
            self.purchase_completed.emit()
            self.close()
          
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

    def update_ui_with_all_data(self, result):
        """Update all UI elements at once"""
        symbol = result["symbol"]
        price = result["price"]
        chart_data = result["chart_data"]
        profile = result.get("profile", {})
        description = result.get("description", "")
        
        # Create company info content
        company_info = self._prepare_company_info(symbol, profile, description)
        
        # Update everything at once
        self.setUpdatesEnabled(False)
        
        try:
            # Update chart and price info
            self.stock_display.setText(f"Selected Stock: {symbol}")
            self.price_display.setText(f"Current Price: ${price:.2f}")
            self.update_total_cost()
            self.current_price_label.setText(f"Current Price: ${price:.2f}")
            self.update_stock_chart(symbol, chart_data)
            
            # Replace placeholder with company info
            for i in range(self.main_layout.count()):
                item = self.main_layout.itemAt(i)
                if isinstance(item, QHBoxLayout):
                    for j in range(item.count()):
                        widget_item = item.itemAt(j)
                        if widget_item and widget_item.widget() == self.company_info_placeholder:
                            old_widget = self.company_info_placeholder
                            item.replaceWidget(old_widget, company_info)
                            old_widget.setParent(None)
                            self.company_info_placeholder = company_info
                            break
            
            # Enable buttons
            self.preview_button.setEnabled(True)
            self.buy_button.setEnabled(True)
            
            # Show success message
            self.show_success(f"Found: {profile.get('name', symbol)} ({symbol})")
        finally:
            # Apply all changes at once
            self.setUpdatesEnabled(True)
            
            # Turn off loading state
            self.status_bar.showMessage(f"Stock information loaded")
            self.set_loading_state(False)
            
            # Reset search controls
            self.stock_search.setEnabled(True)
            self.stock_search.setReadOnly(False)
            self.stock_search.clearFocus()
            QApplication.processEvents()
   
    def _prepare_company_info(self, symbol, profile, description):
        """Create the company info widget but don't add it to layout yet"""
        company_info = QFrame()
        company_info.setObjectName("card")
        company_info.setMinimumHeight(300)
        company_layout = QVBoxLayout(company_info)
        company_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create header with name and symbol
        header_layout = QHBoxLayout()
        name_label = QLabel(profile.get("name", symbol))
        name_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        ticker_label = QLabel(f"({symbol})")
        ticker_label.setStyleSheet("font-size: 18px; color: #666;")
        
        # Add logo placeholder
        logo_frame = QFrame()
        logo_frame.setFixedSize(80, 80)
        logo_frame.setStyleSheet(f"background-color: {self.theme.ACCENT_COLOR}; border-radius: 8px;")
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(5, 5, 5, 5)
        
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        initial = profile.get("name", symbol)[0].upper()
        logo_label.setText(initial)
        logo_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        logo_layout.addWidget(logo_label)
        
        # If there's a logo URL, load it asynchronously after UI is updated
        logo_url = profile.get("logoUrl", "")
        if logo_url and logo_url.strip():
            # Create a reference to update later
            self.pending_logo_label = logo_label
            self.pending_logo_url = logo_url
            # Start loading in the background after UI updates
            QTimer.singleShot(100, self._load_logo_async)
        
        header_layout.addWidget(logo_frame)
        header_layout.addWidget(name_label)
        header_layout.addWidget(ticker_label)
        header_layout.addStretch()
        
        # Company details
        details_grid = QGridLayout()
        details_grid.setVerticalSpacing(10)
        details_grid.setHorizontalSpacing(20)
        
        # Industry Row
        industry_label = QLabel("Industry:")
        industry_label.setStyleSheet(f"color: {self.theme.ACCENT_COLOR}; font-weight: bold; font-size: 14px;")
        details_grid.addWidget(industry_label, 0, 0)

        industry_value = QLabel(profile.get("industry", "N/A"))
        industry_value.setStyleSheet(f"color: {self.theme.TEXT_PRIMARY}; font-size: 14px;")
        details_grid.addWidget(industry_value, 0, 1)

        # Exchange Row
        exchange_label = QLabel("Exchange:")
        exchange_label.setStyleSheet(f"color: {self.theme.ACCENT_COLOR}; font-weight: bold; font-size: 14px;")
        details_grid.addWidget(exchange_label, 0, 2)

        exchange_value = QLabel(profile.get("exchange", "N/A"))
        exchange_value.setStyleSheet(f"color: {self.theme.TEXT_PRIMARY}; font-size: 14px;")
        details_grid.addWidget(exchange_value, 0, 3)

        # Country Row
        country_label = QLabel("Country:")
        country_label.setStyleSheet(f"color: {self.theme.ACCENT_COLOR}; font-weight: bold; font-size: 14px;")
        details_grid.addWidget(country_label, 1, 0)

        country_value = QLabel(profile.get("country", "N/A"))
        country_value.setStyleSheet(f"color: {self.theme.TEXT_PRIMARY}; font-size: 14px;")
        details_grid.addWidget(country_value, 1, 1)

        # Website Row
        website_label = QLabel("Website:")
        website_label.setStyleSheet(f"color: {self.theme.ACCENT_COLOR}; font-weight: bold; font-size: 14px;")
        details_grid.addWidget(website_label, 1, 2)

        web_value = QLabel(profile.get("webUrl", "N/A"))
        # Apply styling for website link
        web_value.setStyleSheet("color: blue; text-decoration: underline; font-size: 14px;")
        details_grid.addWidget(web_value, 1, 3)

        # Description Section
        desc_label = QLabel("Company Description")
        desc_label.setStyleSheet(f"color: {self.theme.ACCENT_COLOR}; font-weight: bold; font-size: 16px; margin-top: 15px;")
        company_layout.addLayout(header_layout)
        company_layout.addSpacing(5)
        company_layout.addLayout(details_grid)
        company_layout.addWidget(desc_label)

        desc_text = QTextEdit()
        desc_text.setReadOnly(True)
        desc_text.setMinimumHeight(100)
        desc_text.setMaximumHeight(150)
        desc_text.setText(description)
        desc_text.setStyleSheet("""
        background-color: #F8F9FA;
        border: 1px solid #E5E5EA;
        border-radius: 6px;
        padding: 10px;
        font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
        font-size: 14px;
    """)

        company_layout.addWidget(desc_text)

        return company_info
    
    def update_stock_chart(self, stock_symbol, chart_data):
        """Update the stock chart with historical data"""
        # Create a new chart
        chart = QChart()
        chart.setTitle(f"{stock_symbol} - 52 Week History")
        chart.setTitleFont(QFont("SF Pro Display", 12, QFont.Bold))
        chart.setTitleBrush(QColor(self.theme.ACCENT_COLOR))
        chart.setBackgroundVisible(False)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Create data series
        series = QLineSeries()
        series.setName(f"{stock_symbol} Price")
        
        # Add data points
        for date_timestamp, price in chart_data:
            series.append(date_timestamp, price)
        
        # Style the line
        pen = QPen(QColor(self.theme.ACCENT_COLOR))
        pen.setWidth(3)
        series.setPen(pen)
        
        chart.addSeries(series)
        
        # Set up axes
        date_axis = QDateTimeAxis()
        date_axis.setFormat("MMM yyyy")
        date_axis.setTitleText("Date")
        date_axis.setTitleFont(QFont("SF Pro Display", 10))
        date_axis.setLabelsColor(QColor("#666666"))
        date_axis.setGridLineVisible(True)
        date_axis.setGridLineColor(QColor("#E5E5EA"))
        
        value_axis = QValueAxis()
        value_axis.setTitleText("Price ($)")
        value_axis.setTitleFont(QFont("SF Pro Display", 10))
        value_axis.setLabelsColor(QColor("#666666"))
        value_axis.setGridLineVisible(True)
        value_axis.setGridLineColor(QColor("#E5E5EA"))
        
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
        
        # Update the chart view
        self.chart_view.setChart(chart)

    def _load_logo_async(self):
        """Load logo asynchronously after UI is updated"""
        if hasattr(self, 'pending_logo_url') and hasattr(self, 'pending_logo_label'):
            # Create network request to load the logo
            self.network_manager = QNetworkAccessManager()
            self.network_manager.finished.connect(
                lambda reply: self._update_logo(reply, self.pending_logo_label)
            )
            
            # Start the network request
            request = QNetworkRequest(QUrl(self.pending_logo_url))
            self.network_manager.get(request)

    def _update_logo(self, reply, label):
        """Update logo when loaded"""
        if reply.error() == QNetworkReply.NoError:
            try:
                data = reply.readAll()
                pixmap = QPixmap()
                if pixmap.loadFromData(data):
                    scaled_pixmap = pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label.setPixmap(scaled_pixmap)
                    label.setText("")  # Clear any text
            except Exception:
                pass