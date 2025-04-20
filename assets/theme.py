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

class FaceID6Theme:
    """
    FaceID6 theme definition with modern iOS-inspired styling
    """

    # Color palette
    PRIMARY_COLOR = "#1F2937"       # Dark blue/slate for header bar
    SECONDARY_COLOR = "#30455C"     # Button color
    ACCENT_COLOR = "#37506D"        # iOS blue accent color
    SUCCESS_COLOR = "#34C759"       # Green (unchanged)
    WARNING_COLOR = "#FF9500"       # Orange (unchanged)
    DANGER_COLOR = "#FF3B30"        # Red (unchanged)
    BACKGROUND_COLOR = "#F2F2F7"    # Light gray background (unchanged)
    CARD_COLOR = "#FFFFFF"          # White (unchanged)
    TEXT_PRIMARY = "#000000"        # Black text (unchanged)
    TEXT_SECONDARY = "#A6BCD3"      # Changed to your specified color
    TEXT_MUTED = "#8E8E93"

    # Main stylesheet
    STYLE_SHEET = f"""
        /* Global styles */
        QWidget {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            color: {TEXT_PRIMARY};
        }}

        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Header bar styling */
        QFrame#header-bar {{
            background-color: {PRIMARY_COLOR};
            min-height: 60px;
            max-height: 60px;
        }}

        QLabel#logo-icon {{
            font-size: 30px;
            color: white;
            font-weight: bold;
        }}

        QLabel#logo-label {{
            font-size: 24px;
            font-weight: bold;
            color: white;
        }}

        QPushButton#account-button {{
            background-color: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 22px;
            font-size: 22px;
            color: white;
            min-width: 44px;
            min-height: 44px;
            max-width: 44px;
            max-height: 44px;
        }}

        QPushButton#account-button:hover {{
            background-color: rgba(255, 255, 255, 0.3);
        }}

        /* Menu bar styling */
        QMenuBar {{
            background-color: {CARD_COLOR};
            border-bottom: 1px solid #E5E5EA;
        }}

        QMenuBar::item {{
            padding: 6px 12px;
            background: transparent;
        }}

        QMenuBar::item:selected {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 4px;
        }}

        QMenu {{
            background-color: {CARD_COLOR};
            border: 1px solid #E5E5EA;
            border-radius: 10px;
            padding: 5px 0px;
        }}

        QMenu::item {{
            padding: 6px 25px 6px 20px;
        }}

        QMenu::item:selected {{
            background-color: #E5E5EA;
            border-radius: 5px;
        }}

        /* Button styling */
        QPushButton {{
            background-color: {BACKGROUND_COLOR};
            color: {SECONDARY_COLOR};
            border: 1px solid #E5E5EA;
            border-radius: 10px;
            padding: 15px 20px;
            font-weight: 500;
            font-size: 16px;
        }}

        QPushButton:hover {{
            background-color: #E5E5EA;
        }}

        QPushButton:pressed {{
            background-color: #D1D1D6;
        }}

        QPushButton#highlight-button {{
            background-color: {ACCENT_COLOR};
            color: white;
            border: none;
        }}

        QPushButton#highlight-button:hover {{
            background-color: #0069D9;
        }}

        /* Header styles */
        QFrame#header-frame {{
            background-color: {CARD_COLOR};
            border-radius: 12px;
        }}

        QLabel#welcome-label {{
            font-size: 24px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
            margin-bottom: 8px;
        }}

        QLabel#subtitle-label {{
            font-size: 14px;
            color: {TEXT_SECONDARY};
        }}

        QFrame#info-card {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 10px;
            padding: 10px;
        }}

        QLabel#account-text {{
            font-size: 16px;
            font-weight: 600;
            color: {ACCENT_COLOR};
        }}

        QLabel#quote-text {{
            font-size: 13px;
            font-style: italic;
            color: {TEXT_SECONDARY};
            margin-top: 10px;
        }}

        /* Section titles */
        QLabel#section-title {{
            font-size: 20px;
            font-weight: 600;
            color: {TEXT_PRIMARY};
            margin-top: 10px;
            margin-bottom: 5px;
        }}

        /* Cards */
        QFrame#card {{
            background-color: {CARD_COLOR};
            border-radius: 10px;
        }}

        QFrame#summary-card {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }}

        QFrame#market-card {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 8px;
            padding: 12px;
        }}

        /* Value displays */
        QLabel#large-value {{
            font-size: 36px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
        }}

        QLabel#value-text {{
            font-size: 26px;
            font-weight: 600;
            color: {TEXT_PRIMARY};
        }}

        QLabel#accent-text {{
            font-size: 14px;
            font-weight: 600;
            color: {ACCENT_COLOR};
        }}

        /* Table styling */
        QTableWidget {{
            background-color: {CARD_COLOR};
            border: none;
            gridline-color: #E5E5EA;
            border-radius: 8px;
            selection-background-color: #E5E5EA;
            selection-color: {TEXT_PRIMARY};
        }}

        QTableWidget::item {{
            padding: 5px;
            border-radius: 4px;
        }}

        QTableWidget::item:selected {{
            background-color: #E5E5EA;
            color: {TEXT_PRIMARY};
        }}

        QHeaderView::section {{
            background-color: {BACKGROUND_COLOR};
            padding: 10px;
            border: none;
            font-weight: 600;
            color: {TEXT_SECONDARY};
        }}

        QTableWidget:alternate-background-color {{
            background-color: #F7F7F9;
        }}

        /* Tab widget */
        QTabWidget::pane {{
            border: none;
            background-color: {CARD_COLOR};
            border-radius: 10px;
        }}

        QTabBar::tab {{
            background-color: transparent;
            padding: 8px 15px;
            margin-right: 5px;
            color: {TEXT_SECONDARY};
            border-bottom: 2px solid transparent;
        }}

        QTabBar::tab:selected {{
            color: {ACCENT_COLOR};
            border-bottom: 2px solid {ACCENT_COLOR};
        }}

        QTabBar::tab:hover {{
            color: {ACCENT_COLOR};
        }}

        /* Scroll area */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: #F2F2F7;
            width: 10px;
            margin: 0px;
        }}

        QScrollBar::handle:vertical {{
            background-color: #C7C7CC;
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* Status bar */
        QStatusBar {{
            background-color: {PRIMARY_COLOR};
            color: white;
            font-weight: 500;
            min-height: 25px;
        }}

        QStatusBar::item {{
            border: none;
        }}

        /* ---- Buy Stocks Page Styling ---- */

        /* Enhanced stock info card */
        QFrame#stock-info-card {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            border: 1px solid #E5E5EA;
        }}

        /* Chart styling */
        QFrame#chart-container {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #E5E5EA;
        }}

        /* Stock price and change display */
        QLabel#stock-price {{
            font-size: 36px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
        }}

        QLabel#stock-change-positive {{
            color: {SUCCESS_COLOR};
            font-size: 16px;
            font-weight: bold;
        }}

        QLabel#stock-change-negative {{
            color: {DANGER_COLOR};
            font-size: 16px;
            font-weight: bold;
        }}

        /* Stock search styling */
        QLineEdit#stock-search {{
            background-color: {CARD_COLOR};
            border: 1px solid #E5E5EA;
            border-radius: 10px;
            padding: 12px 15px;
            font-size: 15px;
            min-height: 45px;
        }}

        QLineEdit#stock-search:focus {{
            border: 1px solid {ACCENT_COLOR};
        }}

        /* Order form styling */
        QFrame#order-form {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
        }}

        /* Order summary sections */
        QFrame#order-summary {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 10px;
            padding: 15px;
        }}

        QLabel#summary-label {{
            color: {TEXT_MUTED};
            font-size: 14px;
        }}

        QLabel#summary-value {{
            color: {TEXT_PRIMARY};
            font-size: 16px;
            font-weight: 600;
        }}

        QLabel#total-label {{
            color: {ACCENT_COLOR};
            font-size: 16px;
            font-weight: bold;
        }}

        QLabel#total-value {{
            color: {TEXT_PRIMARY};
            font-size: 20px;
            font-weight: bold;
        }}

        /* Quantity spinner styling */
        QSpinBox#quantity-spinner {{
            background-color: {CARD_COLOR};
            border: 1px solid #E5E5EA;
            border-radius: 10px;
            padding: 8px 12px;
            min-height: 40px;
            font-size: 16px;
        }}

        QSpinBox#quantity-spinner::up-button, QSpinBox#quantity-spinner::down-button {{
            background-color: {BACKGROUND_COLOR};
            border: 1px solid #E5E5EA;
            border-radius: 5px;
            width: 20px;
            height: 15px;
        }}

        QSpinBox#quantity-spinner::up-button:hover, QSpinBox#quantity-spinner::down-button:hover {{
            background-color: #E5E5EA;
        }}

        /* Market data grid styling */
        QFrame#market-data-item {{
            background-color: {BACKGROUND_COLOR};
            border-radius: 8px;
            padding: 10px;
            min-height: 70px;
        }}

        QLabel#data-label {{
            color: {TEXT_MUTED};
            font-size: 14px;
        }}

        QLabel#data-value {{
            color: {TEXT_PRIMARY};
            font-size: 18px;
            font-weight: 600;
        }}

        /* Error and success messages */
        QLabel#error-message {{
            color: {DANGER_COLOR};
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        }}

        QLabel#success-message {{
            color: {SUCCESS_COLOR};
            font-size: 14px;
            font-weight: bold;
            padding: 5px;
        }}

        /* Progress bar styling */
        QProgressBar {{
            border: 1px solid #E5E5EA;
            border-radius: 5px;
            background-color: {BACKGROUND_COLOR};
            text-align: center;
            height: 10px;
        }}

        QProgressBar::chunk {{
            background-color: {ACCENT_COLOR};
            border-radius: 4px;
        }}

        /* List widget styling */
        QListWidget {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: 1px solid #E5E5EA;
            padding: 5px;
        }}

        QListWidget::item {{
            padding: 10px;
            border-bottom: 1px solid #E5E5EA;
            border-radius: 5px;
        }}

        QListWidget::item:selected {{
            background-color: #E5E5EA;
            color: {TEXT_PRIMARY};
        }}

        QListWidget::item:hover {{
            background-color: rgba(0, 122, 255, 0.05);
        }}

        /* Stock display styling */
        QLabel#stock-display {{
            font-size: 16px;
            font-weight: bold;
            color: {ACCENT_COLOR};
        }}

        /* Price display styling */
        QLabel#price-display {{
            color: {ACCENT_COLOR};
        }}

        /* Current price label styling */
        QLabel#current-price-label {{
            color: {ACCENT_COLOR};
            font-size: 16px;
            font-weight: bold;
        }}
    """
