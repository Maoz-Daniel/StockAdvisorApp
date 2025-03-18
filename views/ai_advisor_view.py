from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, 
    QGraphicsDropShadowEffect, QApplication, QScrollArea, QSizePolicy,
    QHBoxLayout, QProgressBar, QSpacerItem
)
from PySide6.QtCore import Qt, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QFont, QIcon
from presenters.ai_advisor_presenter import AIAdvisorPresenter

# Import luxury theme colors
from assets.theme import LuxuryTheme

class AIAdvisorWindow(QMainWindow):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.username = model.get_username()
        self.setWindowTitle("AI Advisor - SmartInvest Pro")
        self.last_refresh_time = "Just now"  

        # Window settings
        self.setMinimumSize(850, 600)
        self.resize(1100, 750)  

        # Apply general styling from the theme colors
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                background-color: {LuxuryTheme.DARK_BLUE};
            }}
            QLabel {{
                color: {LuxuryTheme.TEXT_LIGHT};
                font-size: 22px;
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {LuxuryTheme.NAVY};
                color: {LuxuryTheme.TEXT_LIGHT};
                padding: 12px 25px;
                border-radius: 8px;
                font-weight: bold;
                border: 1px solid {LuxuryTheme.HIGHLIGHT_BLUE};
                font-size: 16px;
                min-height: 48px;
            }}
            QPushButton:hover {{
                background-color: {LuxuryTheme.HIGHLIGHT_BLUE};
                color: {LuxuryTheme.ELECTRIC_BLUE};
            }}
            QPushButton:disabled {{
                background-color: rgba(30, 73, 118, 0.5);
            }}
            QFrame {{
                background-color: {LuxuryTheme.NAVY};
                border-radius: 12px;
                padding: 15px;
                border: 1px solid {LuxuryTheme.HIGHLIGHT_BLUE};
            }}
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: rgba(30, 73, 118, 0.5);
                height: 8px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {LuxuryTheme.GOLD};
                border-radius: 4px;
            }}
        """)

        # Create central widget and main layout
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Create header
        self.header_frame = QFrame()
        self.header_frame.setFixedHeight(140)
        self.header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {LuxuryTheme.DARK_BLUE}, stop:1 {LuxuryTheme.NAVY});
                border-radius: 12px;
                border: 1px solid {LuxuryTheme.HIGHLIGHT_BLUE};
                border-bottom: 2px solid {LuxuryTheme.GOLD};
                padding: 5px;
            }}
        """)
        header_layout = QVBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        top_header_layout = QHBoxLayout()
        
        title_label = QLabel("🤖 AI Advisor Insights")
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {LuxuryTheme.TEXT_WHITE};")
        
        welcome_label = QLabel(f"Welcome, {self.username}")
        welcome_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        welcome_label.setStyleSheet(f"font-size: 16px; color: {LuxuryTheme.GOLD}; font-weight: normal;")
        
        top_header_layout.addWidget(title_label)
        top_header_layout.addWidget(welcome_label)
        
        subtitle_label = QLabel("Your intelligent financial companion")
        subtitle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        subtitle_label.setStyleSheet(f"font-size: 14px; font-weight: normal; color: {LuxuryTheme.TEXT_GRAY};")
        
        header_layout.addLayout(top_header_layout)
        header_layout.addWidget(subtitle_label)
        self.main_layout.addWidget(self.header_frame)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background: {LuxuryTheme.DARK_BLUE};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {LuxuryTheme.HIGHLIGHT_BLUE};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {LuxuryTheme.ELECTRIC_BLUE};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(15)

        # Portfolio summary card
        portfolio_summary = self.create_portfolio_summary()
        self.scroll_layout.addWidget(portfolio_summary)
        
        # AI insights card
        insights_card = self.create_info_card()
        self.scroll_layout.addWidget(insights_card)

        # Add spacing at the bottom
        self.scroll_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Bottom buttons row
        buttons_layout = QHBoxLayout()
        self.analysis_button = QPushButton("🔍 Perform AI Analysis")
        self.analysis_button.setObjectName("gold-button")
        self.analysis_button.setStyleSheet(f"""
            background-color: {LuxuryTheme.NAVY};
            color: {LuxuryTheme.GOLD};
            border: 1px solid {LuxuryTheme.GOLD};
            border-left: 3px solid {LuxuryTheme.BRIGHT_GOLD};
            border-right: 3px solid {LuxuryTheme.BRIGHT_GOLD};
        """)
        self.analysis_button.clicked.connect(self.run_ai_analysis)
        self.analysis_button.setCursor(Qt.PointingHandCursor)
        
        self.portfolio_button = QPushButton("📊 Portfolio Optimizer")
        self.portfolio_button.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(self.analysis_button)
        buttons_layout.addWidget(self.portfolio_button)
        self.main_layout.addLayout(buttons_layout)

        self.setCentralWidget(central_widget)
        
        # Refresh timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_last_refresh)
        self.update_timer.start(60000)  # Update every minute
        self.last_refresh_time = "Just now"

        # Create presenter instance
        self.presenter = AIAdvisorPresenter(self, model)

    # ------------------ UI Component Creation Methods ------------------
    def create_portfolio_summary(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            background-color: {LuxuryTheme.NAVY}; 
            border-radius: 12px; 
            padding: 20px;
            border-left: 4px solid {LuxuryTheme.GOLD};
        """)
        self.add_shadow_effect(frame, gold=True)

        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        title_layout = QHBoxLayout()
        
        summary_label = QLabel("💼 Portfolio Summary")
        summary_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {LuxuryTheme.GOLD};")
        
        refresh_label = QLabel(f"Last update: {self.last_refresh_time}")
        refresh_label.setObjectName("refresh_label")
        refresh_label.setStyleSheet(f"font-size: 14px; color: {LuxuryTheme.TEXT_GRAY}; font-weight: normal;")
        refresh_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        title_layout.addWidget(summary_label)
        title_layout.addWidget(refresh_label)
        
        layout.addLayout(title_layout)

        portfolio_info = QLabel("Total value: $127,540 | YTD Return: +8.4% | Risk Level: Moderate")
        portfolio_info.setStyleSheet(f"font-size: 16px; color: {LuxuryTheme.TEXT_LIGHT}; font-weight: normal;")
        layout.addWidget(portfolio_info)
        
        progress_layout = QHBoxLayout()
        
        progress_label = QLabel("Progress to annual goal:")
        progress_label.setStyleSheet(f"font-size: 16px; color: {LuxuryTheme.TEXT_LIGHT}; font-weight: normal;")
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(65)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(8)
        
        progress_value = QLabel("65%")
        progress_value.setStyleSheet(f"font-size: 16px; color: {LuxuryTheme.GOLD}; font-weight: bold;")
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(progress_bar)
        progress_layout.addWidget(progress_value)
        
        layout.addLayout(progress_layout)

        return frame

    def create_info_card(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            background-color: {LuxuryTheme.NAVY}; 
            border-radius: 12px; 
            padding: 20px;
            border-top: 4px solid {LuxuryTheme.GOLD};
        """)
        self.add_shadow_effect(frame, gold=True)

        layout = QVBoxLayout(frame)
        layout.setSpacing(15)

        insights_label = QLabel("📊 AI Market Insights")
        insights_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {LuxuryTheme.GOLD};")

        # Get insights from model
        advice = self.model.get_ai_advice("market trends")
        
        insights_text = QLabel(f"""
<span style="font-size: 16px; color: {LuxuryTheme.TEXT_LIGHT};">
• {advice} <span style="color: {LuxuryTheme.POSITIVE_GREEN};">📈</span><br><br>
• <b>Energy sector</b> remains stable despite market fluctuations <span style="color: {LuxuryTheme.ELECTRIC_BLUE};">📊</span><br><br>
• AI recommends <b>adding NVDA & AAPL</b> to your portfolio <span style="color: {LuxuryTheme.POSITIVE_GREEN};">🚀</span><br><br>
• <b>Risk alert:</b> High volatility detected in crypto market! <span style="color: {LuxuryTheme.NEGATIVE_RED};">⚠️</span>
</span>
        """)
        insights_text.setTextFormat(Qt.RichText)
        insights_text.setWordWrap(True)

        layout.addWidget(insights_label)
        layout.addWidget(insights_text)

        return frame

    # ------------------ UI Update Methods ------------------
    def update_analysis_button_text(self, text):
        self.analysis_button.setText(text)

    def set_analysis_button_enabled(self, enabled):
        self.analysis_button.setEnabled(enabled)

    def add_new_insight(self, insight_text):
        new_insight_frame = QFrame()
        new_insight_frame.setStyleSheet(f"""
            background-color: rgba(44, 90, 140, 0.3); 
            border-radius: 12px; 
            padding: 15px;
            border-left: 4px solid {LuxuryTheme.GOLD};
        """)
        insight_layout = QVBoxLayout(new_insight_frame)
        insight_layout.setContentsMargins(10, 10, 10, 10)
        
        new_label = QLabel("🆕 NEW AI INSIGHT")
        new_label.setStyleSheet(f"font-size: 14px; color: {LuxuryTheme.GOLD}; font-weight: bold;")
        
        new_insight = QLabel("AI suggests: " + insight_text)
        new_insight.setStyleSheet(f"font-size: 16px; color: {LuxuryTheme.TEXT_LIGHT};")
        new_insight.setWordWrap(True)
        
        insight_layout.addWidget(new_label)
        insight_layout.addWidget(new_insight)
        
        self.add_shadow_effect(new_insight_frame, gold=True)
        self.scroll_layout.insertWidget(1, new_insight_frame)

    # ------------------ Core Methods ------------------
    def run_ai_analysis(self):
        """Pass AI analysis event to presenter"""
        self.presenter.run_ai_analysis()

    def update_last_refresh(self):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M")
        self.last_refresh_time = current_time
        
        refresh_label = self.findChild(QLabel, "refresh_label")
        if refresh_label:
            refresh_label.setText(f"Last update: {self.last_refresh_time}")

    def add_shadow_effect(self, widget, gold=False):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        if gold:
            shadow.setColor(QColor(255, 215, 0, 30))  # Gold shadow
        else:
            shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        widget.setGraphicsEffect(shadow)


# For standalone testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create mock model for testing
    from models.mock_stock_model import MockStockModel
    model = MockStockModel()
    
    window = AIAdvisorWindow(model)
    window.show()
    
    # High DPI support
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    sys.exit(app.exec())