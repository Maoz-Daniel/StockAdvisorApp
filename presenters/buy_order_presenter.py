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


class BuyOrderPresenter(QObject):
    # Signals for thread-safe UI updates
    stockFoundSignal = Signal(str, float, str, list)
    stockNotFoundSignal = Signal(str, str)
    loadingStartedSignal = Signal(str)
    loadingFinishedSignal = Signal()
    
    def __init__(self, view, model):
        super().__init__()
        self.view = view
        self.model = model
        self.current_stock = {
            "symbol": None,
            "price": 0.0,
            "chart_data": []
        }
        
        # Connect signals to view methods
        self.stockFoundSignal.connect(self.view.stock_found)
        self.stockNotFoundSignal.connect(self.view.stock_not_found)
        self.loadingStartedSignal.connect(lambda msg: self.view.set_loading_state(True, msg))
        self.loadingFinishedSignal.connect(lambda: self.view.set_loading_state(False))
        
        # Initialize the view
        self.load_user_data()
        self.load_available_stocks()

    def load_user_data(self):
        """Load user data and update view"""
        username = self.model.get_username()
        self.view.update_user_info(username)

    def load_available_stocks(self):
        """Load available stocks from model and update view"""
        # We could enhance the model to provide this
        # For now, we'll use a hardcoded list as a fallback
        stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NFLX"]
        self.view.update_stock_list(stocks)

    def search_stock_by_name(self, company_name):
        """Search for a stock by company name using the API"""
        if not company_name:
            self.view.show_error("Please enter a company name")
            return
        
        # Show loading state via signal
        self.loadingStartedSignal.emit(f"Searching for {company_name}...")
        
        # Create a worker thread for the API call
        self.worker = WorkerThread(self._search_stock_worker, company_name)
        self.worker.finished.connect(self._search_completed)
        self.worker.start()
    
    def _search_stock_worker(self, company_name):
        """Worker function that runs in a separate thread"""
        # Search for the stock symbol
        success, symbol, error_message = self.model.search_symbol_by_name(company_name)
        
        if success and symbol:
            # Get current price and chart data
            price = self.model.get_current_price(symbol)
            chart_data = self.model.get_stock_history(symbol)
            
            return {
                "success": True,
                "symbol": symbol,
                "price": price,
                "company_name": company_name,
                "chart_data": chart_data
            }
        else:
            return {
                "success": False,
                "company_name": company_name,
                "error_message": error_message or "Stock not found"
            }
    
    def _search_completed(self, result):
        """Handle the search result from the worker thread"""
        # Hide loading indicator
        self.loadingFinishedSignal.emit()
        
        if result["success"]:
            # Stock was found
            symbol = result["symbol"]
            price = result["price"]
            company_name = result["company_name"]
            chart_data = result["chart_data"]
            
            # Store current stock data
            self.current_stock = {
                "symbol": symbol,
                "price": price,
                "chart_data": chart_data
            }
            
            # Emit signal to update the view
            self.stockFoundSignal.emit(symbol, price, company_name, chart_data)
        else:
            # Stock was not found
            company_name = result["company_name"]
            error_message = result["error_message"]
            
            # Emit signal to update the view
            self.stockNotFoundSignal.emit(company_name, error_message)

    def process_buy_order(self, stock, quantity):
        """Process the buy order through the model"""
        try:
            # Get current price for the stock
            float_price = self.model.get_current_price(stock)
            
            # Execute buy through model
            success = self.model.buy_stock(stock, quantity, float_price)
            
            if success:
                self.view.show_success_message(f"Successfully purchased {quantity} shares of {stock} at ${float_price:.2f}")
                return True
            else:
                self.view.show_error_message("Failed to process buy order. Please check your account balance.")
                return False
                
        except Exception as e:
            self.view.show_error_message(f"Error processing order: {str(e)}")
            return False

    def preview_order(self, stock, quantity):
        """Generate a preview of the order with estimated costs"""
        try:
            float_price = self.model.get_current_price(stock)
            total_cost = float_price * quantity
            commission = total_cost * 0.01  # Example: 1% commission
            
            preview_info = {
                "stock": stock,
                "quantity": quantity,
                "price_per_share": float_price,
                "estimated_total": total_cost,
                "commission": commission,
                "total_with_commission": total_cost + commission
            }
            
            self.view.display_order_preview(preview_info)
            return True
            
        except Exception as e:
            self.view.show_error_message(f"Error generating preview: {str(e)}")
            return False
    