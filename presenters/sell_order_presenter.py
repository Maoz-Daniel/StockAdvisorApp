from PySide6.QtCore import QObject, Signal, QThread

class WorkerThread(QThread):
    """Worker thread for API calls"""
    finished = Signal(object)
    
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        
    def run(self):
        result = self.function(*self.args, **self.kwargs)
        self.finished.emit(result)


class SellOrderPresenter(QObject):
    # Signals for thread-safe UI updates
    portfolioLoadedSignal = Signal(list)
    stockSelectedSignal = Signal(str, float, list)
    loadingStartedSignal = Signal(str)
    loadingFinishedSignal = Signal()
    
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.current_stock = {
            "symbol": None,
            "price": 0.0,
            "shares_owned": 0,
            "chart_data": []
        }
        
        # Connect signals to view methods
        self.portfolioLoadedSignal.connect(self.view.update_portfolio_list)
        self.stockSelectedSignal.connect(self.view.stock_selected)
        self.loadingStartedSignal.connect(lambda msg: self.view.set_loading_state(True, msg))
        self.loadingFinishedSignal.connect(lambda: self.view.set_loading_state(False))
        
        # Initialize the view
        self.load_user_data()
        self.load_portfolio_data()

    def load_user_data(self):
        """Load user data and update view"""
        username = self.model.get_username()
        self.view.update_user_info(username)

    def load_portfolio_data(self):
        """Load user portfolio from the model"""
        # Show loading state
        self.loadingStartedSignal.emit("Loading portfolio data...")
        
        # Create a worker thread for the database call
        self.worker = WorkerThread(self._load_portfolio_worker)
        self.worker.finished.connect(self._portfolio_loading_completed)
        self.worker.start()
    
    def _load_portfolio_worker(self):
        """Worker function that runs in a separate thread to load portfolio data"""
        # Get the user's portfolio from the model
        portfolio_data = self.model.get_portfolio_data()
        
        # Format the portfolio data for the view
        formatted_portfolio = []
        for item in portfolio_data:
            formatted_portfolio.append({
                "symbol": item["symbol"],
                "shares": int(item["quantity"]),
                "current_price": item["current_price"],
                "total_value": item["market_value"]
            })
            
        return formatted_portfolio
    
    def _portfolio_loading_completed(self, portfolio_data):
        """Handle portfolio loading result from worker thread"""
        # Hide loading indicator
        self.loadingFinishedSignal.emit()
        
        # Send the portfolio data to the view
        self.portfolioLoadedSignal.emit(portfolio_data)
    
    def select_stock(self, symbol, shares_owned):
        """Handle stock selection from the portfolio list"""
        # Show loading state
        self.loadingStartedSignal.emit(f"Loading data for {symbol}...")
        
        # Create a worker thread for data loading
        self.worker = WorkerThread(self._select_stock_worker, symbol, shares_owned)
        self.worker.finished.connect(self._stock_selection_completed)
        self.worker.start()
        
    
    def _select_stock_worker(self, symbol, shares_owned):
        """Worker function to get stock data"""
        try:
            # Get current price and chart data for the selected stock
            price = self.model.get_current_price(symbol)
            chart_data = self.model.get_stock_history(symbol)
            
            # Debug output
            print(f"Retrieved price for {symbol}: {price}")
            print(f"Retrieved chart data for {symbol}: {chart_data[:5] if chart_data else 'None'}")
            
            return {
                "symbol": symbol,
                "price": price,
                "shares_owned": shares_owned,
                "chart_data": chart_data
            }
        except Exception as e:
            print(f"Error in _select_stock_worker: {str(e)}")
            return {
                "symbol": symbol,
                "price": 0.0,
                "shares_owned": shares_owned,
                "chart_data": []
            }
    
    def _stock_selection_completed(self, result):
        """Handle stock selection result from worker thread"""
        # Hide loading indicator
        self.loadingFinishedSignal.emit()
        
        # Store the current stock data
        self.current_stock = result
        
        # Emit signal to update the view
        self.stockSelectedSignal.emit(
            result["symbol"],
            result["price"],
            result["chart_data"]
        )
        
        # Update the view with shares owned
        self.view.update_shares_owned(result["shares_owned"])
    
    def preview_order(self, symbol, quantity):
        """Generate a preview of the sell order"""
        try:
            # Check if the quantity is valid
            shares_owned = self.current_stock["shares_owned"]
            if quantity > shares_owned:
                self.view.show_error_message(f"You only own {shares_owned} shares of {symbol}")
                return False
            
            # Get current price for the stock
            float_price = self.model.get_current_price(symbol)
            total_value = float_price * quantity
            commission = total_value * 0.01  # Example: 1% commission
            
            preview_info = {
                "stock": symbol,
                "quantity": quantity,
                "price_per_share": float_price,
                "estimated_total": total_value,
                "commission": commission,
                "total_after_commission": total_value - commission,
                "shares_remaining": shares_owned - quantity
            }
            
            self.view.display_order_preview(preview_info)
            return True
            
        except Exception as e:
            self.view.show_error_message(f"Error generating preview: {str(e)}")
            return False
    
    def process_sell_order(self, symbol, quantity):
        """Process the sell order through the model"""
        try:
            # Check if the quantity is valid
            shares_owned = self.current_stock["shares_owned"]
            if quantity > shares_owned:
                self.view.show_error_message(f"You only own {shares_owned} shares of {symbol}")
                return False
            
            # Get current price for the stock
            float_price = self.model.get_current_price(symbol)
            
            # Execute sell through model
            success = self.model.sell_stock(symbol, quantity, float_price)
            
            if success:
                self.view.show_success_message(
                    f"Successfully sold {quantity} shares of {symbol} at ${float_price:.2f}"
                )
                return True
            else:
                self.view.show_error_message("Failed to process sell order.")
                return False
                
        except Exception as e:
            self.view.show_error_message(f"Error processing order: {str(e)}")
            return False