class DarkLuxuryTheme:
    """
    Dark Luxury theme with a premium dark appearance and emerald accents
    Includes top header bar with logo and account button
    """

    # Color palette
    PRIMARY_COLOR = "#10B981"       # Emerald green
    SECONDARY_COLOR = "#34D399"     # Light emerald
    ACCENT_COLOR = "#F59E0B"        # Amber for gold accents
    BACKGROUND_COLOR = "#111827"    # Dark gray/blue background
    CARD_COLOR = "#1E293B"          # Dark blue-gray for cards
    CARD_ALT_COLOR = "#374151"      # Lighter gray for cards
    TEXT_PRIMARY = "#F9FAFB"        # Almost white text
    TEXT_SECONDARY = "#D1D5DB"      # Light gray text
    TEXT_MUTED = "#9CA3AF"          # Medium gray text
    DANGER_COLOR = "#EF4444"        # Red
    POSITIVE_COLOR = "#10B981"      # Green
    BORDER_COLOR = "#1E293B"        # Border color
    HEADER_BG_COLOR = "#0F172A"     # Darker color for the header bar

    # Main stylesheet
    STYLE_SHEET = f"""
        /* Global styles */
        QWidget {{
            font-family: 'Montserrat', 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
            color: {TEXT_PRIMARY};
            background-color: {BACKGROUND_COLOR};
        }}

        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}

        /* Header Bar Styling */
        QFrame#header-bar {{
            background-color: {HEADER_BG_COLOR};
            min-height: 50px;
            max-height: 50px;
            border-bottom: 1px solid {BORDER_COLOR};
        }}

        QLabel#logo-label {{
            font-size: 22px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
            padding-left: 10px;
        }}

        QLabel#logo-icon {{
            padding-left: 15px;
            padding-right: 5px;
            color: {PRIMARY_COLOR};
        }}

        QPushButton#account-button {{
            background-color: transparent;
            border: none;
            color: {TEXT_PRIMARY};
            padding: 8px;
            border-radius: 20px;
        }}

        QPushButton#account-button:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* Menu bar styling - now part of header bar */
        QMenuBar {{
            background-color: {HEADER_BG_COLOR};
            border: none;
            color: {TEXT_PRIMARY};
            padding: 0px 15px;
        }}

        QMenuBar::item {{
            padding: 15px 15px;
            background: transparent;
        }}

        QMenuBar::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }}

        QMenu {{
            background-color: {CARD_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            padding: 5px 0px;
        }}

        QMenu::item {{
            padding: 8px 30px 8px 20px;
        }}

        QMenu::item:selected {{
            background-color: {CARD_ALT_COLOR};
        }}

        /* Button styling */
        QPushButton {{
            background-color: {CARD_COLOR};
            color: {TEXT_PRIMARY};
            border: 1px solid #2C3E50;
            border-radius: 6px;
            padding: 12px 20px;
            font-weight: 600;
            text-align: center;
        }}

        QPushButton:hover {{
            background-color: rgba(24, 40, 66, 1);
        }}

        QPushButton:pressed {{
            background-color: rgba(16, 30, 50, 1);
        }}

        QPushButton#buy-button {{
            background-color: rgba(16, 185, 129, 0.2);
            color: {PRIMARY_COLOR};
            border: none;
        }}

        QPushButton#buy-button:hover {{
            background-color: rgba(16, 185, 129, 0.3);
        }}

        QPushButton#sell-button {{
            background-color: rgba(239, 68, 68, 0.2);
            color: #FCA5A5;
            border: none;
        }}

        QPushButton#sell-button:hover {{
            background-color: rgba(239, 68, 68, 0.3);
        }}

        QPushButton#ai-button {{
            background-color: rgba(59, 130, 246, 0.2);
            color: #93C5FD;
            border: none;
        }}

        QPushButton#ai-button:hover {{
            background-color: rgba(59, 130, 246, 0.3);
        }}

        QPushButton#history-button {{
            background-color: rgba(168, 85, 247, 0.2);
            color: #C4B5FD;
            border: none;
        }}

        QPushButton#history-button:hover {{
            background-color: rgba(168, 85, 247, 0.3);
        }}

        /* Header styles */
        QFrame#welcome-frame {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: none;
            padding: 15px;
        }}

        QLabel#welcome-label {{
            font-size: 26px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
        }}

        QLabel#subtitle-label {{
            font-size: 16px;
            color: {TEXT_SECONDARY};
        }}

        QFrame#info-frame {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: none;
            padding: 15px;
        }}

        QLabel#account-tag {{
            font-size: 14px;
            color: {TEXT_PRIMARY};
            background-color: rgba(16, 185, 129, 0.2);
            border-radius: 15px;
            padding: 5px 10px;
        }}

        QLabel#login-info {{
            font-size: 14px;
            color: {TEXT_SECONDARY};
            margin-top: 5px;
        }}

        QLabel#quote-text {{
            font-size: 14px;
            font-style: italic;
            color: {TEXT_SECONDARY};
            margin-top: 10px;
        }}

        /* Section titles */
        QLabel#section-title {{
            font-size: 22px;
            font-weight: 600;
            color: {TEXT_PRIMARY};
            margin-top: 15px;
            margin-bottom: 10px;
        }}

        /* Cards */
        QFrame#card {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: none;
        }}

        QFrame#summary-card {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: none;
            padding: 20px;
        }}

        QFrame#value-card {{
            background-color: {CARD_COLOR};
            border-radius: 8px;
            border: none;
            padding: 15px;
        }}

        QLabel#value-label {{
            font-size: 16px;
            color: {TEXT_SECONDARY};
        }}

        QLabel#large-value {{
            font-size: 36px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
        }}

        QLabel#positive-value {{
            font-size: 36px;
            font-weight: bold;
            color: {PRIMARY_COLOR};
        }}

        QLabel#market-title {{
            font-size: 16px;
            color: {TEXT_SECONDARY};
        }}

        QLabel#market-value {{
            font-size: 28px;
            font-weight: bold;
            color: {TEXT_PRIMARY};
        }}

        QLabel#market-change-positive {{
            font-size: 16px;
            color: {PRIMARY_COLOR};
        }}

        QLabel#market-change-negative {{
            font-size: 16px;
            color: {DANGER_COLOR};
        }}

        /* Table styling */
        QTableWidget {{
            background-color: {CARD_COLOR};
            border: none;
            gridline-color: {BORDER_COLOR};
            border-radius: 8px;
        }}

        QTableWidget::item {{
            padding: 10px;
            border-bottom: 1px solid {BORDER_COLOR};
        }}

        QTableWidget::item:selected {{
            background-color: rgba(255, 255, 255, 0.1);
        }}

        QHeaderView::section {{
            background-color: {CARD_COLOR};
            padding: 12px;
            border: none;
            font-weight: 600;
            color: {TEXT_SECONDARY};
            border-bottom: 1px solid {BORDER_COLOR};
        }}

        QTableWidget:alternate-background-color {{
            background-color: rgba(31, 41, 55, 0.4);
        }}

        /* Tab widget */
        QTabWidget::pane {{
            border: none;
            background-color: {CARD_COLOR};
            border-radius: 8px;
        }}

        QTabBar::tab {{
            background-color: transparent;
            padding: 10px 20px;
            margin-right: 5px;
            color: {TEXT_SECONDARY};
            border-bottom: 2px solid transparent;
        }}

        QTabBar::tab:selected {{
            color: {PRIMARY_COLOR};
            border-bottom: 2px solid {PRIMARY_COLOR};
        }}

        QTabBar::tab:hover {{
            color: {SECONDARY_COLOR};
        }}

        /* Scroll area */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            border: none;
            background-color: {CARD_COLOR};
            width: 10px;
            margin: 0px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {CARD_ALT_COLOR};
            border-radius: 5px;
            min-height: 30px;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        /* Status bar */
        QStatusBar {{
            background-color: #0F172A;
            color: {TEXT_SECONDARY};
            font-weight: 500;
            min-height: 25px;
            border-top: 1px solid {BORDER_COLOR};
        }}

        QStatusBar::item {{
            border: none;
        }}
    """
    