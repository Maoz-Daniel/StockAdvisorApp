from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QApplication, QMainWindow
from PySide6.QtCore import Qt, Signal, QByteArray
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer

class HeaderBar(QFrame):
    """Reusable header bar component with home navigation"""
    
    # Signal emitted when the home button is clicked
    home_clicked = Signal()
    
    def __init__(self, parent=None, use_blue_theme=False, main_window_instance=None):
        super().__init__(parent)
        self.use_blue_theme = use_blue_theme
        self.main_window = main_window_instance
        self.setObjectName("header-bar")
        self.setFixedHeight(60)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the header UI"""
        # Header layout
        header_layout = QHBoxLayout(self)
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
        app_name.clicked.connect(self.go_to_home)
        
        # Logo container
        logo_container = QHBoxLayout()
        logo_container.addWidget(logo_label)
        logo_container.addWidget(app_name)
        logo_container.addStretch()
        
        # Add a simple "Back" button
        back_btn = QPushButton("Back to Dashboard")
        back_btn.setStyleSheet("""
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
        back_btn.clicked.connect(self.go_to_home)
        
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
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(account_btn)
        
        # Apply appropriate styling based on theme
        bg_color = "#007AFF" if self.use_blue_theme else "#1F2937"
        self.setStyleSheet(f"""
            QFrame#header-bar {{
                background-color: {bg_color};
                color: white;
            }}
        """)
    
    def go_to_home(self):
        """Navigate to home screen with refresh"""
        # Emit signal for any custom handling
        self.home_clicked.emit()
        
        # Find the parent window to close
        parent_window = self.find_parent_window()
        if parent_window and parent_window != self.main_window:
            parent_window.close()
        
        # If we have a reference to the main window, refresh it
        if self.main_window:
            # Check if the main window has a refresh_dashboard method
            if hasattr(self.main_window, 'refresh_dashboard'):
                self.main_window.refresh_dashboard()
            # Or try to reload data through the presenter
            elif hasattr(self.main_window, 'presenter'):
                if hasattr(self.main_window.presenter, 'load_user_data'):
                    self.main_window.presenter.load_user_data()
                if hasattr(self.main_window.presenter, 'load_portfolio_data'):
                    self.main_window.presenter.load_portfolio_data()
    
    def find_parent_window(self):
        """Find the parent window widget"""
        # Start with this widget's parent
        widget = self.parent()
        
        # Navigate up until we find a QMainWindow or reach the top
        while widget is not None:
            if isinstance(widget, QMainWindow):
                return widget
            widget = widget.parent()
        
        # If no parent window found, try to find the active window
        return QApplication.activeWindow()
    
    def set_main_window(self, main_window):
        """Set the main window reference"""
        self.main_window = main_window