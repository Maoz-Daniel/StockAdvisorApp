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
        self.model.on_data_changed = self.refresh_portfolio_data

        print(f"MainPresenter.__init__: Received model with username: {model.get_username()}")

        self.display_existing_portfolio_data()


    def display_cached_data(self):
        """Display cached data instead of reloading"""
        if hasattr(self.model, "cached_portfolio_data") and self.model.cached_portfolio_data:
            print("Using cached portfolio data")
            # Update the view with cached data
            self.view.update_portfolio_table(self.model.cached_portfolio_data)
            
            # Use cached totals if available
            if hasattr(self.model, "total_portfolio_value") and hasattr(self.model, "total_unrealized_pl"):
                total_value = self.model.total_portfolio_value
                total_unrealized_pl = self.model.total_unrealized_pl
                self.view.update_portfolio_summary(total_value, total_unrealized_pl)
            else:
                # Fall back to calculating totals from cached data
                total_value, total_unrealized_pl = self.model.get_portfolio_total_value(self.model.cached_portfolio_data)
                self.view.update_portfolio_summary(total_value, total_unrealized_pl)
        else:
            # Fall back to loading fresh data if no cache
            print("No cached data found, loading portfolio data")
            self.load_portfolio_data()

    def display_existing_portfolio_data(self):
        """Display already loaded portfolio data without fetching it again"""
        try:
            # Check if we have cached data to avoid refetching
            if hasattr(self.model, "cached_portfolio_data") and self.model.cached_portfolio_data:
                print("Using cached portfolio data")
                portfolio_data = self.model.cached_portfolio_data
                
                # Update the table
                self.view.update_portfolio_table(portfolio_data)
                
                # Use cached totals if available
                if hasattr(self.model, "total_portfolio_value") and hasattr(self.model, "total_unrealized_pl"):
                    total_value = self.model.total_portfolio_value
                    total_unrealized_pl = self.model.total_unrealized_pl
                    self.view.update_portfolio_summary(total_value, total_unrealized_pl)
                else:
                    # Fall back to calculating totals
                    total_value, total_unrealized_pl = self.model.get_portfolio_total_value()
                    self.view.update_portfolio_summary(total_value, total_unrealized_pl)
            else:
                # Fall back to loading fresh data
                print("No cached data found, loading portfolio data")
                self.load_portfolio_data()
        except Exception as e:
            print(f"Error displaying portfolio data: {e}")

    def load_user_data(self):
        """ Load username and update main header """
        username = self.model.get_username()
        self.view.update_header(f"Welcome, {username}!")
        self.view.update_status_bar(f"Logged in as: {username} | Market Status: Open | Last Update: {QDate.currentDate().toString('dd/MM/yyyy')}")


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

    # In your MainPresenter class
    def refresh_portfolio_data(self):
        """Refresh portfolio data in the main view"""
        try:
            # Get fresh data from the model
            portfolio_data = self.model.get_portfolio_data()
            
            # Update the view with new data
            self.view.update_portfolio_table(portfolio_data)
            
            # Update the summary information
            total_value, total_unrealized_pl = self.model.get_portfolio_total_value()
            self.view.update_portfolio_summary(total_value, total_unrealized_pl)
            
            print("Portfolio data refreshed successfully")
        except Exception as e:
            print(f"Error refreshing portfolio data: {e}")

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
