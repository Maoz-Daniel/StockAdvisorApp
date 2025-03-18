# buy_order_presenter.py
from models.mock_stock_model import MockStockModel
from PySide6.QtWidgets import QMessageBox

class BuyOrderPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.load_user_data()
        self.load_available_stocks()

    def load_user_data(self):
        """Load user data and update view"""
        username = self.model.get_username()
        self.view.update_user_info(username)

    def load_available_stocks(self):
        """Load available stocks from model and update view"""
        # Get available stocks from model - we could enhance the model to provide this
        stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"]
        self.view.update_stock_list(stocks)

    def process_buy_order(self, stock, quantity, price, order_type):
        """Process the buy order through the model"""
        try:
            # Convert price to float if it's not "Market Price"
            float_price = float(price) if price != "Market Price" else self.get_market_price(stock)
            
            # Execute buy through model
            success = self.model.buy_stock(stock, quantity, float_price)
            
            if success:
                self.view.show_success_message(f"Successfully purchased {quantity} shares of {stock} at ${float_price:.2f}")
                return True
            else:
                self.view.show_error_message("Failed to process buy order. Please check your account balance.")
                return False
                
        except ValueError:
            self.view.show_error_message("Invalid price format. Please enter a valid number.")
            return False
        except Exception as e:
            self.view.show_error_message(f"Error processing order: {str(e)}")
            return False

    def get_market_price(self, stock):
        """Get current market price for a stock - could be enhanced in the model"""
        # In a real application, this would fetch real-time prices
        # Here we're using portfolio data if available
        if stock in self.model.portfolio:
            return self.model.portfolio[stock]["price"]
        # Default price if stock not in portfolio
        return 100.0  # Default price

    def preview_order(self, stock, quantity, price, order_type):
        """Generate a preview of the order with estimated costs"""
        try:
            float_price = float(price) if price and price != "Market Price" else self.get_market_price(stock)
            total_cost = float_price * quantity
            commission = total_cost * 0.01  # Example: 1% commission
            
            preview_info = {
                "stock": stock,
                "quantity": quantity,
                "price_per_share": float_price,
                "order_type": order_type,
                "estimated_total": total_cost,
                "commission": commission,
                "total_with_commission": total_cost + commission
            }
            
            self.view.display_order_preview(preview_info)
            return True
            
        except ValueError:
            self.view.show_error_message("Invalid price format. Please enter a valid number.")
            return False
        except Exception as e:
            self.view.show_error_message(f"Error generating preview: {str(e)}")
            return False