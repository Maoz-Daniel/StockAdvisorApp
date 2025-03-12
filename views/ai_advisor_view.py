from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QApplication, QScrollArea, QSizePolicy,
    QHBoxLayout, QProgressBar, QSpacerItem
)
from PySide6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont, QIcon


class AIAdvisorWindow(QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.username = username
        self.setWindowTitle("AI Advisor - SmartInvest Pro")

        self.last_refresh_time = "Just now"  


        # 📌 התאמה דינמית של החלון
        self.setMinimumSize(850, 600)
        self.resize(1100, 750)  

        # 📌 עיצוב כללי - מודרני יותר
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
            QPushButton:disabled {
                background-color: #7998D5;
            }
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 15px;
                border: 1px solid #D0E1FF;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #E0E7F7;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4A7CE0;
                border-radius: 4px;
            }
        """)

        # 🔹 **יצירת ממשק מרכזי**
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 🔹 **תיבה עליונה עם מידע אישי**
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(140)
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

        # 🆕 שורה עליונה עם שם משתמש
        top_header_layout = QHBoxLayout()
        
        title_label = QLabel("🤖 AI Advisor Insights")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        welcome_label = QLabel(f"Welcome, {username}")
        welcome_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        welcome_label.setStyleSheet("font-size: 16px; color: white; font-weight: normal;")
        
        top_header_layout.addWidget(title_label)
        top_header_layout.addWidget(welcome_label)
        
        subtitle_label = QLabel("Your intelligent financial companion")
        subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        subtitle_label.setStyleSheet("font-size: 14px; font-weight: normal; color: rgba(255, 255, 255, 0.8);")

        header_layout.addLayout(top_header_layout)
        header_layout.addWidget(subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # 🔹 **אזור הגלילה המרכזי ל-Insights**
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #F0F5FF;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #BBD0FF;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(15)

        # 🆕 כרטיס סיכום נכסים
        portfolio_summary = self.create_portfolio_summary()
        self.scroll_layout.addWidget(portfolio_summary)
        
        # 🔹 **כרטיס מידע עם תובנות AI**
        insights_card = self.create_info_card()
        self.scroll_layout.addWidget(insights_card)

        # מוסיף מרווח אוטומטי בתחתית אזור הגלילה
        self.scroll_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # 🆕 שורת כפתורים תחתונה
        buttons_layout = QHBoxLayout()
        
        self.analysis_button = QPushButton("🔍 Perform AI Analysis")
        self.analysis_button.clicked.connect(self.run_ai_analysis)
        self.analysis_button.setCursor(Qt.PointingHandCursor)
        
        # 🆕 כפתור נוסף
        self.portfolio_button = QPushButton("📊 Portfolio Optimizer")
        self.portfolio_button.setStyleSheet("""
            background-color: #21A366;
        """)
        self.portfolio_button.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(self.analysis_button)
        buttons_layout.addWidget(self.portfolio_button)
        
        self.main_layout.addLayout(buttons_layout)

        self.setCentralWidget(central_widget)
        
        # 🆕 שעון עדכון אחרון
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_last_refresh)
        self.update_timer.start(60000)  # עדכון כל דקה
        self.last_refresh_time = "Just now"

    def create_portfolio_summary(self):
        """ יוצר כרטיס סיכום תיק השקעות """
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: white; 
            border-radius: 12px; 
            padding: 20px;
            border-left: 4px solid #21A366;
        """)
        self.add_shadow_effect(frame)

        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        # כותרת הכרטיס
        title_layout = QHBoxLayout()
        
        summary_label = QLabel("💼 Portfolio Summary")
        summary_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        
        refresh_label = QLabel(f"Last update: {self.last_refresh_time}")
        refresh_label.setObjectName("refresh_label")
        refresh_label.setStyleSheet("font-size: 14px; color: #7F8C9D; font-weight: normal;")
        refresh_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        title_layout.addWidget(summary_label)
        title_layout.addWidget(refresh_label)
        
        layout.addLayout(title_layout)

        # מידע על התיק
        portfolio_info = QLabel("Total value: $127,540 | YTD Return: +8.4% | Risk Level: Moderate")
        portfolio_info.setStyleSheet("font-size: 16px; color: #4A5568; font-weight: normal;")
        layout.addWidget(portfolio_info)
        
        # סרגל התקדמות - ביצועים מול יעד
        progress_layout = QHBoxLayout()
        
        progress_label = QLabel("Progress to annual goal:")
        progress_label.setStyleSheet("font-size: 16px; color: #4A5568; font-weight: normal;")
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(65)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(8)
        
        progress_value = QLabel("65%")
        progress_value.setStyleSheet("font-size: 16px; color: #21A366; font-weight: bold;")
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(progress_bar)
        progress_layout.addWidget(progress_value)
        
        layout.addLayout(progress_layout)

        return frame

    def create_info_card(self):
        """ יוצר כרטיס מידע עם תובנות AI - עם עיצוב משופר """
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: white; 
            border-radius: 12px; 
            padding: 20px;
            border-top: 4px solid #2956B2;
        """)
        self.add_shadow_effect(frame)

        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        insights_label = QLabel("📊 AI Market Insights (Demo Data)")
        insights_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")

        # שיפור עיצוב התובנות עם אייקונים ותבליטים
        insights_text = QLabel("""
