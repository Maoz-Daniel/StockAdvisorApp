import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))

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


class EnhancedChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        
        # יצירת מסגרת מעוצבת
        self.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
        """)
        
        # יצירת אפקט צל
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        

        
    def createLineChart(self,chart_data=[]):
        # יצירת סדרת נתונים משופרת
        print(f"📊 Creating Line Chart with: {chart_data}")  # בדיקה שהגרף מקבל נתונים
        series = QLineSeries()
        series.setName("Trade Value")
        
        if not chart_data:
            print("⚠️ No data for chart!")
            return  # אם אין נתונים, לא מציגים כלום
       
        
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

        # עיצוב הקו
        pen = QPen(QColor("#2563EB"))
        pen.setWidth(3)
        series.setPen(pen)

        # יצירת הגרף
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Trade Performance History")
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setTitleBrush(QColor("#1F3B73"))
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # יצירת צירים מעוצבים
        axisX = QValueAxis()
        axisX.setRange(0, 8)
        axisX.setTitleText("Week")
        axisX.setTitleFont(QFont("Segoe UI", 10))
        axisX.setLabelsColor(QColor("#475569"))
        axisX.setGridLineVisible(True)
        axisX.setGridLineColor(QColor("#EDF2F7"))
        axisX.setTickCount(8)

        axisY = QValueAxis()
        axisY.setRange(min_y-100, max_y+100) 
        axisY.setTitleText("Value ($)")
        axisY.setTitleFont(QFont("Segoe UI", 10))
        axisY.setLabelsColor(QColor("#475569"))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor("#EDF2F7"))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        # התאמת הסגנון של המקרא
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 9))
        
        self.setChart(chart)
        
    def createBarChart(self, bar_chart_data=[]):
        """ יצירת גרף עמודות על בסיס הנתונים מה-Presenter """
        print(f"📊 Creating Bar Chart with: {bar_chart_data}")

        if not bar_chart_data:
            print("⚠️ No data for bar chart!")
            return

        barSet = QBarSet("Trades")

        # הוספת הנתונים לגרף
        for stock, count in bar_chart_data:
            barSet.append(count)

        barSet.setColor(QColor("#2563EB"))
        series = QBarSeries()
        series.append(barSet)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Number of Trades per Stock")
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setTitleBrush(QColor("#1F3B73"))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundVisible(False)

        categories = [stock for stock, _ in bar_chart_data]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        axisX.setLabelsFont(QFont("Segoe UI", 9))
        axisX.setLabelsColor(QColor("#475569"))

        axisY = QValueAxis()
        axisY.setRange(0, max(count for _, count in bar_chart_data) + 2)
        axisY.setTitleText("Number of Trades")
        axisY.setTitleFont(QFont("Segoe UI", 10))
        axisY.setLabelsColor(QColor("#475569"))
        axisY.setGridLineVisible(True)
        axisY.setGridLineColor(QColor("#EDF2F7"))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.setChart(chart)



# 🔹 מחלקה לחלון הראשי עם שיפורים
class TradeHistoryWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"Trade History - SmartInvest Pro - {username}")

        # 🔹 קבלת גודל המסך והתאמה
        screen_size = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_size.x(), screen_size.y(), screen_size.width() * 0.85, screen_size.height() * 0.85)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 🔹 סגנון משופר
        self.setStyleSheet("""
    QMainWindow, QWidget {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        background-color: #F5F8FB;
    }
    
    QLabel {
        color: #1E293B;
        font-size: 16px;
        font-weight: normal;
        margin-bottom: 8px;
    }

    /* כותרת ראשית */
    #title-label {
        font-size: 30px;
        font-weight: bold;
        color: #1F3B73;
        margin-bottom: 15px;
    }
    
    #subtitle-label {
        font-size: 16px;
        color: #64748B;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* מסגרת מעוגלת לכל הטבלה */
    QTableWidget {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        gridline-color: #EDF2F7;
        selection-background-color: rgba(37, 99, 235, 0.15);
        selection-color: #1E40AF;
        padding: 5px;
    }
    
    QTableWidget::item {
        padding: 12px;
        border-bottom: 1px solid #EDF2F7;
        color: #334155;
    }
    
    QTableWidget::item:selected {
        background-color: rgba(37, 99, 235, 0.15);
        color: #1E40AF;
        border-bottom: 1px solid #1E40AF;
    }
    
    QHeaderView::section {
        background-color: #1F3B73;
        color: white;
        padding: 14px;
        font-size: 15px;
        font-weight: bold;
        border: none;
    }
    
    QHeaderView::section:first {
        border-top-left-radius: 8px;
    }
    
    QHeaderView::section:last {
        border-top-right-radius: 8px;
    }
    
    QPushButton {
        background-color: #2563EB;
        color: white;
        padding: 10px 18px;
        border-radius: 6px;
        font-weight: bold;
        border: none;
        min-height: 38px;
    }
    
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    
    QPushButton:pressed {
        background-color: #1E40AF;
    }
    
    QPushButton#chart-toggle-button {
        background-color: #475569;
        padding: 8px 15px;
    }
    
    QPushButton#chart-toggle-button:hover {
        background-color: #334155;
    }
    
    QPushButton#export-button {
        background-color: #10B981;
    }
    
    QPushButton#export-button:hover {
        background-color: #059669;
    }
    
    /* עיצוב התאריכים והמניה */
    QDateEdit, QComboBox {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 8px;
        min-width: 145px;
        min-height: 38px;
        font-size: 14px;
        color: #334155;
    }
    
    QDateEdit:focus, QComboBox:focus {
        border: 1px solid #2563EB;
    }
    
    QCheckBox {
        font-size: 14px;
        color: #475569;
        spacing: 8px;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid #CBD5E1;
    }
    
    QCheckBox::indicator:checked {
        background-color: #2563EB;
        border: 1px solid #2563EB;
    }
    
    /* עיצוב לכותרות כמו "From:", "To:", "Stock:" */
    #filter-label {
        font-size: 14px;
        font-weight: bold;
        color: #475569;
    }
    
    /* מסגרת לאזור הסינון */
    #filter-frame, #action-frame {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 15px;
    }
    
    /* עיצוב מיוחד לערכים חיוביים/שליליים */
    .positive-value {
        color: #10B981;
        font-weight: 600;
    }
    
    .negative-value {
        color: #EF4444;
        font-weight: 600;
    }
    
    /* סרגל גלילה מותאם */
    QScrollBar:vertical {
        background: #F1F5F9;
        width: 10px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical {
        background: #CBD5E1;
        border-radius: 5px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #94A3B8;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    /* עיצוב אזור הגלילה */
    QScrollArea {
        border: none;
        background-color: transparent;
    }
""")

        # הוספת אזור גלילה לחלון הראשי
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll_area)
        
        # 🔹 תוכן ראשי עטוף בתוך QWidget
        content_widget = QWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # הגדרת אזור הגלילה להשתמש ב-content_widget
        scroll_area.setWidget(content_widget)

        # 🔹 כותרת הדף
        title_layout = QVBoxLayout()        

        title_label = QLabel("Trade History Dashboard")
        title_label.setObjectName("title-label")
        
        subtitle_label = QLabel(f"View and analyze your trading activity - {username}")
        subtitle_label.setObjectName("subtitle-label")
        subtitle_label.setStyleSheet("font-size: 16px; color: #64748B; margin-top: 8px;")  # 📌 דוחף את הטקסט מעט למטה

        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        main_layout.addLayout(title_layout)

        # 🔹 שורת פעולות עליונה
        action_frame = QFrame()
        action_frame.setObjectName("action-frame")
        action_layout = QHBoxLayout(action_frame)
        action_layout.setContentsMargins(15, 15, 15, 15)
        
        stats_layout = QVBoxLayout()
        
        trading_summary = QLabel("Trading summary:")
        trading_summary.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F3B73; margin-bottom: 2px;")
        
        statistics_label = QLabel("Total Trades: 32 | Buy: 24 | Sell: 8 | Avg. Price: $485.50")
        statistics_label.setStyleSheet("font-size: 14px; color: #475569; margin-top: 0px;")
        
        stats_layout.addWidget(trading_summary)
        stats_layout.addWidget(statistics_label)
        
        chart_toggle_button = QPushButton("Toggle Chart Type")
        chart_toggle_button.setObjectName("chart-toggle-button")
        chart_toggle_button.setFixedWidth(150)
        
        export_button = QPushButton("Export Data")
        export_button.setObjectName("export-button")
        export_button.setFixedWidth(130)
        
        action_layout.addLayout(stats_layout)
        action_layout.addStretch()
        action_layout.addWidget(chart_toggle_button)
        action_layout.addWidget(export_button)
        
        main_layout.addWidget(action_frame)

        # 🔹 אזור סינון משודרג
        filter_frame = QFrame()
        filter_frame.setObjectName("filter-frame")
        filter_layout = QGridLayout(filter_frame)
        
        filter_layout.setContentsMargins(8, 8, 8, 8)  # 📌 מקטין את הרווחים הפנימיים
        filter_layout.setHorizontalSpacing(8)  # 📌 מקטין את המרווחים בין האלמנטים
        filter_layout.setVerticalSpacing(6)  # 📌 מקטין את המרווחים בין השורות
        filter_frame.setFixedHeight(200)  # 📌 מגביל את גובה המסגרת
        filter_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


        # מרכיבי סינון
        from_label = QLabel("From:")
        from_label.setObjectName("filter-label")
        
        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_edit.setCalendarPopup(True)
        self.from_date_edit.setFixedSize(140, 35)

        to_label = QLabel("To:")
        to_label.setObjectName("filter-label")
        
        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate.currentDate())
        self.to_date_edit.setCalendarPopup(True)
        self.to_date_edit.setFixedSize(140, 35)

        stock_label = QLabel("Stock:")
        stock_label.setObjectName("filter-label")
        
        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["All Stocks", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"])
        self.stock_combo.setFixedSize(160, 35)  # 📌 מקטין את שדה המניה
        self.stock_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  


        transaction_label = QLabel("Transaction:")
        transaction_label.setObjectName("filter-label")
        
        transaction_layout = QHBoxLayout()
        self.buy_checkbox = QCheckBox("Buy")
        self.buy_checkbox.setChecked(True)
        self.sell_checkbox = QCheckBox("Sell")
        self.sell_checkbox.setChecked(True)
        self.buy_checkbox.setStyleSheet("font-size: 16px; padding: 6px;")  # 📌 מגדיל טקסט
        self.sell_checkbox.setStyleSheet("font-size: 16px; padding: 6px;")
        
        transaction_layout.addWidget(self.buy_checkbox)
        transaction_layout.addWidget(self.sell_checkbox)
        transaction_layout.addStretch()

        filter_button = QPushButton("Apply Filter")
        filter_button.setFixedWidth(120)
        filter_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        filter_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  
        filter_button.clicked.connect(self.apply_filter)

        
        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("background-color: #64748B;")
        reset_button.clicked.connect(self.reset_filters)
        reset_button.setFixedWidth(90)
        

        # הוספת הרכיבים לגריד
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

        main_layout.addWidget(filter_frame)

        # 🔹 אזור הטבלה המשודרג
        self.table = QTableWidget(8, 6)  # הוספת עמודה נוספת ושורות נוספות
        self.table.setHorizontalHeaderLabels(["Date", "Stock", "Action", "Quantity", "Unit Price", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(300)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(self.table)

        # אפקט צל לטבלה
        table_shadow = QGraphicsDropShadowEffect(self.table)
        table_shadow.setBlurRadius(15)
        table_shadow.setColor(QColor(0, 0, 0, 25))
        table_shadow.setOffset(0, 2)
        self.table.setGraphicsEffect(table_shadow)

        # 🔹 אזור הגרף המשודרג
        self.chart_widget = EnhancedChartWidget()
        self.chart_widget.setMinimumHeight(280)
        main_layout.addWidget(self.chart_widget, stretch=1)
        
        # חיבור כפתור החלפת סוג תרשים
        chart_toggle_button.clicked.connect(self.toggle_chart_type)
        
        # משתנה פנימי לסוג התרשים הנוכחי
        # self.current_chart_type = "bar"

        self.presenter=TradeHistoryPresenter(self)
        self.presenter.load_trade_history()
        self.presenter.load_trade_chart_data()
        self.presenter.load_trade_bar_chart_data()

        
    def update_chart(self,chart_data):
        print("updae chart with data",chart_data)
        self.chart_widget.createLineChart(chart_data)
    
    def update_bar_chart(self, bar_chart_data):
        """ מעדכן את גרף העמודות עם הנתונים מה-Presenter """
        print("📊 Updating Bar Chart with data:", bar_chart_data)
        self.chart_widget.createBarChart(bar_chart_data)

    
    def update_trade_table(self, trade_history):
        print(f"✅ update_trade_table() called with {len(trade_history)} trades")

        # 🛠 ניקוי נתונים ישנים מהטבלה
        self.table.clearContents()
        self.table.setRowCount(len(trade_history))

        if not trade_history:
            print("⚠️ No trades to display!")
            return

        for row, trade in enumerate(trade_history):
            print(f"🔹 Adding row {row}: {trade}")
            self.table.setItem(row, 0, QTableWidgetItem(trade["date"].strftime("%Y-%m-%d")))
            self.table.setItem(row, 1, QTableWidgetItem(trade["stock"]))
            self.table.setItem(row, 2, QTableWidgetItem(trade["action"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(trade["quantity"])))
            self.table.setItem(row, 4, QTableWidgetItem(f"${trade['price']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"${trade['quantity'] * trade['price']:.2f}"))

    
    def apply_filter(self):
        """ שולח בקשת סינון ל-Presenter """
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

        self.presenter.filter_trade_history(start_date, end_date, stocks, selected_action)  # ✅ שולח את הבקשה ל-Presenter

    def reset_filters(self):
        """ מאפס את כל השדות בטופס ומציג מחדש את כל העסקאות """
        print("🔄 Resetting filters to default values...")

        # 🛠 איפוס כל שדות הסינון
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.to_date_edit.setDate(QDate.currentDate())
        self.stock_combo.setCurrentIndex(0)  # מחזיר ל- "All Stocks"
        self.buy_checkbox.setChecked(True)
        self.sell_checkbox.setChecked(True)

        # 🔄 טוען מחדש את כל העסקאות
        self.presenter.load_trade_history()
    

    def toggle_chart_type(self):
        """מפעילה את החלפת סוג הגרף דרך ה-Presenter"""
        self.presenter.toggle_chart_type()
        
        # אם רוצים לשמור על אנימציה בממשק, ניתן להשאיר אותה כאן (כחלק מה-View בלבד):
        animation = QPropertyAnimation(self.chart_widget, b"geometry")
        animation.setDuration(300)
        animation.setStartValue(self.chart_widget.geometry())
        animation.setEndValue(self.chart_widget.geometry())
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.start()


# 🔹 הפעלת האפליקציה
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradeHistoryWindow("John Doe")
    window.show()
    
    # תמיכה ב-High DPI
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    sys.exit(app.exec())