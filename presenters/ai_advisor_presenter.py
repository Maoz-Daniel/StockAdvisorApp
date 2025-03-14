from models.mock_stock_model import MockStockModel
from PySide6.QtCore import QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QFrame


class AIAdvisorPresenter:
    def __init__(self, view):
        """מחבר את ה-View למודל ושולט בלוגיקה של ניתוח ה-AI"""
        self.view = view
        self.model = MockStockModel()  # ניתן להחליף במודל ייעודי אם קיים

    def run_ai_analysis(self):
        """מפעיל ניתוח AI – מעדכן את כפתור הניתוח, מדמה השהייה, ומחזיר תובנה חדשה"""
        # עדכון מצב הכפתור דרך ה-View
        self.view.update_analysis_button_text("🔄 Analyzing...")
        self.view.set_analysis_button_enabled(False)
        # for frame in self.findChildren(QFrame):
        #     animation = QPropertyAnimation(frame, b"geometry")
        #     animation.setDuration(300)
        #     animation.setStartValue(frame.geometry())
        #     animation.setEndValue(frame.geometry())
        #     animation.setEasingCurve(QEasingCurve.OutBack)
        #     animation.start()
       
        QTimer.singleShot(2000, self.finish_analysis)

    def finish_analysis(self):
        """שולח את תובנת ה-AI שהתקבלה מהמודל לעדכון ה-View"""
        new_insight = self.model.get_ai_advice("dummy query")
        self.view.add_new_insight(new_insight)
        self.view.update_analysis_button_text("🔍 Perform AI Analysis")
        self.view.set_analysis_button_enabled(True)
        self.view.update_last_refresh()
