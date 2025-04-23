from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QObject, QThread, Signal


class AIAdvisorPresenter:
    def __init__(self, view, model):
        """Connect the View to the model and control the AI analysis logic"""
        self.view = view
        self.model = model
        self.current_query = ""  # Add this to store the current query

    def set_query(self, query):
        """Store the query for processing"""
        self.current_query = query
        print(f"AIAdvisorPresenter: Query set to: {self.current_query}")

    def run_ai_analysis(self):
        """Run AI analysis - update analysis button, simulate delay, and return new insight"""
        # Update button status via View
        self.view.update_analysis_button_text("🔄 Analyzing...")
        self.view.set_analysis_button_enabled(False)
        
        # Show the loading indicator instead of the loading bar
        self.view.show_loading_indicator()
    
        # Simulate delay and then finish analysis
        QTimer.singleShot(2000, self.finish_analysis)

    def finish_analysis(self):
        """Send the AI insight from the model to update the View"""
        # Use the stored query instead of getting it from the input field
        print(f"AIAdvisorPresenter: Processing query: {self.current_query}")
        
        # Get AI advice from model
        new_insight = self.model.get_ai_advice(self.current_query)
        
        # Hide the loading indicator instead of loading bar
        self.view.hide_loading_indicator()
        
        # Update the view with new insight
        self.view.add_new_insight(new_insight)
        self.view.update_analysis_button_text("🔍 Send")
        self.view.set_analysis_button_enabled(True)
        self.view.update_last_refresh()

