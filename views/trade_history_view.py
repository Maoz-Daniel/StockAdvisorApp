import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QDateEdit, QComboBox, QFrame, QApplication,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QDate, QMargins
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis


# 🔹 מחלקה לגרף עם פריסה משופרת
class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 🔹 יצירת סדרת נתונים
        series = QLineSeries()
        demo_data = [(1, 10), (2, 15), (3, 7), (4, 20), (5, 12)]
        for x, y in demo_data:
            series.append(x, y)

        # 🎨 עיצוב הקו
        pen = QPen(QColor("#1F3B73"))
        pen.setWidth(3)
        series.setPen(pen)

        # 🔹 יצירת הגרף
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("")
        chart.setBackgroundVisible(False)
        chart.setMargins(QMargins(10, 10, 10, 10))

        # 🔹 יצירת צירים מעוצבים
        axisX = QValueAxis()
        axisX.setRange(0, 6)
        axisX.setTitleText("Time")
        axisX.setLabelsColor(QColor("#2C3E50"))

        axisY = QValueAxis()
        axisY.setRange(0, 25)
        axisY.setTitleText("Trade Value")
        axisY.setLabelsColor(QColor("#2C3E50"))

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.chart().legend().hide()

        # 🔹 התאמה אוטומטית לגודל המסך - הפחתת גובה לטובת הטבלה
        self.setFixedHeight(200)


# 🔹 מחלקה לחלון הראשי עם תיקוני פריסה
class TradeHistoryWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle("Trade History - SmartInvest Pro")

        # 🔹 קבלת גודל המסך והתאמה
        screen_size = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_size.x(), screen_size.y(), screen_size.width() * 0.85, screen_size.height() * 0.85)

        # 🔹 סגנון משופר
        self.setStyleSheet("""
    QMainWindow, QWidget {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        background-color: #F0F2F6;
    }
    
    QLabel {
        color: #1E293B;
        font-size: 16px;
        font-weight: normal;
        margin-bottom: 8px;
    }

    /* כותרת ראשית */
    .title-label {
        font-size: 28px;
        font-weight: bold;
        color: #0F2D5A;
        margin-bottom: 15px;
    }

    /* מסגרת מעוגלת לכל הטבלה */
    QTableWidget {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        gridline-color: #EDF2F7;
        selection-background-color: rgba(15, 45, 90, 0.15);
        selection-color: #0F2D5A;
        padding: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    QTableWidget::item {
        padding: 12px;
        border-bottom: 1px solid #EDF2F7;
        color: #334155;
    }
    
    QTableWidget::item:selected {
        background-color: rgba(15, 45, 90, 0.15);
        color: #0F2D5A;
        border-bottom: 1px solid #0F2D5A;
    }
    
    QHeaderView::section {
        background-color: #0F2D5A;
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
    }
    
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    
    QPushButton:pressed {
        background-color: #1E40AF;
    }
    
    /* עיצוב התאריכים והמניה - הגדלה קלה */
    QDateEdit, QComboBox {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
        padding: 8px;
        min-width: 135px;
        font-size: 14px;
        color: #334155;
    }
    
    QDateEdit:focus, QComboBox:focus {
        border: 1px solid #2563EB;
    }
    
    /* עיצוב לכותרות כמו "From:", "To:", "Stock:" */
    .filter-label {
        font-size: 14px;
        font-weight: bold;
        color: #475569;
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
""")

        # 🔹 תוכן ראשי
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 🔹 כותרת הדף
        title_label = QLabel("Trade History")
        title_label.setObjectName("title-label")
        title_label.setStyleSheet("""
        font-size: 30px;  /* גודל כותרת גדול ומרשים */
        font-weight: bold; /* טקסט מודגש */
        color: #1F3B73;  /* צבע כחול מקצועי */
        margin-bottom: 15px; /* הוספת ריווח מתחת לכותרת */
""")
        main_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        # 🔹 אזור סינון
        filter_container = QWidget()
        filter_layout = QHBoxLayout(filter_container)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        filter_layout.setSpacing(15)

        self.from_date_edit = QDateEdit()
        self.from_date_edit.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_edit.setCalendarPopup(True)

        self.to_date_edit = QDateEdit()
        self.to_date_edit.setDate(QDate.currentDate())
        self.to_date_edit.setCalendarPopup(True)

        self.stock_combo = QComboBox()
        self.stock_combo.addItems(["All Stocks", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"])

        filter_button = QPushButton("Apply Filter")
        filter_button.setFixedWidth(150)

        filter_layout.addWidget(QLabel("From:", parent=filter_container, objectName="filter-label"))
        filter_layout.addWidget(self.from_date_edit)
        filter_layout.addWidget(QLabel("To:", parent=filter_container, objectName="filter-label"))
        filter_layout.addWidget(self.to_date_edit)
        filter_layout.addWidget(QLabel("Stock:", parent=filter_container, objectName="filter-label"))
        filter_layout.addWidget(self.stock_combo)
        filter_layout.addWidget(filter_button)
        filter_layout.addStretch()

        main_layout.addWidget(filter_container)

        # 🔹 אזור הטבלה
        self.table = QTableWidget(5, 5)
        self.table.setHorizontalHeaderLabels(["Date", "Stock", "Action", "Quantity", "Unit Price"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(350)

        demo_data = [
            ("01/03/2024", "AAPL", "Buy", "10", "$175.50"),
            ("15/02/2024", "GOOGL", "Sell", "2", "$2,800.00"),
            ("10/02/2024", "MSFT", "Buy", "5", "$410.25"),
            ("01/02/2024", "TSLA", "Buy", "12", "$165.30"),
            ("25/01/2024", "AMZN", "Buy", "8", "$178.60")
        ]

        for row, row_data in enumerate(demo_data):
            for col, item in enumerate(row_data):
                table_item = QTableWidgetItem(item)
                table_item.setTextAlignment(Qt.AlignCenter)
                if col == 2:
                    table_item.setForeground(QColor("#27AE60") if item == "Buy" else QColor("#E74C3C"))
                self.table.setItem(row, col, table_item)

        main_layout.addWidget(self.table)

        # 🔹 אזור הגרף
        self.chart_widget = ChartWidget()
        main_layout.addWidget(self.chart_widget)

        self.setCentralWidget(central_widget)


# 🔹 הפעלת האפליקציה
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradeHistoryWindow("John Doe")
    window.show()
    sys.exit(app.exec())
