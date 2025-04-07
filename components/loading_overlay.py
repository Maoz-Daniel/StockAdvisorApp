# components/loading_overlay.py
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

class LoadingOverlay(QFrame):
    def __init__(self, parent=None, message="Loading your portfolio..."):
        super().__init__(parent)
        self.setObjectName("loading-overlay")
        self.setStyleSheet("""
            QFrame#loading-overlay {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
            }
            QLabel#message-label {
                color: #1E3A8A;
                font-size: 18px;
                font-weight: bold;
                margin-top: 15px;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create loading animation with QMovie
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignCenter)
        
        # Use QMovie to display the GIF
        self.movie = QMovie("assets/loading.gif")  # Adjust the path to your GIF
        self.movie.setScaledSize(QSize(100, 100))  # Adjust size as needed
        self.animation_label.setMovie(self.movie)
        
        # Loading message
        self.message_label = QLabel(message)
        self.message_label.setObjectName("message-label")
        self.message_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(self.animation_label, 0, Qt.AlignCenter)
        layout.addWidget(self.message_label, 0, Qt.AlignCenter)
        
        # Initially hidden
        self.hide()
    
    def set_message(self, message):
        """Update the loading message"""
        self.message_label.setText(message)
    
    def show_overlay(self):
        """Show the loading overlay covering the parent widget"""
        if self.parentWidget():
            self.setGeometry(0, 0, self.parentWidget().width(), self.parentWidget().height())
        
        # Start the movie animation
        self.movie.start()
        
        self.show()
        self.raise_()
    
    def hide_overlay(self):
        """Hide the loading overlay"""
        # Stop the movie animation
        self.movie.stop()
        self.hide()