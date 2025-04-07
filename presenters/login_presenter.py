# login_presenter.py
from models.mock_stock_model import MockStockModel
from PySide6.QtCore import QThread, Signal, QObject, QTimer

class DataLoaderWorker(QObject):
    progress_update = Signal(int, str)  # Progress value, status message
    finished = Signal()
    
    def __init__(self, model, username):
        super().__init__()
        self.model = model
        self.username = username
        self.is_loaded = False
    
    def load_data(self):
        """Load data for the main view with progress updates"""
        print(f"DataLoaderWorker: Loading data for user {self.username}")
        
        # Start by letting the UI know we're beginning
        self.progress_update.emit(0, "Initializing dashboard...")
        
        # Load portfolio data - approx. 40% of total work
        self.progress_update.emit(5, "Loading portfolio data...")
        portfolio_data = self.model.get_portfolio_data()
        self.model.cached_portfolio_data = portfolio_data

        self.progress_update.emit(40, "Portfolio data loaded.")
        
        # Load market data - approx. 20% of total work
        self.progress_update.emit(45, "Loading market data...")
        self.load_market_data()
        self.progress_update.emit(60, "Market data loaded.")
        
        # Load trade history - approx. 20% of total work
        self.progress_update.emit(65, "Loading transaction history...")
        user_id = getattr(self.model, "user_id", 1)
        self.model.trade_history = self.model.get_user_transactions(user_id)
        self.progress_update.emit(80, "Transaction history loaded.")
        
        # Preload all current prices for portfolio items (critical for smooth display)
        self.progress_update.emit(85, "Loading stock prices...")
        for item in portfolio_data:
            symbol = item.get("symbol")
            if symbol:
                # Preload price data (already cached in the model)
                self.model.get_current_price(symbol)
        self.progress_update.emit(95, "Stock prices loaded.")
        
        # Final initialization - ready to show main view
        import time
        self.progress_update.emit(98, "Preparing interface...")
        time.sleep(0.5)  # Small delay to ensure UI is responsive
        
        # Complete
        self.progress_update.emit(100, "Ready!")
        
        # Important: Wait briefly before signaling completion to ensure
        # all model data is loaded and the dialog has updated
        time.sleep(0.5)
        self.is_loaded = True
        self.finished.emit()
    
    def load_market_data(self):
        """Load market data for display"""
        # In a real implementation, this would fetch market data
        # from an API or other data source
        import time
        time.sleep(0.5)  # Simulate loading time


class LoginPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.data_loader = None
        self.loader_thread = None
    
    def perform_login(self, username, password):
        """Original login method kept exactly as it was"""
        print(f"LoginPresenter.perform_login() called with username={username}, password={password}")
        result = self.model.login(username, password)
        if result:
            print(f"LoginPresenter: Setting username in model to: {username}")
            self.model.set_username(username)
            print("LoginPresenter: Login successful")
        else:
            print("LoginPresenter: Login failed")
        return result
    
    def start_loading_data(self, username, view):
        """Start loading data for the main view with progress updates"""
        # Save the view reference
        self.view = view
        
        # Create data loader worker
        self.data_loader = DataLoaderWorker(self.model, username)
        
        # Connect signals
        self.data_loader.progress_update.connect(view.update_progress)
        self.data_loader.finished.connect(self.on_data_loaded)
        
        # Create thread for loading data
        self.loader_thread = QThread()
        self.data_loader.moveToThread(self.loader_thread)
        self.loader_thread.started.connect(self.data_loader.load_data)
        
        # Start the thread
        self.loader_thread.start()
    
    def on_data_loaded(self):
        """Called when data loading is complete"""
        print("LoginPresenter: Data loading complete")
        
        # Use the signal to close the dialog from the main thread
        self.view.close_dialog.emit()
        
        # Clean up thread
        if self.loader_thread:
            self.loader_thread.quit()
            self.loader_thread.wait()