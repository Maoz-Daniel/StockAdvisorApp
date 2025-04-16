import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView, QPushButton, QDateEdit, QComboBox, QFrame, 
    QApplication, QSizePolicy, QSpacerItem, QAbstractItemView, QScrollArea,QGraphicsDropShadowEffect,QMenu
)
from PySide6.QtCore import Qt, QDate, QSize, QMargins, QPropertyAnimation, QEasingCurve, QByteArray
from PySide6.QtGui import QColor, QPainter, QFont, QIcon, QPen, QBrush, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtSvg import QSvgRenderer

from PySide6.QtWidgets import QStyledItemDelegate
import tempfile

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis

from presenters.trade_history_presenter import TradeHistoryPresenter

# Import the FaceID6 theme
from assets.theme import FaceID6Theme
class LeftPaddingDelegate(QStyledItemDelegate):
    """Delegate to add left padding to table cells"""
    def __init__(self, padding, parent=None):
        super().__init__(parent)
        self.padding = padding
        
    def paint(self, painter, option, index):
        option.rect.setLeft(option.rect.left() + self.padding)
        super().paint(painter, option, index)

class RightAlignedDelegate(QStyledItemDelegate):
    """Delegate to align text to the right with optional padding."""
    def __init__(self, padding=10, parent=None):
        super().__init__(parent)
        self.padding = padding

    def paint(self, painter, option, index):
        # הגדרת יישור לימין ובאמצע אנכי
        option.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
        # ניתן להוסיף קצת Padding מהקצה הימני
        option.rect.setRight(option.rect.right() - self.padding)
        super().paint(painter, option, index)

class EnhancedChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        
        # Apply iOS-inspired styling
        self.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 1px solid #E5E5EA;
        """)
        
        # Add subtle shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))  # Soft shadow
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
        pen = QPen(QColor(FaceID6Theme.ACCENT_COLOR))
        pen.setWidth(3)
        series.setPen(pen)

        # Create the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Trade Performance History")
        chart.setTitleFont(QFont("SF Pro Display", 14, QFont.Bold))
        chart.setTitleBrush(QColor(FaceID6Theme.TEXT_PRIMARY))
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # Style the axis
        axisX = QValueAxis()
        axisX.setRange(0, 8)
        axisX.setTitleText("Week")
        axisX.setTitleFont(QFont("SF Pro Display", 11))
        axisX.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))
        axisX.setGridLineVisible(True)
        axisX.setGridLineColor(QColor("#E5E5EA"))
        axisX.setTickCount(8)

        axisY = QValueAxis()
        axisY.setRange(min_y-100, max_y+100) 
        axisY.setTitleText("Value ($)")
        axisY.setTitleFont(QFont("SF Pro Display", 11))
        axisY.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor("#E5E5EA"))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        # Style the legend
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("SF Pro Display", 10))
        chart.legend().setLabelColor(QColor(FaceID6Theme.TEXT_PRIMARY))
        
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

        barSet.setColor(QColor(FaceID6Theme.ACCENT_COLOR))
        series = QBarSeries()
        series.append(barSet)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Number of Trades per Stock")
        chart.setTitleFont(QFont("SF Pro Display", 14, QFont.Bold))
        chart.setTitleBrush(QColor(FaceID6Theme.TEXT_PRIMARY))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)

        categories = [stock for stock, _ in bar_chart_data]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(QFont("SF Pro Display", 10))
        axisX.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))

        axisY = QValueAxis()
        axisY.setRange(0, max(count for _, count in bar_chart_data) + 2)
        axisY.setTitleText("Number of Trades")
        axisY.setTitleFont(QFont("SF Pro Display", 11))
        axisY.setLabelsColor(QColor(FaceID6Theme.TEXT_SECONDARY))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor("#E5E5EA"))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setLabelColor(QColor(FaceID6Theme.TEXT_PRIMARY))

        self.setChart(chart)


class TradeHistoryWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("Trade History")

        # Set window size
        screen_size = QApplication.primaryScreen().availableGeometry()
        # Set window to full screen
        self.showFullScreen()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Apply FaceID6 theme
        self.setStyleSheet(FaceID6Theme.STYLE_SHEET)

        # Main widget to hold everything
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header bar
        self.header_frame = QFrame()
        self.header_frame.setObjectName("header-bar")
        self.header_frame.setFixedHeight(60)
        self.create_header_layout(self.header_frame)  # Put header creation code in a separate method
        
        # Add header to main layout
        main_layout.addWidget(self.header_frame)
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Content widget inside scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Add content sections
        self.create_header_section(content_layout)
        self.create_table_section(content_layout)
        self.create_chart_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        
        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)
        
        # Set main widget as central widget
        self.setCentralWidget(main_widget)
        
        # Initialize presenter
        self.presenter = TradeHistoryPresenter(self, self.model)
        
        # Load data
        self.presenter.load_trade_history()
        self.presenter.load_trade_chart_data()
        self.presenter.load_trade_bar_chart_data()


    def create_header_layout(self, header_frame):
        """Create the layout for the header bar with logo and navigation buttons"""
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
        
        # App name
        app_name = QLabel("InvestPro")
        app_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-left: 10px;")
        app_name.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering
        app_name.mousePressEvent = lambda event: self.close()  # Close window when clicked
        
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
                ("Dashboard", self.open_dashboard),
                ("My Portfolio", self.open_portfolio),
                ("Market Overview", self.open_market_overview),
                ("Reports & Analysis", self.open_reports),
                ("Account Settings", self.open_account_settings),
                ("Exit", self.close)
            ]),
            ("Trading", [
                ("Buy Assets", self.open_buy_order),
                ("Sell Assets", self.open_sell_order),
                ("Order History", self.open_trade_history)
            ]),
            ("Analytics", [
                ("Performance", self.open_performance),
                ("Risk Analysis", self.open_risk_analysis),
                ("AI Insights", self.open_ai_advisor)
            ]),
            ("Help", [
                ("Documentation", self.open_documentation),
                ("Support", self.open_support),
                ("About", self.open_about)
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
        header_layout.addLayout(nav_layout)
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Overall frame styling
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                color: white;
            }
        """)
    def create_header_bar(self):
        """Create a visible header bar with logo and navigation buttons"""
        # Create header frame
        self.header_frame = QFrame(self)
        self.header_frame.setObjectName("header-bar")
        self.header_frame.setGeometry(0, 0, self.width(), 60)
        
        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
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
        
        # App name
        app_name = QLabel("InvestPro")
        app_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-left: 10px;")
        
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
                ("Dashboard", self.open_dashboard),
                ("My Portfolio", self.open_portfolio),
                ("Market Overview", self.open_market_overview),
                ("Reports & Analysis", self.open_reports),
                ("Account Settings", self.open_account_settings),
                ("Exit", self.close)
            ]),
            ("Trading", [
                ("Buy Assets", self.open_buy_order),
                ("Sell Assets", self.open_sell_order),
                ("Order History", self.open_trade_history)
            ]),
            ("Analytics", [
                ("Performance", self.open_performance),
                ("Risk Analysis", self.open_risk_analysis),
                ("AI Insights", self.open_ai_advisor)
            ]),
            ("Help", [
                ("Documentation", self.open_documentation),
                ("Support", self.open_support),
                ("About", self.open_about)
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
        header_layout.addLayout(nav_layout)
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Overall frame styling
        self.header_frame.setStyleSheet("""
            QFrame {
                background-color: #1F2937;
                color: white;
            }
        """)
        self.header_frame.raise_()  # Ensure header is on top of other widgets

    def resizeEvent(self, event):
        """Handle resize events to adjust header bar width"""
        super().resizeEvent(event)
        if hasattr(self, 'header_frame'):
            # Ensure the header bar spans the full width of the window and stays at the top
            self.header_frame.setGeometry(0, 0, self.width(), 60)

    def create_header_section(self, parent_layout):
        """Create simple header with title and filter controls"""
        header_layout = QHBoxLayout()
        
        # Left side: Title and subtitle
        left_layout = QVBoxLayout()
        
        title_label = QLabel("Trade History")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #000000;
        """)
        
        subtitle_label = QLabel("Track your investment decisions")
        subtitle_label.setStyleSheet("""
            font-size: 16px;
            color: #6B7280;
        """)
        
        left_layout.addWidget(title_label)
        left_layout.addWidget(subtitle_label)
        left_layout.addStretch()
        
        # Right side: Date filters and action dropdown
        right_layout = QHBoxLayout()
        right_layout.setSpacing(10)
        
        # Action filter dropdown
        self.action_combo = QComboBox()
        self.action_combo.addItems(["All Actions", "Buy", "Sell"])
        self.action_combo.setFixedWidth(150)
        self.action_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #111827;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        
        # From date
        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.from_date_edit.setCalendarPopup(True)
        self.from_date_edit.setFixedWidth(150)
        self.from_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #111827;
            }
            QDateEdit::drop-down {
                border: none;
                width: 20px;
            }
        """)
        
        # To label
        to_label = QLabel("to")
        to_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            padding: 0 5px;
        """)
        
        # To date
        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate.currentDate())
        self.to_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.to_date_edit.setCalendarPopup(True)
        self.to_date_edit.setFixedWidth(150)
        self.to_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #111827;
            }
            QDateEdit::drop-down {
                border: none;
                width: 20px;
            }
        """)
        
        # Apply filter button
        self.apply_filter_btn = QPushButton("Apply Filter")
        self.apply_filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #37506D;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30455C;
            }
        """)
        self.apply_filter_btn.clicked.connect(self.apply_filter)
        
        right_layout.addWidget(self.action_combo)
        right_layout.addWidget(self.from_date_edit)
        right_layout.addWidget(to_label)
        right_layout.addWidget(self.to_date_edit)
        right_layout.addWidget(self.apply_filter_btn)
        
        # Add to header layout
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        header_layout.addLayout(right_layout)
        
        parent_layout.addLayout(header_layout)

    def create_table_section(self, parent_layout):
        """Create trade history table section"""
        # Create table frame - the container for both the summary and the table
        table_frame = QFrame()
        table_frame.setFrameShape(QFrame.StyledPanel)
        table_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_frame.setMinimumHeight(300)
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
        """)

        # Main layout for the table frame
        table_main_layout = QVBoxLayout(table_frame)
        table_main_layout.setContentsMargins(20, 15, 20, 15)
        table_main_layout.setSpacing(0)

        # Transaction summary - now inside the table frame
        summary_layout = QHBoxLayout()
        summary_layout.setContentsMargins(0, 0, 0, 15)

        # Create SVG calendar icon
        calendar_icon = QLabel()
        calendar_icon.setFixedSize(24, 24)

        # SVG content for the calendar icon
        svg_content = """
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 2v4"></path>
            <path d="M16 2v4"></path>
            <rect width="18" height="18" x="3" y="4" rx="2"></rect>
            <path d="M3 10h18"></path>
        </svg>
        """

        # Create a temporary file to store the SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as temp:
            temp.write(svg_content.encode('utf-8'))
            temp_path = temp.name

        # Load the SVG into a pixmap and set it to the label
        calendar_pixmap = QPixmap(temp_path)
        calendar_icon.setPixmap(calendar_pixmap)

        # לאחר השימוש – מומלץ למחוק את הקובץ הזמני
        os.remove(temp_path)

        # Transaction count label
        transaction_count = QLabel("35 transactions")
        transaction_count.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            margin-left: 5px;
            border: none;
            background: transparent;
        """)

        # Net total layout and labels
        net_total_layout = QHBoxLayout()
        net_total_label = QLabel("Net Total:")
        net_total_label.setStyleSheet("""
            color: #6B7280;
            font-size: 14px;
            font-weight: bold;
            border: none;
            background: transparent;
        """)

        self.net_total_value = QLabel("$10261.81")
        self.net_total_value.setStyleSheet("""
            color: #EF4444;
            font-size: 14px;
            font-weight: bold;
            border: none;
            background: transparent;                                           
        """)

        net_total_layout.addWidget(net_total_label)
        net_total_layout.addWidget(self.net_total_value)

        summary_layout.addWidget(calendar_icon)
        summary_layout.addWidget(transaction_count)
        summary_layout.addStretch()
        summary_layout.addLayout(net_total_layout)

        # Add summary to main layout of the table frame
        table_main_layout.addLayout(summary_layout)

        # Add a horizontal separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #E5E7EB;")
        separator.setFixedHeight(1)
        table_main_layout.addWidget(separator)
        table_main_layout.addSpacing(15)

        # Create table widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)

        # Set headers
        headers = ["Date", "Action", "Stock", "Quantity", "Price", "Total Amount"]
        self.table.setHorizontalHeaderLabels(headers)

        # Configure header appearance
        header = self.table.horizontalHeader()
        # שימוש במצב Fixed עבור העמודות (ללא Stretch)
        # header.setSectionResizeMode(QHeaderView.Fixed)
        header.setSectionResizeMode(QHeaderView.Stretch)

        for col in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(col)
            if item:
                if col in [3, 4, 5]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setMinimumHeight(250)

        # Style the table via stylesheet
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: transparent;
                outline: none;
            }
            QHeaderView::section {
                background-color: white;
                padding: 15px 10px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
                color: #6B7280;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                text-align: left;
            }
            QTableWidget::item {
                border-bottom: 1px solid #F3F4F6;
                padding: 0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #F9FAFB;
                color: #111827;
            }
        """)

        # שימוש ב־Delegate ליישור לימין בעמודות המספריות
        right_delegate = RightAlignedDelegate(padding=10, parent=self.table)
        self.table.setItemDelegateForColumn(3, right_delegate)
        self.table.setItemDelegateForColumn(4, right_delegate)
        self.table.setItemDelegateForColumn(5, right_delegate)

        # דוגמה להוספת נתונים לטבלה (אתה יכול להוסיף יותר שורות כראות עיניך)
        self.table.setRowCount(3)
        sample_data = [
            ["2023-10-05", "Buy", "AAPL", "10", "$150.00", "$1500.00"],
            ["2023-10-06", "Sell", "GOOG", "5", "$2800.00", "$14000.00"],
            ["2023-10-07", "Buy", "MSFT", "8", "$300.00", "$2400.00"]
        ]
        for row, row_data in enumerate(sample_data):
            for col, data in enumerate(row_data):
                item = QTableWidgetItem(data)
                # ליישור לימין במספרים (delegate דואג לכך, אך אפשר גם להגדיר כאן במפורש)
                if col in [3, 4, 5]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row, col, item)

        # הוספת הטבלה לתוך ה־layout של המסגרת
        table_main_layout.addWidget(self.table)
        parent_layout.addWidget(table_frame, 1)

    

    def adjust_item_display(self, item):
        """Adjust display properties of table items based on column"""
        row = item.row()
        col = item.column()
        
        # Set alignment based on column
        if col in [0, 1, 2]:  # Date, Action, Stock
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:  # Quantity, Price, Total Amount
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Set proper font
        font = QFont("Segoe UI", 10)
        if col == 1:  # Action column gets bold
            font.setBold(True)
        item.setFont(font)
        
        # Set proper text color
        if col == 5:  # Total Amount
            item.setForeground(QBrush(QColor("#000000")))
        else:
            item.setForeground(QBrush(QColor("#1F2937")))
            
        # Add more padding to first column
        if col == 0:
            self.table.setItemDelegateForColumn(0, LeftPaddingDelegate(16, self.table))

    def create_chart_section(self, parent_layout):
        """Create chart visualization section"""
        chart_title = QLabel("Performance Visualization")
        chart_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #111827;
            margin-top: 10px;
        """)
        parent_layout.addWidget(chart_title)
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        """)
        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(16, 16, 16, 16)
        
        # Chart controls
        controls_layout = QHBoxLayout()
        
        chart_toggle_button = QPushButton("Toggle Chart Type")
        chart_toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #37506D;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30455C;
            }
        """)
        chart_toggle_button.clicked.connect(self.toggle_chart_type)
        
        controls_layout.addStretch()
        controls_layout.addWidget(chart_toggle_button)
        
        # Create chart widget
        self.chart_widget = EnhancedChartWidget()
        self.chart_widget.setMinimumHeight(300)
        
        chart_layout.addLayout(controls_layout)
        chart_layout.addWidget(self.chart_widget)
        
        parent_layout.addWidget(chart_frame)

    def initialize_sample_data(self):
        """Populate the table with sample data to match the image"""
        # Set row count
        self.table.setRowCount(3)
        
        # Sample data
        data = [
            {
                "date": "Feb 1, 2024", 
                "action": "SELL", 
                "stock": "AAPL", 
                "quantity": 5, 
                "price": 185.75, 
                "total": 928.75
            },
            {
                "date": "Jan 20, 2024", 
                "action": "BUY", 
                "stock": "TSLA", 
                "quantity": 5, 
                "price": 220.00, 
                "total": 1100.00
            },
            {
                "date": "Jan 15, 2024", 
                "action": "BUY", 
                "stock": "AAPL", 
                "quantity": 10, 
                "price": 175.50, 
                "total": 1755.00
            }
        ]
        
        for row, trade in enumerate(data):
            # Date
            date_item = QTableWidgetItem(trade["date"])
            date_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            # Action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)
            
            # Create action badge with SVG
            action_badge = QLabel()
            
            if trade["action"] == "BUY":
                action_badge.setStyleSheet("""
                    background-color: #DCFCE7;
                    color: #166534;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 4px 8px;
                """)
                action_badge.setText("↑ BUY")  # Simple version for now
            else:
                action_badge.setStyleSheet("""
                    background-color: #FEE2E2;
                    color: #991B1B;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 4px 8px;
                """)
                action_badge.setText("↓ SELL")  # Simple version for now
            
            action_layout.addWidget(action_badge)
            action_layout.addStretch()
            
            # Stock
            stock_item = QTableWidgetItem(trade["stock"])
            stock_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(trade["quantity"]))
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Price
            price_item = QTableWidgetItem(f"${trade['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Total
            total_item = QTableWidgetItem(f"${trade['total']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Add items to table
            self.table.setItem(row, 0, date_item)
            self.table.setCellWidget(row, 1, action_widget)
            self.table.setItem(row, 2, stock_item)
            self.table.setItem(row, 3, quantity_item)
            self.table.setItem(row, 4, price_item)
            self.table.setItem(row, 5, total_item)
            
            # Set row height
            self.table.setRowHeight(row, 50)

    def update_trade_table(self, trade_history):
        """Update the trade table with actual data"""
        if not trade_history:
            return
            
        # Clear existing data
        self.table.setRowCount(0)
        self.table.setRowCount(len(trade_history))
        
        # Calculate net total
        net_total = 0
        
        for row, trade in enumerate(trade_history):
            # Date
            date_str = trade["date"].strftime("%b %d, %Y")
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            # Action
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            action_layout.setSpacing(5)
            
            # Create action badge with SVG
            action_badge = QLabel()
            
            if trade["action"] == "Buy":
                action_badge.setStyleSheet("""
                    background-color: #DCFCE7;
                    color: #166534;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 4px 8px;
                """)
                action_badge.setText("↑ BUY")
                net_total -= (trade["quantity"] * trade["price"])  # Subtract for buy
            else:
                action_badge.setStyleSheet("""
                    background-color: #FEE2E2;
                    color: #991B1B;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 4px 8px;
                """)
                action_badge.setText("↓ SELL")
                net_total += (trade["quantity"] * trade["price"])  # Add for sell
            
            action_layout.addWidget(action_badge)
            action_layout.addStretch()
            
            # Stock
            stock_item = QTableWidgetItem(trade["stock"])
            stock_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(trade["quantity"]))
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Price
            price_item = QTableWidgetItem(f"${trade['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Total
            total = trade["quantity"] * trade["price"]
            total_item = QTableWidgetItem(f"${total:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Add items to table
            self.table.setItem(row, 0, date_item)
            self.table.setCellWidget(row, 1, action_widget)
            self.table.setItem(row, 2, stock_item)
            self.table.setItem(row, 3, quantity_item)
            self.table.setItem(row, 4, price_item)
            self.table.setItem(row, 5, total_item)
            
            # Set row height
            self.table.setRowHeight(row, 50)
        
        # Update transaction count and net total
        transaction_count = len(trade_history)
        self.net_total_value.setText(f"${abs(net_total):.2f}")
        
        # Set net total color based on profit/loss
        if net_total > 0:
            self.net_total_value.setStyleSheet("color: #10B981; font-size: 14px; font-weight: bold;")
        else:
            self.net_total_value.setStyleSheet("color: #EF4444; font-size: 14px; font-weight: bold;")

    def update_chart(self, chart_data):
        """Update line chart with data"""
        print("Updating chart with data", chart_data)
        self.chart_widget.createLineChart(chart_data)
    
    def update_bar_chart(self, bar_chart_data):
        """Update bar chart with data"""
        print("📊 Updating Bar Chart with data:", bar_chart_data)
        self.chart_widget.createBarChart(bar_chart_data)
    
    def apply_filter(self):
        """Apply filters to trade history"""
        start_date = self.from_date_edit.date().toPython()
        end_date = self.to_date_edit.date().toPython()
        selected_action = self.action_combo.currentText()
        
        if selected_action == "All Actions":
            actions = ["Buy", "Sell"]
        else:
            actions = [selected_action]
            
        print(f"🔍 Sending filter request - Start: {start_date}, End: {end_date}, Actions: {actions}")
        
        self.presenter.filter_trade_history(start_date, end_date, [], actions)
    
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
    
    def open_dashboard(self):
        print("Opening Dashboard")

    def open_portfolio(self):
        print("Opening Portfolio")

    def open_market_overview(self):
        print("Opening Market Overview")

    def open_reports(self):
        print("Opening Reports & Analysis")

    def open_account_settings(self):
        print("Opening Account Settings")

    def open_performance(self):
        print("Opening Performance")

    def open_risk_analysis(self):
        print("Opening Risk Analysis")

    def open_documentation(self):
        print("Opening Documentation")

    def open_support(self):
        print("Opening Support")

    def open_about(self):
                print("Opening About")

    def open_buy_order(self):
        print("Opening Buy Order")
    
    def open_sell_order(self):
        print("Opening Sell Order")
        
    def open_trade_history(self):
        print("Opening Trade History")
        
    def open_ai_advisor(self):
        print("Opening AI Advisor")

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