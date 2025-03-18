"""
This file defines a luxury dark theme for the investment application.
Place this file in your assets folder and import it to maintain
consistent styling across all views.
"""

class LuxuryTheme:
    """Defines colors and styles for the luxury investment theme."""
    
    # Main color palette
    DARK_BLUE = "#112240"       # Main background
    NAVY = "#1E3A5F"            # Secondary/Card background
    HIGHLIGHT_BLUE = "#2C5A8C"  # Borders and highlights
    ELECTRIC_BLUE = "#78BEFF"   # Accent blue for titles and highlights
    GOLD = "#FFE866"            # Gold accent for luxury touches
    BRIGHT_GOLD = "#FFD700"     # Brighter gold for important highlights
    
    # Text colors
    TEXT_WHITE = "#FFFFFF"      # Main text color
    TEXT_LIGHT = "#E8E8E8"      # Regular text
    TEXT_GRAY = "#C0C0C0"       # Subtle text
    
    # Status colors
    POSITIVE_GREEN = "#66CFA6"  # Positive values
    NEGATIVE_RED = "#F87171"    # Negative values
    
    # Transparency values
    TRANS_HIGHLIGHT = "rgba(44, 90, 140, 0.3)"   # Transparent highlight blue
    TRANS_GOLD = "rgba(255, 232, 102, 0.1)"     # Transparent gold

    # Master stylesheet - import this in your views
    STYLE_SHEET = f"""
        /* Main window and backgrounds */
        QMainWindow, QWidget {{
            font-family: 'Segoe UI', 'Roboto', 'Open Sans', sans-serif;
            background-color: {DARK_BLUE};
            color: {TEXT_LIGHT};
        }}
        
        /* Header styling */
        QFrame#header-frame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                         stop:0 {DARK_BLUE}, stop:1 {NAVY});
            border-radius: 10px;
            padding: 20px;
            min-height: 120px;
            border: 1px solid {HIGHLIGHT_BLUE};
            border-bottom: 2px solid {GOLD};
        }}
        
        /* Card frames */
        QFrame.card {{
            background-color: {NAVY};
            border-radius: 8px;
            border: 1px solid {HIGHLIGHT_BLUE};
        }}
        
        /* Gold-accented cards */
        QFrame#gold-card {{
            background-color: {TRANS_HIGHLIGHT};
            border-radius: 8px;
            border: 1px solid {GOLD};
            border-left: 3px solid {GOLD};
            padding: 15px;
        }}
        
        /* Summary cards with enhanced gold accents */
        QFrame#summary-card {{
            background-color: {TRANS_HIGHLIGHT};
            border-radius: 8px;
            border: 1px solid rgba(120, 190, 255, 0.2);
            border-top: 2px solid {GOLD};
            padding: 15px;
        }}
        
        /* Market cards */
        QFrame#market-card {{
            background-color: {TRANS_HIGHLIGHT};
            border-radius: 8px;
            border: 1px solid rgba(120, 190, 255, 0.2);
            border-left: 2px solid {GOLD};
            padding: 15px;
        }}
        
        /* Labels */
        QLabel {{
            color: {TEXT_LIGHT};
            font-size: 14px;
        }}
        
        QLabel#welcome-label {{
            font-size: 24px;
            font-weight: bold;
            color: {TEXT_WHITE};
            letter-spacing: 0.5px;
        }}
        
        QLabel#subtitle-label {{
            color: {TEXT_GRAY};
            font-size: 15px;
            font-weight: normal;
        }}
        
        QLabel#section-title {{
            font-size: 18px;
            font-weight: bold;
            color: {ELECTRIC_BLUE};
            margin-top: 10px;
            margin-bottom: 5px;
            border-left: 3px solid {GOLD};
            padding-left: 10px;
        }}
        
        /* Gold text elements */
        QLabel#gold-text {{
            color: {GOLD};
            font-size: 16px;
            font-weight: bold;
        }}
        
        QLabel#gold-accent-text {{
            color: {GOLD};
            font-size: 14px;
            font-weight: bold;
        }}
        
        QLabel#quote-text {{
            color: {TEXT_WHITE};
            font-size: 13px;
            font-style: italic;
            padding-top: 6px;
            border-top: 1px solid rgba(255, 232, 102, 0.3);
            margin-top: 6px;
        }}
        
        QLabel#large-value {{
            color: {TEXT_WHITE};
            font-size: 22px;
            font-weight: bold;
        }}
        
        QLabel#value-text {{
            color: {TEXT_WHITE};
            font-size: 16px;
            font-weight: bold;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {DARK_BLUE};
            color: {TEXT_LIGHT};
            font-size: 14px;
            padding: 5px;
            border: none;
            border-bottom: 1px solid {HIGHLIGHT_BLUE};
        }}
        
        QMenuBar::item {{
            padding: 8px 15px;
            margin: 2px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {HIGHLIGHT_BLUE};
        }}
        
        QMenu {{
            background-color: {NAVY};
            border: 1px solid {HIGHLIGHT_BLUE};
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            color: {TEXT_LIGHT};
        }}
        
        QMenu::item:selected {{
            background-color: {HIGHLIGHT_BLUE};
            color: {ELECTRIC_BLUE};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {DARK_BLUE};
            color: {TEXT_GRAY};
            padding: 8px;
            font-size: 13px;
            border-top: 1px solid {HIGHLIGHT_BLUE};
        }}
        
        /* Action Buttons */
        QPushButton {{
            background-color: {NAVY};
            color: {TEXT_LIGHT};
            border: 1px solid {HIGHLIGHT_BLUE};
            border-radius: 6px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            min-width: 160px;
            min-height: 45px;
        }}
        
        QPushButton:hover {{
            background-color: {HIGHLIGHT_BLUE};
            color: {ELECTRIC_BLUE};
        }}
        
        QPushButton:pressed {{
            background-color: {DARK_BLUE};
            border: 1px solid {ELECTRIC_BLUE};
        }}
        
        /* Special gold accent button */
        QPushButton#gold-button {{
            background-color: {NAVY};
            color: {GOLD};
            border: 1px solid {GOLD};
            border-left: 3px solid {BRIGHT_GOLD};
            border-right: 3px solid {BRIGHT_GOLD};
        }}
        
        QPushButton#gold-button:hover {{
            background-color: {TRANS_GOLD};
            color: {BRIGHT_GOLD};
        }}
        
        QPushButton#gold-button:pressed {{
            background-color: rgba(255, 232, 102, 0.2);
        }}
        
        /* Tabs and Table */
        QTabWidget::pane {{
            border: 1px solid {HIGHLIGHT_BLUE};
            border-radius: 8px;
            background-color: {NAVY};
        }}
        
        QTabBar::tab {{
            background-color: {DARK_BLUE};
            color: {TEXT_GRAY};
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
            font-weight: 500;
            border: 1px solid {HIGHLIGHT_BLUE};
            border-bottom: none;
        }}
        
        QTabBar::tab:selected {{
            background-color: {NAVY};
            color: {ELECTRIC_BLUE};
            border-bottom: 3px solid {GOLD};
        }}
        
        QTableWidget {{
            background-color: {NAVY};
            alternate-background-color: #24466D;
            border: none;
            gridline-color: {HIGHLIGHT_BLUE};
            selection-background-color: {HIGHLIGHT_BLUE};
            selection-color: {TEXT_LIGHT};
            border-radius: 8px;
        }}
        
        QTableWidget::item {{
            padding: 10px;
            border-bottom: 1px solid {HIGHLIGHT_BLUE};
            color: {TEXT_LIGHT};
        }}
        
        QHeaderView::section {{
            background-color: {DARK_BLUE};
            color: {ELECTRIC_BLUE};
            padding: 12px;
            border: none;
            font-weight: bold;
            border-right: 1px solid {HIGHLIGHT_BLUE};
            border-bottom: 2px solid {GOLD};
        }}
        
        /* Scroll Area */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background: {DARK_BLUE};
            width: 10px;
            margin: 0;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {HIGHLIGHT_BLUE};
            min-height: 30px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {ELECTRIC_BLUE};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
    """