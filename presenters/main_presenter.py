from models.mock_stock_model import MockStockModel
from views.buy_order_view import BuyOrderWindow
from views.sell_order_view import SellOrderWindow
from views.ai_advisor_view import AIAdvisorWindow
from views.trade_history_view import TradeHistoryWindow
from PySide6.QtCore import QDate

class MainPresenter:
    def __init__(self, view,model):
        """ קונסטרקטור שמקבל את ה-View ומחבר אותו ל-Model """
        self.view = view
        self.model = model
        print(f"MainPresenter.__init__: Received model with username: {model.get_username()}")

    def load_user_data(self):
        """ Load username and update main header """
        username = self.model.get_username()
        self.view.update_header(f"Welcome, {username}!")
        self.view.update_status_bar(f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')} 10:30")


    def load_portfolio_data(self):
        """Load portfolio data and summary"""
        # Get portfolio data (which also calculates totals)
        portfolio_data = self.model.get_portfolio_data()
        
        # Update the table
        self.view.update_portfolio_table(portfolio_data)
        
        # Get the totals (which were already calculated)
        total_value, total_unrealized_pl = self.model.get_portfolio_total_value()
        
        # Update the summary view
        self.view.update_portfolio_summary(total_value, total_unrealized_pl)

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

    def load_portfolio_summary(self):
        print("DEBUGGING: load_portfolio_summary method called")
        total_value, total_unrealized_pl = self.model.get_portfolio_total_value()
        print(f"DEBUGGING: Got total_value from model: ${total_value:.2f}")
        print(f"DEBUGGING: Got total_unrealized_pl from model: ${total_unrealized_pl:.2f}")
        self.view.update_portfolio_summary(total_value, total_unrealized_pl)
        print("DEBUGGING: Called view.update_portfolio_summary")

    def get_trade_history(self, start_date, end_date, stocks):
        """ מחזיר היסטוריית עסקאות מסוננת """
        return self.model.get_trade_history(start_date, end_date, stocks)

    def get_ai_advice(self, query):
        """ מחזיר ייעוץ AI מהמודל """
        return self.model.get_ai_advice(query)

    def open_buy_order(self):
        """ Open window for buying stocks """
        self.view.buy_order_window = BuyOrderWindow(self.model)
        self.view.buy_order_window.show()

    def open_sell_order(self):
        """ Open window for selling stocks """
        self.view.sell_order_window = SellOrderWindow(self.model)
        self.view.sell_order_window.show()

    def open_ai_advisor(self):
        """ Open AI advisor window """
        self.view.ai_advisor_window = AIAdvisorWindow(self.model)
        self.view.ai_advisor_window.show()

    def open_trade_history(self):
        """ Open trade history window """
        self.view.trade_history_window = TradeHistoryWindow(self.model)
        self.view.trade_history_window.show()
        print(f"open_trade_history: Model username before opening window: {self.model.get_username()}")
