from models.mock_stock_model import MockStockModel

class TradeHistoryPresenter:
    def __init__(self, view):
        """ מחבר את ה-View למודל ושולט בלוגיקה של ההיסטוריה """
        self.view = view
        self.model = MockStockModel()  # מקור הנתונים

    def load_trade_history(self):
        """ טוען את כל היסטוריית העסקאות ומעדכן את ה-View """
        trade_history = self.model.get_trade_history(start_date=None, end_date=None, stocks=[])
        self.view.update_trade_table(trade_history)  # שליחת הנתונים ל-View

    def filter_trade_history(self, start_date, end_date, selected_stocks, selected_actions):
        """ מסנן את היסטוריית העסקאות לפי תאריך, מניות וסוגי פעולות """
        print(f"📌 Presenter: Filtering trades from {start_date} to {end_date} for stocks: {selected_stocks}, Actions: {selected_actions}")

        filtered_data = self.model.get_trade_history(start_date, end_date, selected_stocks, selected_actions)

        print(f"📊 Filtered Data Received ({len(filtered_data)} results): {filtered_data}")

        self.view.update_trade_table(filtered_data)  # שליחת הנתונים המסוננים ל-View

    def load_trade_chart_data(self):
        """ טוען את הנתונים לגרף ומעדכן את ה-View """
        chart_data = self.model.get_trade_chart_data()
        print("📊 Sending Line Chart Data:", chart_data)

        print("chart_data:", chart_data)
        self.view.update_chart(chart_data)  # שולח ל-View

    def load_trade_bar_chart_data(self):
        """ טוען את הנתונים לגרף העמודות ומעדכן את ה-View """
        bar_chart_data = self.model.get_trade_bar_chart_data()
        print("📊 Bar Chart Data:", bar_chart_data)
        self.view.update_bar_chart(bar_chart_data)  # שולח ל-View

    def get_bar_chart_data(self):
        """ מחזיר את הנתונים לגרף העמודות """
        return self.model.get_trade_bar_chart_data()

    def get_chart_data(self):
        """ מחזיר את נתוני הגרף הקווי ללא עדכון התצוגה """
        return self.model.get_trade_chart_data()