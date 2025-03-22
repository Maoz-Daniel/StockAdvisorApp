import random
import requests
from datetime import datetime, timedelta

class MockStockModel:
    def __init__(self):

        self.api_base_url = "http://localhost:5124/api"

        # שם המשתמש המחובר (דמה)
        self.username = "deafult_user"
        # רשימת משתמשים (דוגמה)
        self.users = {
            "maoz": "3242",
            "1": "1",
            "noam": "123"
        }

        
        
        # נתוני תיק השקעות (דמה)
        self.portfolio = {
            "AAPL": {"price": 182.30, "quantity": 35},
            "GOOGL": {"price": 2835.55, "quantity": 5},
            "MSFT": {"price": 419.20, "quantity": 10},
            "TSLA": {"price": 167.50, "quantity": 12},
            "AMZN": {"price": 183.80, "quantity": 8},
        }

        self.trade_history = [
            {"date": datetime.now() - timedelta(days=10), "stock": "AAPL", "action": "Buy", "quantity": 10, "price": 180.00},
            {"date": datetime.now() - timedelta(days=8), "stock": "GOOGL", "action": "Sell", "quantity": 2, "price": 2850.00},
            {"date": datetime.now() - timedelta(days=6), "stock": "MSFT", "action": "Buy", "quantity": 5, "price": 415.00},
            {"date": datetime.now() - timedelta(days=4), "stock": "TSLA", "action": "Buy", "quantity": 7, "price": 200.00},
            {"date": datetime.now() - timedelta(days=3), "stock": "AMZN", "action": "Sell", "quantity": 3, "price": 3400.00},
            {"date": datetime.now() - timedelta(days=2), "stock": "NFLX", "action": "Buy", "quantity": 8, "price": 500.00},
            {"date": datetime.now() - timedelta(days=1), "stock": "META", "action": "Sell", "quantity": 6, "price": 280.00},
            {"date": datetime.now(), "stock": "NVDA", "action": "Buy", "quantity": 4, "price": 750.00},
        ]
    
    def get_trade_chart_data(self):
        chart_data = []
        for i, trade in enumerate(self.trade_history):
            value = trade["quantity"] * trade["price"]  # חישוב הערך הכולל של העסקה
            chart_data.append((i + 1, value))  # (X=אינדקס, Y=שווי העסקה)
        
        return chart_data

    def get_trade_bar_chart_data(self):
        """ מחזיר נתוני גרף עמודות: כמה עסקאות בוצעו לכל מניה """
        trade_counts = {}  # מילון לספירת עסקאות לפי מניה

        for trade in self.trade_history:
            stock = trade["stock"]
            trade_counts[stock] = trade_counts.get(stock, 0) + 1

        # יצירת רשימה מותאמת לגרף [(מניה, כמות עסקאות)]
        return list(trade_counts.items())
    
    def set_username(self, username):
        print(f"MockStockModel.set_username: Setting username to {username}")
        self.username = username

    def get_username(self):
        print(f"MockStockModel.get_username: Returning username: {self.username}")
        return self.username

    def get_portfolio_data(self):
        print("MockStockModel.get_portfolio_data() called")
        return [
            (stock, f"${data['price']:.2f}", f"{data['quantity']}", f"${data['price'] * data['quantity']:.2f}")
            for stock, data in self.portfolio.items()
        ]

    def buy_stock(self, stock, quantity, price):
        print(f"MockStockModel.buy_stock() called with stock={stock}, quantity={quantity}, price={price}")
        if stock in self.portfolio:
            self.portfolio[stock]["quantity"] += quantity
            self.portfolio[stock]["price"] = price
        else:
            self.portfolio[stock] = {"price": price, "quantity": quantity}
        self.trade_history.append({
            "date": datetime.now(),
            "stock": stock,
            "action": "Buy",
            "quantity": quantity,
            "price": price
        })
        return True

    def sell_stock(self, stock, quantity, price):
        print(f"MockStockModel.sell_stock() called with stock={stock}, quantity={quantity}, price={price}")
        if stock in self.portfolio and self.portfolio[stock]["quantity"] >= quantity:
            self.portfolio[stock]["quantity"] -= quantity
            self.portfolio[stock]["price"] = price
            if self.portfolio[stock]["quantity"] == 0:
                del self.portfolio[stock]
            self.trade_history.append({
                "date": datetime.now(),
                "stock": stock,
                "action": "Sell",
                "quantity": quantity,
                "price": price
            })
            return True
        print("Sell stock failed: insufficient quantity or stock not in portfolio")
        return False

    def get_trade_history(self, start_date=None, end_date=None, stocks=[], actions=[]):
        print(f"MockStockModel.get_trade_history() called with start_date={start_date}, end_date={end_date}, stocks={stocks}, actions={actions}")
        
        filtered_trades = [
            t for t in self.trade_history
            if (start_date is None or start_date <= t["date"].date() <= end_date) and
            (not stocks or t["stock"] in stocks) and
            (not actions or t["action"] in actions)  # ✅ הוספת תנאי לפי Buy/Sell
        ]

        print(f"✅ Returning {len(filtered_trades)} filtered trades: {filtered_trades}")
        return filtered_trades


    def get_ai_advice(self, query):
        print(f"MockStockModel.get_ai_advice() called with query: {query}")
        advices = [
            "השוק תנודתי - שקול השקעה מבוזרת!",
            "האם בדקת את המדדים הטכניים לפני הרכישה?",
            "מומלץ להחזיק מניות לטווח ארוך כדי להפחית סיכונים.",
            "השקעה במניות טכנולוגיה היא מגמה עכשווית, אך יש לשים לב לסיכונים."
        ]
        return random.choice(advices)

    def login(self, username, password):
        """
        Authenticate user against the backend API
        """
        print(f"MockStockModel.login() called with username={username}, password={password}")
        
        try:
            response = requests.post(
                f"{self.api_base_url}/Auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                # Login successful
                user_data = response.json()
                self.username = username
                
                # Store user ID if available
                if 'userId' in user_data:
                    self.user_id = user_data['userId']
                    
                print(f"MockStockModel.login(): Login successful. User ID: {self.user_id}")
                return True
            else:
                print(f"MockStockModel.login(): Login failed. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"MockStockModel.login(): API Error: {str(e)}")
            
            # Fallback to mock data if API is unavailable
            if username in self.users and self.users[username] == password:
                self.username = username
                print("MockStockModel.login(): Fallback to mock data - Login successful")
                return True
                
            print("MockStockModel.login(): Login failed")
            return False
        
    def register(self, username, password, email):
        """
        Register a new user with the backend
        """
        try:
            response = requests.post(
                f"{self.api_base_url}/Auth/register",
                json={"username": username, "password": password, "email": email}
            )
            
            return response.status_code == 200
                
        except Exception as e:
            print(f"MockStockModel.register(): API Error: {str(e)}")
            return False
    
def set_user_id(self, user_id):
        """
        Set the user ID received from the backend
        """
        self.user_id = user_id
        print(f"MockStockModel: User ID set to {user_id}")

def get_stock_info(self, stock_symbol):
    """Get detailed information about a specific stock"""
    if stock_symbol in self.portfolio:
        return {
            "symbol": stock_symbol,
            "quantity": self.portfolio[stock_symbol]["quantity"],
            "price": self.portfolio[stock_symbol]["price"],
            "value": self.portfolio[stock_symbol]["quantity"] * self.portfolio[stock_symbol]["price"]
        }
    return None

def get_portfolio_summary(self):
    """Get a summary of the user's portfolio"""
    total_value = sum(stock["price"] * stock["quantity"] for stock in self.portfolio.values())
    stock_count = len(self.portfolio)
    return {
        "total_value": total_value,
        "stock_count": stock_count,
        "username": self.username
    }
    
def calculate_transaction_cost(self, price, quantity, transaction_type="buy"):
    """Calculate total cost including fees for a transaction"""
    base_cost = price * quantity
    # Example fee structure
    if transaction_type == "buy":
        commission = max(4.95, base_cost * 0.005)  # $4.95 or 0.5%, whichever is higher
    else:  # sell
        commission = max(4.95, base_cost * 0.005)
    
    return {
        "base_cost": base_cost,
        "commission": commission,
        "total": base_cost + commission if transaction_type == "buy" else base_cost - commission
    }