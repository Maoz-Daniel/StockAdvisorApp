from models.mock_stock_model import MockStockModel

class TradeHistoryPresenter:
    def __init__(self, view, model):
        """מחבר את ה-View למודל ושולט בלוגיקה של ההיסטוריה"""
        self.view = view
        self.model = model  # מקור הנתונים
        self.current_chart_type = "bar"  # ניהול מצב הגרף בתוך ה-Presenter

    def load_trade_history(self):
        """טוען את כל היסטוריית העסקאות עבור המשתמש ומעדכן את ה-View"""
        # נניח שה-Model שומר את user_id לאחר התחברות
        user_id = getattr(self.model, "user_id", 1)  # ערך ברירת מחדל אם אין עדיין התחברות
        trade_history = self.model.get_user_transactions(user_id)
        self.view.update_trade_table(trade_history)


    def filter_trade_history(self, start_date, end_date, selected_stocks, selected_actions):
        """מסנן את היסטוריית העסקאות לפי תאריך, מניות וסוגי פעולות, תוך שימוש בנתונים שכבר נשלפו."""
        # שליפת נתונים מעודכנים פעם אחת עבור המשתמש
        user_id = getattr(self.model, "user_id", 1)
        transactions = self.model.get_user_transactions(user_id)
        
        # סינון הנתונים שהתקבלו
        filtered_data = self.model.get_trade_history(transactions, start_date, end_date, selected_stocks, selected_actions)
        self.view.update_trade_table(filtered_data)


    def load_trade_chart_data(self):
        """טוען את הנתונים לגרף ומעדכן את ה-View"""
        chart_data = self.model.get_trade_chart_data()
        self.view.update_chart(chart_data)  # שולח ל-View

    def load_trade_bar_chart_data(self):
        """טוען את הנתונים לגרף העמודות ומעדכן את ה-View"""
        bar_chart_data = self.model.get_trade_bar_chart_data()
        self.view.update_bar_chart(bar_chart_data)  # שולח ל-View

    def get_bar_chart_data(self):
        """מחזיר את הנתונים לגרף העמודות"""
        return self.model.get_trade_bar_chart_data()

    def get_chart_data(self):
        """מחזיר את נתוני הגרף הקווי ללא עדכון התצוגה"""
        return self.model.get_trade_chart_data()

    # ← הפונקציה החדשה לניהול החלפת סוג הגרף:
    def toggle_chart_type(self):
        """מטפלת בהחלפת סוג הגרף ומעדכנת את ה-View בהתאם"""
        if self.current_chart_type == "bar":
            self.current_chart_type = "line"
            line_chart_data = self.model.get_trade_chart_data()
            self.view.update_chart(line_chart_data)
        else:
            self.current_chart_type = "bar"
            bar_chart_data = self.model.get_trade_bar_chart_data()
            self.view.update_bar_chart(bar_chart_data)
