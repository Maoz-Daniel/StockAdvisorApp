from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction,QActionGroup
from PySide6.QtCore import QSettings

class ThemeSwitcher:
    """
    Theme switcher class that handles theme switching and persistence
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings = QSettings("SmartInvestPro", "Application")
        
        # Import themes here to avoid circular imports
        from assets.theme import LuxuryTheme, FaceID6Theme, DarkLuxuryTheme
        
        self.themes = {
            "luxury": {
                "name": "Luxury Theme",
                "class": LuxuryTheme,
            },
            "faceID6": {
                "name": "FaceID6 Theme",
                "class": FaceID6Theme,
            },
            "darkLuxury": {
                "name": "Dark Luxury Theme",
                "class": DarkLuxuryTheme,
            }
        }
        
        # Default theme
        self.current_theme = self.settings.value("theme", "darkLuxury")
        
    def setup_theme_menu(self, menu_bar):
        """
        Set up the theme menu in the application's menu bar
        """
        # Create appearance menu
        appearance_menu = QMenu("Appearance", self.main_window)
        menu_bar.addMenu(appearance_menu)
        
        # Create action group for radio button behavior
        theme_group = QActionGroup(self.main_window)
        theme_group.setExclusive(True)  # Only one theme can be selected at a time
        
        # Add theme actions
        for theme_id, theme_info in self.themes.items():
            action = QAction(theme_info["name"], self.main_window)
            action.setCheckable(True)
            action.setData(theme_id)
            
            # Check if this is the current theme
            if theme_id == self.current_theme:
                action.setChecked(True)
            
            # Connect action to theme switching
            action.triggered.connect(self._on_theme_triggered)
            
            # Add to group and menu
            theme_group.addAction(action)
            appearance_menu.addAction(action)
        
        # Apply the current theme
        self.apply_theme(self.current_theme)
    
    def _on_theme_triggered(self):
        """
        Handle theme selection from menu
        """
        action = self.main_window.sender()
        if action and action.isChecked():
            theme_id = action.data()
            self.apply_theme(theme_id)
    
    def apply_theme(self, theme_id):
        """
        Apply the selected theme to the application
        """
        if theme_id in self.themes:
            # Import themes here to ensure we get the latest version
            from assets.theme import LuxuryTheme, FaceID6Theme, DarkLuxuryTheme
            
            # Map theme IDs to actual theme classes
            theme_classes = {
                "luxury": LuxuryTheme,
                "faceID6": FaceID6Theme,
                "darkLuxury": DarkLuxuryTheme
            }
            
            # Get theme class
            theme_class = theme_classes[theme_id]
            
            # Apply stylesheet
            self.main_window.setStyleSheet(theme_class.STYLE_SHEET)
            
            # Save the selected theme
            self.current_theme = theme_id
            self.settings.setValue("theme", theme_id)
            
            print(f"Applied theme: {self.themes[theme_id]['name']}")
            
            # Update status bar
            if hasattr(self.main_window, 'status_bar'):
                self.main_window.status_bar.showMessage(f"Theme changed to {self.themes[theme_id]['name']}", 3000)