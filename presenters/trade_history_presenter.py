from models.mock_stock_model import MockStockModel

class TradeHistoryPresenter:
    def __init__(self, view):
        """מחבר את ה-View למודל ושולט בלוגיקה של ההיסטוריה"""
        self.view = view
        self.model = MockStockModel()  # מקור הנתונים
        self.current_chart_type = "bar"  # ניהול מצב הגרף בתוך ה-Presenter

    def load_trade_history(self):
        """טוען את כל היסטוריית העסקאות ומעדכן את ה-View"""
        trade_history = self.model.get_trade_history(start_date=None, end_date=None, stocks=[])
        self.view.update_trade_table(trade_history)  # שליחת הנתונים ל-View

    def filter_trade_history(self, start_date, end_date, selected_stocks, selected_actions):
        """מסנן את היסטוריית העסקאות לפי תאריך, מניות וסוגי פעולות"""
        print(f"📌 Presenter: Filtering trades from {start_date} to {end_date} for stocks: {selected_stocks}, Actions: {selected_actions}")
        filtered_data = self.model.get_trade_history(start_date, end_date, selected_stocks, selected_actions)
        print(f"📊 Filtered Data Received ({len(filtered_data)} results): {filtered_data}")
        self.view.update_trade_table(filtered_data)  # שליחת הנתונים המסוננים ל-View

    def load_trade_chart_data(self):
        """טוען את הנתונים לגרף ומעדכן את ה-View"""
        chart_data = self.model.get_trade_chart_data()
        print("📊 Sending Line Chart Data:", chart_data)
        self.view.update_chart(chart_data)  # שולח ל-View

    def load_trade_bar_chart_data(self):
        """טוען את הנתונים לגרף העמודות ומעדכן את ה-View"""
        bar_chart_data = self.model.get_trade_bar_chart_data()
        print("📊 Bar Chart Data:", bar_chart_data)
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
            print("📊 Switching to Line Chart with data:", line_chart_data)
            self.view.update_chart(line_chart_data)
        else:
            self.current_chart_type = "bar"
            bar_chart_data = self.model.get_trade_bar_chart_data()
            print("📊 Switching to Bar Chart with data:", bar_chart_data)
            self.view.update_bar_chart(bar_chart_data)
