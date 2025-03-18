# sell_order_presenter.py
from models.mock_stock_model import MockStockModel
from PySide6.QtWidgets import QMessageBox

class SellOrderPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
    
    def initialize(self):
        """Called after the presenter is fully set up on the view side"""
        self.load_user_data()
        self.load_owned_stocks()

    def load_user_data(self):
        """Load user data and update view"""
        username = self.model.get_username()
        self.view.update_user_info(username)

    def load_owned_stocks(self):
        """Load stocks owned by the user and update the view"""
        owned_stocks = list(self.model.portfolio.keys())
        self.view.update_stock_list(owned_stocks, initialize=True)
        # The initialize flag tells the view not to call back to this presenter
    def load_user_data(self):
        """Load user data and update view"""
        username = self.model.get_username()
        self.view.update_user_info(username)

    def load_owned_stocks(self):
        """Load stocks owned by the user and update the view"""
        owned_stocks = list(self.model.portfolio.keys())
        self.view.update_stock_list(owned_stocks)
        
        # Also update quantity limits based on portfolio
        self.update_quantity_limits()

    def update_quantity_limits(self, selected_stock=None):
        """Update the maximum quantity that can be sold based on portfolio"""
        if selected_stock and selected_stock in self.model.portfolio:
            max_quantity = self.model.portfolio[selected_stock]["quantity"]
            self.view.update_quantity_max(max_quantity)
        elif not selected_stock:
            # If no stock selected, just disable the quantity input
            self.view.update_quantity_max(0)

    def process_sell_order(self, stock, quantity, price):
        """Process the sell order through the model"""
        try:
            # Check if user owns enough of this stock
            if stock not in self.model.portfolio or self.model.portfolio[stock]["quantity"] < quantity:
                self.view.show_error_message(f"You don't own enough shares of {stock} to sell {quantity}.")
                return False

            # Convert price to float if it's not "Market Price"
            float_price = float(price) if price != "Market Price" else self.get_market_price(stock)
            
            # Execute sell through model
            success = self.model.sell_stock(stock, quantity, float_price)
            
            if success:
                self.view.show_success_message(f"Successfully sold {quantity} shares of {stock} at ${float_price:.2f}")
                return True
            else:
                self.view.show_error_message("Failed to process sell order.")
                return False
                
        except ValueError:
            self.view.show_error_message("Invalid price format. Please enter a valid number.")
            return False
        except Exception as e:
            self.view.show_error_message(f"Error processing order: {str(e)}")
            return False

    def get_market_price(self, stock):
        """Get current market price for a stock"""
        if stock in self.model.portfolio:
            return self.model.portfolio[stock]["price"]
        return 100.0  # Default price

    def on_stock_selected(self, stock):
        """Handle when a user selects a stock from the dropdown"""
        self.update_quantity_limits(stock)
        current_price = self.get_market_price(stock)
        self.view.update_price_placeholder(f"Current: ${current_price:.2f}")