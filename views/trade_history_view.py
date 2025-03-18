import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QDateEdit, QComboBox, QFrame, QApplication,
    QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy, QCheckBox, QGridLayout,
    QScrollArea  
)
from PySide6.QtCore import Qt, QDate, QMargins, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QIcon
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis

from presenters.trade_history_presenter import TradeHistoryPresenter

# Import the luxury theme
from assets.theme import LuxuryTheme


class EnhancedChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        
        # Apply luxurious styling
        self.setStyleSheet("""
            background-color: #1E3A5F;
            border-radius: 8px;
            border: 1px solid #2C5A8C;
        """)
        
        # Add blue glow shadow effect with gold tint
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 215, 0, 30))  # Gold glow
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
    def createLineChart(self, chart_data=[]):
        # Create data series
        print(f"📊 Creating Line Chart with: {chart_data}")
        series = QLineSeries()
        series.setName("Trade Value")
        
        if not chart_data:
            print("⚠️ No data for chart!")
            return
        
        for x, y in chart_data:
            print(f"Adding data point: ({x}, {y})")
            series.append(x, y)

        if chart_data:
            min_x = min(x for x, _ in chart_data)
            max_x = max(x for x, _ in chart_data)
            min_y = min(y for _, y in chart_data)
            max_y = max(y for _, y in chart_data)
        else:
            min_x, max_x, min_y, max_y = 0, 10, 0, 1000

        # Style the line
        pen = QPen(QColor(LuxuryTheme.GOLD))
        pen.setWidth(3)
        series.setPen(pen)

        # Create the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Trade Performance History")
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setTitleBrush(QColor(LuxuryTheme.GOLD))
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Style the axis
        axisX = QValueAxis()
        axisX.setRange(0, 8)
        axisX.setTitleText("Week")
        axisX.setTitleFont(QFont("Segoe UI", 10))
        axisX.setLabelsColor(QColor(LuxuryTheme.TEXT_LIGHT))
        axisX.setGridLineVisible(True)
        axisX.setGridLineColor(QColor(LuxuryTheme.HIGHLIGHT_BLUE))
        axisX.setTickCount(8)

        axisY = QValueAxis()
        axisY.setRange(min_y-100, max_y+100) 
        axisY.setTitleText("Value ($)")
        axisY.setTitleFont(QFont("Segoe UI", 10))
        axisY.setLabelsColor(QColor(LuxuryTheme.TEXT_LIGHT))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor(LuxuryTheme.HIGHLIGHT_BLUE))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        # Style the legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 9))
        chart.legend().setLabelColor(QColor(LuxuryTheme.TEXT_LIGHT))
        
        self.setChart(chart)
        
    def createBarChart(self, bar_chart_data=[]):
        """Create a bar chart based on data"""
        print(f"📊 Creating Bar Chart with: {bar_chart_data}")

        if not bar_chart_data:
            print("⚠️ No data for bar chart!")
            return

        barSet = QBarSet("Trades")

        # Add data to chart
        for stock, count in bar_chart_data:
            barSet.append(count)

        barSet.setColor(QColor(LuxuryTheme.GOLD))
        series = QBarSeries()
        series.append(barSet)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Number of Trades per Stock")
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setTitleBrush(QColor(LuxuryTheme.GOLD))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)

        categories = [stock for stock, _ in bar_chart_data]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(QFont("Segoe UI", 9))
        axisX.setLabelsColor(QColor(LuxuryTheme.TEXT_LIGHT))

        axisY = QValueAxis()
        axisY.setRange(0, max(count for _, count in bar_chart_data) + 2)
        axisY.setTitleText("Number of Trades")
        axisY.setTitleFont(QFont("Segoe UI", 10))
        axisY.setLabelsColor(QColor(LuxuryTheme.TEXT_LIGHT))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor(LuxuryTheme.HIGHLIGHT_BLUE))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setLabelColor(QColor(LuxuryTheme.TEXT_LIGHT))

        self.setChart(chart)


class TradeHistoryWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle(f"Trade History - SmartInvest Pro - {self.username}")

        # Set window size
        screen_size = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_size.x(), screen_size.y(), screen_size.width() * 0.85, screen_size.height() * 0.85)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply luxury theme
        self.setStyleSheet(LuxuryTheme.STYLE_SHEET)

        # Create scroll area for main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll_area)
        
        # Main content widget in scroll area
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        scroll_area.setWidget(content_widget)

        # Header section
        self.create_header_section(main_layout)
        
        # Action bar section
        self.create_action_section(main_layout)
        
        # Filter section
        self.create_filter_section(main_layout)
        
        # Table section
        self.create_table_section(main_layout)
        
        # Chart section
        self.create_chart_section(main_layout)

        # Initialize presenter
        self.presenter = TradeHistoryPresenter(self, self.model)
        
        # Load data
        self.presenter.load_trade_history()
        self.presenter.load_trade_chart_data()
        self.presenter.load_trade_bar_chart_data()

        print(f"TradeHistoryWindow.__init__: Model username: {model.get_username()}")

    def create_header_section(self, parent_layout):
        """Create header section with title and subtitle"""
        # Header container
        header_frame = QFrame()
        header_frame.setObjectName("header-frame")
        
        # Add blue glow shadow effect with gold tint
        shadow = QGraphicsDropShadowEffect(header_frame)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(255, 215, 0, 30))  # Subtle gold glow
        shadow.setOffset(0, 2)
        header_frame.setGraphicsEffect(shadow)
        
        # Header layout
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 25, 25, 25)
        
        # Left side with title
        left_layout = QVBoxLayout()
        
        title_label = QLabel("Trade History Dashboard")
        title_label.setObjectName("welcome-label")
        
        subtitle_label = QLabel(f"View and analyze your trading activity")
        subtitle_label.setObjectName("subtitle-label")
        
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addStretch()
        
        # Right side with analytics insight
        right_frame = QFrame()
        right_frame.setObjectName("gold-card")
        
        right_layout = QVBoxLayout(right_frame)
        
        account_label = QLabel(f"Active Account: {self.username}")
        account_label.setObjectName("gold-text")
        
        insight_label = QLabel("\"Trading history reflects strategy, not just results.\"")
        insight_label.setObjectName("quote-text")
        insight_label.setWordWrap(True)
        
        right_layout.addWidget(account_label)
        right_layout.addWidget(insight_label)
        
        # Add both sections to header
        header_layout.addLayout(left_layout, 7)
        header_layout.addWidget(right_frame, 3)
        
        parent_layout.addWidget(header_frame)

    def create_action_section(self, parent_layout):
        """Create action bar with summary and buttons"""
        action_title = QLabel("Trading Summary")
        action_title.setObjectName("section-title")
        parent_layout.addWidget(action_title)
        
        action_frame = QFrame()
        action_frame.setObjectName("card")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(20, 20, 20, 20)
        
        # Summary statistics section
        stats_layout = QVBoxLayout()
        
        trading_summary = QLabel("Overall Performance:")
        trading_summary.setObjectName("gold-accent-text")
        
        statistics_label = QLabel("Total Trades: 32 | Buy: 24 | Sell: 8 | Avg. Price: $485.50")
        statistics_label.setStyleSheet("color: #E8E8E8; font-size: 14px;")
        
        stats_layout.addWidget(trading_summary)
        stats_layout.addWidget(statistics_label)
        
        # Action buttons
        chart_toggle_button = QPushButton("Toggle Chart Type")
        chart_toggle_button.setObjectName("gold-button")
        chart_toggle_button.setFixedWidth(150)
        chart_toggle_button.clicked.connect(self.toggle_chart_type)
        
        export_button = QPushButton("Export Data")
        export_button.setFixedWidth(130)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(chart_toggle_button)
        button_layout.addWidget(export_button)
        
        action_layout.addLayout(stats_layout, 7)
        action_layout.addLayout(button_layout, 3)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(action_frame)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 215, 0, 20))
        shadow.setOffset(0, 3)
        action_frame.setGraphicsEffect(shadow)
        
        parent_layout.addWidget(action_frame)

    def create_filter_section(self, parent_layout):
        """Create filter controls section"""
        filter_title = QLabel("Filter Transactions")
        filter_title.setObjectName("section-title")
        parent_layout.addWidget(filter_title)
        
        filter_frame = QFrame()
        filter_frame.setObjectName("card")
        filter_layout = QGridLayout(filter_frame)
        
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setHorizontalSpacing(15)
        filter_layout.setVerticalSpacing(15)
        
        # From date filter
        from_label = QLabel("From:")
        from_label.setObjectName("gold-accent-text")
        
        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_edit.setCalendarPopup(True)
        self.from_date_edit.setStyleSheet("""
            background-color: #24466D;
            border: 1px solid #2C5A8C;
            border-radius: 6px;
            padding: 8px;
            color: #E8E8E8;
        """)

        # To date filter
        to_label = QLabel("To:")
        to_label.setObjectName("gold-accent-text")
        
        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate.currentDate())
        self.to_date_edit.setCalendarPopup(True)
        self.to_date_edit.setStyleSheet("""
            background-color: #24466D;
            border: 1px solid #2C5A8C;
            border-radius: 6px;
            padding: 8px;
            color: #E8E8E8;
        """)

        # Stock filter
        stock_label = QLabel("Stock:")
        stock_label.setObjectName("gold-accent-text")
        
        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["All Stocks", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"])
        self.stock_combo.setStyleSheet("""
            background-color: #24466D;
            border: 1px solid #2C5A8C;
            border-radius: 6px;
            padding: 8px;
            color: #E8E8E8;
        """)

        # Transaction type filter
        transaction_label = QLabel("Transaction:")
        transaction_label.setObjectName("gold-accent-text")
        
        transaction_layout = QHBoxLayout()
        
        self.buy_checkbox = QCheckBox("Buy")
        self.buy_checkbox.setChecked(True)
        self.buy_checkbox.setStyleSheet("""
            color: #E8E8E8;
            font-size: 14px;
            spacing: 8px;
        """)
        
        self.sell_checkbox = QCheckBox("Sell")
        self.sell_checkbox.setChecked(True)
        self.sell_checkbox.setStyleSheet("""
            color: #E8E8E8;
            font-size: 14px;
            spacing: 8px;
        """)
        
        transaction_layout.addWidget(self.buy_checkbox)
        transaction_layout.addWidget(self.sell_checkbox)
        transaction_layout.addStretch()

        # Filter action buttons
        filter_button = QPushButton("Apply Filter")
        filter_button.clicked.connect(self.apply_filter)
        
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("""
            background-color: #475569;
            color: white;
        """)
        reset_button.clicked.connect(self.reset_filters)
        
        # Add all components to grid
        filter_layout.addWidget(from_label, 0, 0)
        filter_layout.addWidget(self.from_date_edit, 0, 1)
        filter_layout.addWidget(to_label, 0, 2)
        filter_layout.addWidget(self.to_date_edit, 0, 3)
        filter_layout.addWidget(stock_label, 0, 4)
        filter_layout.addWidget(self.stock_combo, 0, 5)
        
        filter_layout.addWidget(transaction_label, 1, 0)
        filter_layout.addLayout(transaction_layout, 1, 1, 1, 2)
        filter_layout.addWidget(filter_button, 1, 4)
        filter_layout.addWidget(reset_button, 1, 5)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(filter_frame)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 215, 0, 20))
        shadow.setOffset(0, 3)
        filter_frame.setGraphicsEffect(shadow)
        
        parent_layout.addWidget(filter_frame)

    def create_table_section(self, parent_layout):
        """Create trade history table section"""
        table_title = QLabel("Transaction History")
        table_title.setObjectName("section-title")
        parent_layout.addWidget(table_title)
        
        table_frame = QFrame()
        table_frame.setObjectName("card")
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Date", "Stock", "Action", "Quantity", "Unit Price", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(300)
        
        # Add subtle glow effect to table with gold tint
        table_shadow = QGraphicsDropShadowEffect(self.table)
        table_shadow.setBlurRadius(10)
        table_shadow.setColor(QColor(255, 215, 0, 20))
        table_shadow.setOffset(0, 1)
        self.table.setGraphicsEffect(table_shadow)
        
        table_layout.addWidget(self.table)
        
        # Add shadow effect to frame
        frame_shadow = QGraphicsDropShadowEffect(table_frame)
        frame_shadow.setBlurRadius(15)
        frame_shadow.setColor(QColor(255, 215, 0, 20))
        frame_shadow.setOffset(0, 3)
        table_frame.setGraphicsEffect(frame_shadow)
        
        parent_layout.addWidget(table_frame)

    def create_chart_section(self, parent_layout):
        """Create chart visualization section"""
        chart_title = QLabel("Performance Visualization")
        chart_title.setObjectName("section-title")
        parent_layout.addWidget(chart_title)
        
        chart_frame = QFrame()
        chart_frame.setObjectName("card")
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create chart widget
        self.chart_widget = EnhancedChartWidget()
        self.chart_widget.setMinimumHeight(300)
        chart_layout.addWidget(self.chart_widget)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(chart_frame)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 215, 0, 20))
        shadow.setOffset(0, 3)
        chart_frame.setGraphicsEffect(shadow)
        
        parent_layout.addWidget(chart_frame)

    def update_chart(self, chart_data):
        """Update line chart with data"""
        print("Updating chart with data", chart_data)
        self.chart_widget.createLineChart(chart_data)
    
    def update_bar_chart(self, bar_chart_data):
        """Update bar chart with data"""
        print("📊 Updating Bar Chart with data:", bar_chart_data)
        self.chart_widget.createBarChart(bar_chart_data)
    
    def update_trade_table(self, trade_history):
        """Update trade history table with data"""
        print(f"✅ update_trade_table() called with {len(trade_history)} trades")

        # Clear old data
        self.table.clearContents()
        self.table.setRowCount(len(trade_history))

        if not trade_history:
            print("⚠️ No trades to display!")
            return

        for row, trade in enumerate(trade_history):
            print(f"🔹 Adding row {row}: {trade}")
            
            date_item = QTableWidgetItem(trade["date"].strftime("%Y-%m-%d"))
            stock_item = QTableWidgetItem(trade["stock"])
            action_item = QTableWidgetItem(trade["action"])
            quantity_item = QTableWidgetItem(str(trade["quantity"]))
            price_item = QTableWidgetItem(f"${trade['price']:.2f}")
            total_item = QTableWidgetItem(f"${trade['quantity'] * trade['price']:.2f}")
            
            # Set alignment
            date_item.setTextAlignment(Qt.AlignCenter)
            stock_item.setTextAlignment(Qt.AlignCenter)
            action_item.setTextAlignment(Qt.AlignCenter)
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Set colors for action column
            if trade["action"] == "Buy":
                action_item.setForeground(QColor(LuxuryTheme.POSITIVE_GREEN))
            else:
                action_item.setForeground(QColor(LuxuryTheme.NEGATIVE_RED))
                
            # Highlight total with gold
            total_item.setForeground(QColor(LuxuryTheme.GOLD))
            
            # Add items to table
            self.table.setItem(row, 0, date_item)
            self.table.setItem(row, 1, stock_item)
            self.table.setItem(row, 2, action_item)
            self.table.setItem(row, 3, quantity_item)
            self.table.setItem(row, 4, price_item)
            self.table.setItem(row, 5, total_item)
    
    def apply_filter(self):
        """Apply filters to trade history"""
        start_date = self.from_date_edit.date().toPython()
        end_date = self.to_date_edit.date().toPython()
        selected_stock = self.stock_combo.currentText()
        selected_action = []

        if self.buy_checkbox.isChecked():
            selected_action.append("Buy")
        if self.sell_checkbox.isChecked():
            selected_action.append("Sell")

        stocks = [] if selected_stock == "All Stocks" else [selected_stock]

        print(f"🔍 Sending filter request - Start: {start_date}, End: {end_date}, Stocks: {stocks}, Actions: {selected_action}")

        self.presenter.filter_trade_history(start_date, end_date, stocks, selected_action)

    def reset_filters(self):
        """Reset all filters to default values"""
        print("🔄 Resetting filters to default values...")

        # Reset filter fields
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.to_date_edit.setDate(QDate.currentDate())
        self.stock_combo.setCurrentIndex(0)  # Back to "All Stocks"
        self.buy_checkbox.setChecked(True)
        self.sell_checkbox.setChecked(True)

        # Reload all trades
        self.presenter.load_trade_history()

    def toggle_chart_type(self):
        """Toggle between chart types"""
        self.presenter.toggle_chart_type()
        
        # Add animation effect
        animation = QPropertyAnimation(self.chart_widget, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.chart_widget.geometry())
        animation.setEndValue(self.chart_widget.geometry())
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.start()


# For standalone testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create mock model
    from models.mock_stock_model import MockStockModel
    model = MockStockModel()
    
    window = TradeHistoryWindow(model)
    window.show()
    
    # High DPI support
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    sys.exit(app.exec())