import datetime
import re
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QTextEdit, QPushButton, QFrame, QScrollArea, 
                              QSizePolicy, QSpacerItem, QMenu)
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QByteArray, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

from assets.theme import FaceID6Theme
from models.mock_stock_model import MockStockModel


class AIAdvisorWindow(QWidget):
    """AI Advisor chat window for investment advice"""
    
    def __init__(self, model=None, parent=None):
        super().__init__(parent)
        self.model = model if model else MockStockModel()
        self.theme = FaceID6Theme
        
        # Initialize the presenter
        try:
            from presenters.ai_advisor_presenter import AIAdvisorPresenter
            self.presenter = AIAdvisorPresenter(self, self.model)
        except ImportError:
            print("Error importing AIAdvisorPresenter. Using a simple presenter instead.")
        
        self.init_ui()
        #do full screen
        self.showFullScreen()  # Uncomment to start in full screen mode

    
    def init_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle("AI Investment Advisor")
        self.setMinimumSize(800, 600)  
        # self.showFullScreen()  # Start in full screen mode      
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add header bar
        header_bar = self.create_header_bar()
        main_layout.addWidget(header_bar)
        
        # Create a scroll area for the entire content to ensure it fits
        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        main_scroll_area.setFrameShape(QFrame.NoFrame)
        main_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        main_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Content area with some padding
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # Main title and description
        title_label = QLabel("AI Investment Advisor")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #1F2937;")
        
        description_label = QLabel("Ask for investment advice, portfolio analysis, or market insights. Our AI advisor will provide personalized recommendations based on your queries.")
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 14px; color: #4B5563; margin-top: 5px;")
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(description_label)
        
        # Chat container - make it take a reasonable proportion of the space
        chat_frame = QFrame()
        chat_frame.setObjectName("card")
        chat_frame.setMinimumHeight(550)  # Increased minimum height
        chat_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow expansion
        chat_frame.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border: 1px solid #E5E5EA;
                border-radius: 8px;
            }
        """)
        
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)
        
        # Chat header
        chat_header = QFrame()
        chat_header.setStyleSheet("""
            background-color: #f9fafb;
            border-bottom: 1px solid #E5E5EA;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 10px;
        """)
        
        chat_header_layout = QHBoxLayout(chat_header)
        chat_header_layout.setContentsMargins(15, 10, 15, 10)
        
        chat_title = QLabel("Investment Advisor Chat")
        chat_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F2937;")
        
        chat_header_layout.addWidget(chat_title)
        chat_layout.addWidget(chat_header)
        
        # Chat messages area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #F2F2F7;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #C7C7CC;
                min-height: 30px;
                border-radius: 4px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #A9A9B0;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)        
        # Container for chat messages
        self.messages_container = QWidget()
        self.messages_container.setMinimumWidth(1100)

        self.messages_container.setStyleSheet("background-color: white;")
        self.messages_layout = QVBoxLayout(self.messages_container)
        self.messages_layout.setAlignment(Qt.AlignTop)
        self.messages_layout.setContentsMargins(20, 20, 20, 20)
        self.messages_layout.setSpacing(15)
        
        # Add welcome message
        self.add_welcome_message()
        
        # Add stretch to push messages to the top
        self.messages_layout.addStretch()
        
        self.scroll_area.setWidget(self.messages_container)
        chat_layout.addWidget(self.scroll_area)
        
        # Input area
        input_container = QFrame()
        input_container.setStyleSheet("""
            background-color: white;
            border-top: 1px solid #E5E5EA;
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            padding: 10px;
        """)
        
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        # Text input field
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Ask for investment advice...")
        self.input_field.setMaximumHeight(50)
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #E5E5EA;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #37506D;
            }
        """)
        
        # Send button
        self.send_button = QPushButton()
        try:
            # SVG for send icon
            send_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>"""
            send_renderer = QSvgRenderer(QByteArray(send_svg.encode()))
            send_pixmap = QPixmap(24, 24)
            send_pixmap.fill(Qt.transparent)
            send_painter = QPainter(send_pixmap)
            send_renderer.render(send_painter)
            send_painter.end()
            self.send_button.setIcon(QIcon(send_pixmap))
        except:
            # Fallback to using text if icon not available
            self.send_button.setText("→")
            
        self.send_button.setFixedSize(40, 40)
        self.send_button.setIconSize(QSize(20, 20))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #1c2c3f;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2a3c52;
            }
            QPushButton:disabled {
                background-color: #A6BCD3;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.send_button)


        self.loading_indicator = QLabel("Analyzing your question...")
        self.loading_indicator.setAlignment(Qt.AlignCenter)
        self.loading_indicator.setStyleSheet("""
            color: #1c2c3f;
            background-color: #F3F4F6;
            border-radius: 12px;
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 500;
        """)
        self.loading_indicator.setVisible(False)

        # Add the loading indicator to the chat layout
        chat_layout.addWidget(self.loading_indicator)
        chat_layout.addWidget(input_container)
        
        # Add chat frame to content layout
        content_layout.addWidget(chat_frame)
        
        # Footer disclaimer
        footer_label = QLabel("© 2025 InvestAI Advisor. All investment advice is simulated for demonstration purposes.\nNot financial advice. Consult with a professional advisor before making investment decisions.")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #6B7280; font-size: 12px; margin-top: 10px;")
        content_layout.addWidget(footer_label)
        
        # Set the content widget as the main scrollable area's widget
        main_scroll_area.setWidget(content_widget)
        
        # Add the main scroll area to the main layout
        main_layout.addWidget(main_scroll_area)


    def show_loading_indicator(self):
        """Show the loading indicator"""
        self.loading_indicator.setVisible(True)
        
    def hide_loading_indicator(self):
        """Hide the loading indicator"""
        self.loading_indicator.setVisible(False)

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
        
        # Logo and App name container
        logo_container = QHBoxLayout()
        logo_container.setSpacing(10)
        
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
        
        logo_container.addWidget(logo_label)
        logo_container.addWidget(app_name)
        
        # Navigation buttons - positioned in the middle with space
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(20)
        
        nav_items = ["Main Menu", "Trading", "Analytics", "Help"]
        
        for item in nav_items:
            nav_btn = QPushButton(item)
            nav_btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: transparent;
                    border: none;
                    padding: 8px 12px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    color: #E5E5EA;
                }
            """)
            nav_btn.clicked.connect(self.close)  # For now, just close the window
            nav_layout.addWidget(nav_btn)
        
        # Account button on the far right
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
        
        # Add components to main header layout in proper order
        # Logo on the left, nav in middle, account on right
        header_layout.addLayout(logo_container)
        header_layout.addStretch(1)  # Push nav to the middle
        header_layout.addLayout(nav_layout)
        header_layout.addStretch(1)  # Push account to the right
        header_layout.addWidget(account_btn)
        
        # Overall frame styling
        header_frame.setStyleSheet("""
            QFrame#header-bar {
                background-color: #1F2937;
                color: white;
            }
        """)
        
        return header_frame
        
    def add_welcome_message(self):
        """Add the initial welcome message"""
        welcome_frame = QFrame()
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        
        welcome_label = QLabel()
        welcome_label.setText(
            "<div style='text-align:center;'>"
            "<p style='margin-bottom:8px;font-size:16px;color:#4B5563;'>Welcome to your AI Investment Advisor</p>"
            "<p style='font-size:14px;color:#6B7280;'>Ask any investment question to get started</p>"
            "</div>"
        )
        welcome_label.setAlignment(Qt.AlignCenter)
        
        welcome_layout.addWidget(welcome_label)
        self.messages_layout.addWidget(welcome_frame, 0, Qt.AlignCenter)
    
    def create_user_message(self, text):
        """Create a user message bubble"""
        message_frame = QFrame()
        message_layout = QHBoxLayout(message_frame)
        message_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add spacer to push the message to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        message_layout.addItem(spacer)
        
        # Message bubble
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMinimumWidth(200)  # Minimum width for small messages
        bubble.setStyleSheet("""
        background-color: white;
        color: #1F2937;
        border: 1px solid #E5E5EA;
        border-radius: 12px 12px 12px 0px;
        padding: 12px 16px;
        min-width: 200px;
        max-width: 1200px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
    """)
        bubble.setFixedWidth(1000)  # Force a wide fixed width
        message_layout.addWidget(bubble)
        return message_frame
        
    def create_advisor_message(self, text, tag=None):
        """Create an advisor message bubble with optional tag icon"""
        message_frame = QFrame()
        message_layout = QHBoxLayout(message_frame)
        message_layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon based on tag
        icon_label = QLabel()
        icon_label.setFixedSize(20, 20)
        
        # Select icon and color based on tag
        icon_svg = ""
        if tag == "buy":
            # TrendingUp icon
            icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34C759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>"""
        elif tag == "sell":
            # TrendingDown icon
            icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF3B30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>"""
        elif tag == "warning":
            # AlertTriangle icon
            icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
        elif tag == "success":
            # CheckCircle icon
            icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34C759" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
        else:
            # HelpCircle icon (default)
            icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#37506D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
        
        if icon_svg:
            renderer = QSvgRenderer(QByteArray(icon_svg.encode()))
            pixmap = QPixmap(20, 20)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            icon_label.setPixmap(pixmap)
        
        # Message bubble
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setMinimumWidth(100)  # Minimum width for small messages
        font = bubble.font()
        font.setWordSpacing(1)  # Slightly increase word spacing
        font.setLetterSpacing(QFont.PercentageSpacing, 101)  # Very slightly increase letter spacing
        bubble.setFont(font)
        bubble.setFixedWidth(1000)

        bubble.setStyleSheet("""
        background-color: #1c2c3f;
        color: white;
        border-radius: 12px 12px 0px 12px;
        padding: 12px 16px;
        min-width: 200px;
        max-width: 1200px;
        box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
    """)
        # Add the icon and bubble directly to the message layout
        message_layout.addWidget(icon_label)
        message_layout.addWidget(bubble)
        
        # Add spacer to push the message to the left
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        message_layout.addItem(spacer)
        
        return message_frame
    
    def send_message(self):
        """Send a user message and get a response with faster animation"""
        user_text = self.input_field.toPlainText().strip()
        if not user_text:
            return
        
        self.presenter.set_query(user_text)

        # Create user message
        user_message = self.create_user_message(user_text)
        user_message.setMaximumHeight(0)
        user_message.setVisible(False)
        
        # Add to layout
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, user_message)
        self.input_field.clear()

        # Animate user message quickly
        def animate_user_message():
            user_message.setVisible(True)
            for i in range(1, 6):  # 5 steps for faster animation
                def set_height(step=i):
                    target_height = user_message.sizeHint().height()
                    current_height = int(target_height * (step/5))
                    user_message.setMaximumHeight(current_height)
                    if step == 5:
                        user_message.setMaximumHeight(16777215)
                        # Scroll to bottom
                        self.scroll_to_bottom()
                        # After user message is shown, get AI response
                        if step == 5 and i == 5:
                            self.presenter.run_ai_analysis()
                QTimer.singleShot(20 * i, set_height)  # Faster animation (20ms)
        
        # Start animation immediately
        animate_user_message()
        
        # Clear input field
        self.input_field.clear()
        
        # Disable send button while processing
        self.send_button.setEnabled(False)
    
    def keyPressEvent(self, event):
        """Handle key press events for the input field"""
        # Send message when Enter is pressed (without Shift)
        if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
            # Only if input field has focus
            if self.input_field.hasFocus():
                self.send_message()
                return
        
        super().keyPressEvent(event)
        
    def add_new_insight(self, insight):
        """Add a new AI insight to the chat with faster animation"""
        # For demo, randomly assign a tag sometimes
        import random
        tags = [None, "buy", "sell", "warning", "success", None, None, None]
        tag = random.choice(tags)
        
        # Create the message but set it initially invisible
        advisor_message = self.create_advisor_message(insight, tag)
        advisor_message.setMaximumHeight(0)
        advisor_message.setVisible(False)
        
        # Add it to the layout
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, advisor_message)
        
        # Create animation to slide in the message - faster with fewer steps
        def animate_message():
            advisor_message.setVisible(True)
            # Use 5 steps instead of 10, and shorter interval (20ms instead of 40ms)
            for i in range(1, 6):
                def set_height(step=i):
                    target_height = advisor_message.sizeHint().height()
                    current_height = int(target_height * (step/5))
                    advisor_message.setMaximumHeight(current_height)
                    if step == 5:
                        advisor_message.setMaximumHeight(16777215)  # Default max
                        self.scroll_to_bottom()
                # Faster delay (20ms per step)
                QTimer.singleShot(20 * i, set_height)
        
        # Shorter delay before starting animation
        QTimer.singleShot(50, animate_message)
        
    def scroll_to_bottom(self):
        """Scroll the chat area to the bottom"""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        
    def update_analysis_button_text(self, text):
        """Update the send button text when analyzing"""
        # If we have an icon, temporarily hide it and show text
        if text == "🔄 Analyzing...":
            self.send_button.setIcon(QIcon())
            self.send_button.setText(text)
        else:
            # Reset to icon
            self.send_button.setText("")
            try:
                # SVG for send icon
                send_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>"""
                send_renderer = QSvgRenderer(QByteArray(send_svg.encode()))
                send_pixmap = QPixmap(24, 24)
                send_pixmap.fill(Qt.transparent)
                send_painter = QPainter(send_pixmap)
                send_renderer.render(send_painter)
                send_painter.end()
                self.send_button.setIcon(QIcon(send_pixmap))
            except:
                self.send_button.setText("→")
        
    def set_analysis_button_enabled(self, enabled):
        """Enable or disable the send button"""
        self.send_button.setEnabled(enabled)
        
    def update_last_refresh(self):
        """Update the last refresh timestamp (not used in this implementation)"""
        pass
        
    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        
        # Adjust content based on window size
        window_width = self.width()
        
        # Scale message bubbles based on window width
        max_bubble_width = min(int(window_width * 0.85), 800)
        
        # Update bubble styles with new max width
        self.update_message_bubbles_width(max_bubble_width)
        
        # Scroll to bottom to keep the latest messages visible
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def showEvent(self, event):
        """Handle when window is shown"""
        super().showEvent(event)
        
        # Set initial width of chat bubbles based on window size
        window_width = self.width()
        max_bubble_width = min(int(window_width * 0.8), 800)
        
        # Update all message bubbles after a short delay (to ensure layout is stable)
        QTimer.singleShot(100, lambda: self.update_message_bubbles_width(max_bubble_width))

    def add_new_insight(self, insight):
        """Add a new AI insight to the chat with animation"""
        # For demo, randomly assign a tag sometimes
        import random
        tags = [None, "buy", "sell", "warning", "success", None, None, None]
        tag = random.choice(tags)
        
        # Create the message but set it initially invisible
        advisor_message = self.create_advisor_message(insight, tag)
        advisor_message.setMaximumHeight(0)
        advisor_message.setVisible(False)
        
        # Add it to the layout
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, advisor_message)
        
        # Create animation to slide in the message
        def animate_message():
            advisor_message.setVisible(True)
            # Start a series of height increases
            for i in range(1, 11):
                def set_height(step=i):
                    # Calculate final height based on content
                    target_height = advisor_message.sizeHint().height()
                    current_height = int(target_height * (step/10))
                    advisor_message.setMaximumHeight(current_height)
                    # On the last step, remove height restriction
                    if step == 10:
                        advisor_message.setMaximumHeight(16777215)  # Default max
                        # Scroll to bottom
                        self.scroll_to_bottom()
                # Schedule each step with increasing delay
                QTimer.singleShot(40 * i, set_height)
        
        # Slight delay before starting animation
        QTimer.singleShot(100, animate_message)

    def update_message_bubbles_width(self, max_width):
        """Update all message bubbles to have the specified max width"""
        # Find all labels in message containers and update their max-width
        for i in range(self.messages_layout.count() - 1):  # -1 to skip the stretch at the end
            item = self.messages_layout.itemAt(i)
            if item and item.widget():
                frame = item.widget()
                # Find label in the frame's layout
                if hasattr(frame, 'layout'):
                    layout = frame.layout()
                    for j in range(layout.count()):
                        layout_item = layout.itemAt(j)
                        if layout_item and layout_item.widget() and isinstance(layout_item.widget(), QLabel):
                            label = layout_item.widget()
                            # Update style with new max width
                            style = label.styleSheet()
                            if 'max-width:' in style:
                                try:
                                    style = re.sub(r'max-width:\s*\d+px', f'max-width: {max_width}px', style)
                                    label.setStyleSheet(style)
                                except:
                                    # In case regex fails, just set the max width directly
                                    label.setMaximumWidth(max_width)