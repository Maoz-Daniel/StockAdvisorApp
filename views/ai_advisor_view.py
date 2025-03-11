from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QApplication, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QColor


class AIAdvisorWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle("AI Advisor - SmartInvest Pro")

        # 📌 התאמה דינמית של החלון
        self.setMinimumSize(850, 600)
        self.resize(1100, 750)  

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
        """)

        # 🔹 **יצירת ממשק מרכזי**
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 🔹 **תיבה עליונה מוקטנת (Header)**
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(140)  # 🔹 מקטין את ה-Header אבל שומר על מקום לטקסט
        self.header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2956B2, stop:1 #4A7CE0);
                border-radius: 12px;
                border: none;
                padding: 5px;
            }
        """)
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(15, 5, 15, 5)  # 🔹 יותר מקום לטקסט

        title_label = QLabel("🤖 AI Advisor Insights")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 🔹 מבטיח שהטקסט יהיה נראה
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")

        subtitle_label = QLabel("Your intelligent financial companion")
        subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 🔹 גם הכותרת המשנית מיושרת נכון
        subtitle_label.setStyleSheet("font-size: 14px; font-weight: normal; color: rgba(255, 255, 255, 0.8);")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **אזור הגלילה המרכזי ל-Insights**
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(15)

        # 🔹 **כרטיס מידע עם תובנות AI**
        insights_card = self.create_info_card()
        self.scroll_layout.addWidget(insights_card)

        # מוסיף מרווח אוטומטי בתחתית אזור הגלילה
        self.scroll_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # 🔹 **כפתור ניתוח AI**
        self.analysis_button = QPushButton("🔍 Perform AI Analysis")
        self.analysis_button.clicked.connect(self.run_ai_analysis)
        self.analysis_button.setCursor(Qt.PointingHandCursor)
        self.analysis_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # כפתור מתרחב לרוחב
        self.main_layout.addWidget(self.analysis_button, alignment=Qt.AlignCenter)

        self.setCentralWidget(central_widget)

    def create_info_card(self):
        """ יוצר כרטיס מידע עם תובנות AI """
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: white; 
            border-radius: 12px; 
            padding: 20px;
            border-top: 4px solid #2956B2;
        """)
        self.add_shadow_effect(frame)

        layout = QVBoxLayout(frame)
        layout.setSpacing(10)

        insights_label = QLabel("📊 AI Market Insights (Demo Data)")
        insights_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")

        insights_text = QLabel("""
✔ **Technology stocks** expected to rise in Q2 2024 📈  
✔ **Energy sector** remains stable despite market fluctuations  
✔ AI recommends **adding NVDA & AAPL** to your portfolio 🚀  
✔ **Risk alert:** High volatility detected in crypto market! ⚠  
        """)
        insights_text.setStyleSheet("font-size: 18px; color: #4A5568;")
        insights_text.setWordWrap(True)

        layout.addWidget(insights_label)
        layout.addWidget(insights_text)

        return frame

    def run_ai_analysis(self):
        """ מציג אנימציה קטנה של טעינה ומציג תובנה נוספת לאחר 2 שניות """
        self.analysis_button.setText("🔄 Analyzing...")
        self.analysis_button.setDisabled(True)

        QTimer.singleShot(2000, lambda: self.display_new_insight())

    def display_new_insight(self):
        """ מוסיף תובנה חדשה לאחר לחיצה על ניתוח AI """
        self.analysis_button.setText("✅ AI Analysis Complete")
        new_insight = QLabel("✔ AI suggests **diversifying** portfolio with **renewable energy stocks**! 🌱")
        new_insight.setStyleSheet("font-size: 18px; color: #2C3E50; font-weight: bold;")
        self.scroll_layout.insertWidget(0, new_insight)

    def add_shadow_effect(self, widget):
        """ מוסיף אפקט צל אלגנטי """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        widget.setGraphicsEffect(shadow)


# ✅ **הרצת החלון**
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AIAdvisorWindow("John Doe")
    window.show()

    # תמיכה ב-High DPI
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    sys.exit(app.exec())