<span style="font-size: 18px; color: #4A5568;">
• <b>Technology stocks</b> expected to rise in Q2 2024 <span style="color: #21A366;">📈</span><br>
• <b>Energy sector</b> remains stable despite market fluctuations <span style="color: #3498DB;">📊</span><br>
• AI recommends <b>adding NVDA & AAPL</b> to your portfolio <span style="color: #21A366;">🚀</span><br>
• <b>Risk alert:</b> High volatility detected in crypto market! <span style="color: #E74C3C;">⚠️</span>
</span>
        """)
        insights_text.setTextFormat(Qt.RichText)
        insights_text.setWordWrap(True)

        layout.addWidget(insights_label)
        layout.addWidget(insights_text)

        return frame

    def run_ai_analysis(self):
        """ מציג אנימציה קטנה של טעינה ומציג תובנה נוספת לאחר 2 שניות """
        self.analysis_button.setText("🔄 Analyzing...")
        self.analysis_button.setDisabled(True)
        
        # 🆕 אנימציה וטיימר לסימולציית ניתוח
        for frame in self.findChildren(QFrame):
            # יוצר אפקט הבהוב קל לכל הכרטיסים
            animation = QPropertyAnimation(frame, b"geometry")
            animation.setDuration(300)
            animation.setStartValue(frame.geometry())
            animation.setEndValue(frame.geometry())
            animation.setEasingCurve(QEasingCurve.OutBack)
            animation.start()

        QTimer.singleShot(2000, lambda: self.display_new_insight())

    def display_new_insight(self):
        """ מוסיף תובנה חדשה לאחר לחיצה על ניתוח AI """
        self.analysis_button.setText("✅ AI Analysis Complete")
        QTimer.singleShot(1500, lambda: self.analysis_button.setEnabled(True))
        QTimer.singleShot(1500, lambda: self.analysis_button.setText("🔍 Perform AI Analysis"))
        
        # 🆕 תיבת תובנה חדשה משודרגת
        new_insight_frame = QFrame()
        new_insight_frame.setStyleSheet("""
            background-color: #EBF5FF; 
            border-radius: 12px; 
            padding: 15px;
            border-left: 4px solid #3498DB;
        """)
        
        insight_layout = QVBoxLayout(new_insight_frame)
        insight_layout.setContentsMargins(10, 10, 10, 10)
        
        new_label = QLabel("🆕 NEW AI INSIGHT")
        new_label.setStyleSheet("font-size: 14px; color: #3498DB; font-weight: bold;")
        
        new_insight = QLabel("AI suggests <b>diversifying</b> your portfolio with <b>renewable energy stocks</b>! " +
                            "Consider adding <b>NEE</b> and <b>ENPH</b> to benefit from the green energy trend. 🌱")
        new_insight.setStyleSheet("font-size: 16px; color: #2C3E50;")
        new_insight.setWordWrap(True)
        
        insight_layout.addWidget(new_label)
        insight_layout.addWidget(new_insight)
        
        self.add_shadow_effect(new_insight_frame)
        self.scroll_layout.insertWidget(1, new_insight_frame)
        
        # עדכון שעון רענון אחרון
        self.update_last_refresh()

    def update_last_refresh(self):
        """ מעדכן את זמן הרענון האחרון """
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        self.last_refresh_time = current_time
        
        refresh_label = self.findChild(QLabel, "refresh_label")
        if refresh_label:
            refresh_label.setText(f"Last update: {self.last_refresh_time}")

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