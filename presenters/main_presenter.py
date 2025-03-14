from models.mock_stock_model import MockStockModel
from views.buy_order_view import BuyOrderWindow
from views.sell_order_view import SellOrderWindow
from views.ai_advisor_view import AIAdvisorWindow
from views.trade_history_view import TradeHistoryWindow
from PySide6.QtCore import QDate

class MainPresenter:
    def __init__(self, view):
        """ קונסטרקטור שמקבל את ה-View ומחבר אותו ל-Model """
        self.view = view
        self.model = MockStockModel()  # שימוש בנתוני דמה

    def load_user_data(self):
        """ טוען את שם המשתמש ומעדכן את הכותרת הראשית """
        self.model.username = self.view.username
        username = self.model.get_username()

        self.view.update_header(f"Welcome, {username}!")  # קריאה ל-View לעדכן כותרת
        self.view.update_status_bar(f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30")


    def load_portfolio_data(self):
        """ טוען את נתוני התיק מהמודל ומעדכן את הטבלה ב-View """
        portfolio_data = self.model.get_portfolio_data()
        self.view.update_portfolio_table(portfolio_data)  # קריאה ל-View לעדכן טבלה

    def buy_stock(self, stock, quantity, price):
        """ מבצע רכישת מניה ועדכון ב-Model """
        success = self.model.buy_stock(stock, quantity, price)
        if success:
            self.load_portfolio_data()  # עדכון התצוגה לאחר קנייה

    def sell_stock(self, stock, quantity, price):
        """ מבצע מכירה של מניה ועדכון ב-Model """
        success = self.model.sell_stock(stock, quantity, price)
        if success:
            self.load_portfolio_data()  # עדכון התצוגה לאחר מכירה

    def get_trade_history(self, start_date, end_date, stocks):
        """ מחזיר היסטוריית עסקאות מסוננת """
        return self.model.get_trade_history(start_date, end_date, stocks)

    def get_ai_advice(self, query):
        """ מחזיר ייעוץ AI מהמודל """
        return self.model.get_ai_advice(query)

    # ✅ פונקציות לפתיחת חלונות מה-View
    def open_buy_order(self):
        """ פותח חלון לרכישת מניות """
        self.view.buy_order_window = BuyOrderWindow(self.view.username)
        self.view.buy_order_window.show()

    def open_sell_order(self):
        """ פותח חלון למכירת מניות """
        self.view.sell_order_window = SellOrderWindow(self.view.username)
        self.view.sell_order_window.show()

    def open_ai_advisor(self):
        """ פותח חלון ליועץ AI """
        self.view.ai_advisor_window = AIAdvisorWindow(self.view.username)
        self.view.ai_advisor_window.show()

    def open_trade_history(self):
        """ פותח חלון להיסטוריית מסחר """
        self.view.trade_history_window = TradeHistoryWindow(self.view.username)
        self.view.trade_history_window.show()
