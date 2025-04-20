from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QFrame

class AIAdvisorPresenter:
    def __init__(self, view, model):
        """Connect the View to the model and control the AI analysis logic"""
        self.view = view
        self.model = model  # Can be replaced with a dedicated model if exists

    def run_ai_analysis(self):
        """Run AI analysis - update analysis button, simulate delay, and return new insight"""
        # Update button status via View
        self.view.update_analysis_button_text("🔄 Analyzing...")
        self.view.set_analysis_button_enabled(False)
       
        # Simulate delay and then finish analysis
        QTimer.singleShot(2000, self.finish_analysis)

    def finish_analysis(self):
        """Send the AI insight from the model to update the View"""
        # Get the user's message from the input field
        user_query = self.view.input_field.toPlainText().strip()
        
        # Get AI advice from model
        new_insight = self.model.get_ai_advice(user_query)
        
        # Update the view with new insight
        self.view.add_new_insight(new_insight)
        self.view.update_analysis_button_text("🔍 Send")
        self.view.set_analysis_button_enabled(True)
        self.view.update_last_refresh()