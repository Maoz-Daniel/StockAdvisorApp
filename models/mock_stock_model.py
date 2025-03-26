import random
import requests
from datetime import datetime, timedelta

class MockStockModel:
    def __init__(self):
        # Base API URL
        self.api_base_url = "http://localhost:5124/api"


        self.portfolio = {
    "AAPL": {"price": 182.30, "quantity": 35},
    "GOOGL": {"price": 2850.00, "quantity": 5},
    "MSFT": {"price": 415.00, "quantity": 10},
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
    
    
    def search_symbol_by_name(self, company_name):
        """
        Search for a stock symbol by company name using the API
        Returns a tuple of (success, symbol, error_message)
        """
        try:
            print(f"Searching for symbol by company name: {company_name}")
            
            # Call the API endpoint
            response = requests.get(
                f"{self.api_base_url}/Stock/search-symbol",
                params={"name": company_name}
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                # Check for both uppercase and lowercase key versions
                symbol = data.get("Symbol") or data.get("symbol")
                
                if symbol:
                    print(f"Found symbol: {symbol} for company: {company_name}")
                    return True, symbol, None
                else:
                    print(f"API returned success but no symbol for: {company_name}")
                    return False, None, "Symbol not found in API response"
            
            # Handle not found case
            elif response.status_code == 404:
                print(f"Company not found: {company_name}")
                return False, None, "The stock name is incorrect or the stock does not exist"
            
            # Handle other errors
            else:
                print(f"API error: {response.status_code} - {response.text}")
                return False, None, f"API Error: {response.status_code}"
                
        except Exception as e:
            error_message = f"Error searching for symbol: {str(e)}"
            print(error_message)
            
           
    
    def get_stock_history(self, symbol, start_date=None, end_date=None):
        """
        Get stock price history from the API
        Returns a list of historical price data points
        """
        try:
            # Default to last 52 weeks if dates not provided
            start_date = start_date or (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            end_date = end_date or datetime.now().strftime("%Y-%m-%d")
            
            print(f"Getting stock history for {symbol} from {start_date} to {end_date}")
            
            # Call the API endpoint
            response = requests.get(
                f"{self.api_base_url}/Stock/{symbol}/yahoo-history",
                params={"from": start_date, "to": end_date}
            )
            
            if response.status_code == 200:
                history_data = response.json()
                chart_data = []
                for record in history_data:
                    # Convert date string to timestamp
                    date = datetime.fromisoformat(record["date"].replace("Z", "+00:00"))
                    timestamp = int(date.timestamp() * 1000)  # Milliseconds for QDateTime
                    close_price = record["close"]
                    chart_data.append((timestamp, close_price))
                
                return chart_data
                    
            else:
                print(f"API error: {response.status_code} - {response.text}")
                # Generate mock data as fallback
                return self.generate_mock_history(symbol)
                    
        except Exception as e:
            print(f"Error getting stock history: {str(e)}")
            # Generate mock data as fallback
            return self.generate_mock_history(symbol)
        
    
    def get_current_price(self, symbol):
        """Get current price for a stock"""
        try:
            response = requests.get(f"{self.api_base_url}/Stock/{symbol}/price")
            
            if response.status_code == 200:
                price_data = response.json()
                
                # Check for different possible field names
                if "currentPrice" in price_data:
                    print(f"Found currentPrice for {symbol}: {price_data['currentPrice']}")
                    return price_data["currentPrice"]
                elif "price" in price_data:  
                    print(f"Found price for {symbol}: {price_data['price']}")
                    return price_data["price"]
                else:
                    print(f"No price field found in response for {symbol}")
            else:
                print(f"API error for {symbol} price: {response.status_code} - {response.text}")
            
            # If we get here, the price API failed - try Yahoo history API
            print(f"Attempting to get latest price from Yahoo history for {symbol}")
            raw_history = self.get_stock_history(symbol)
            
            if raw_history and len(raw_history) > 0:
                # Get the most recent closing price from the tuple (timestamp, close_price)
                latest_price = raw_history[-1][1]
                print(f"Using latest closing price from Yahoo history for {symbol}: {latest_price}")
                return latest_price
            
            # If everything fails, use generic default
            print(f"All price sources failed. Using default price (100.0) for {symbol}")
            return 100.0
                    
        except Exception as e:
            print(f"Error getting current price for {symbol}: {str(e)}")
            
            # Try Yahoo history API in the exception block
            try:
                print(f"Trying Yahoo history after exception for {symbol}")
                raw_history = self.get_stock_history(symbol)
                
                if raw_history and len(raw_history) > 0:
                    latest_price = raw_history[-1][1]
                    print(f"Using latest closing price after exception for {symbol}: {latest_price}")
                    return latest_price
            except Exception as history_error:
                print(f"Error getting historical price: {history_error}")
            
            # Final fallback
            return 100.0
    def get_trade_chart_data(self):
        """Get chart data for trade history visualization"""
        chart_data = []
        for i, trade in enumerate(self.trade_history):
            value = trade["quantity"] * trade["price"]
            chart_data.append((i + 1, value))
        return chart_data

    def get_trade_bar_chart_data(self):
        """Get bar chart data showing trade count per stock"""
        trade_counts = {}
        for trade in self.trade_history:
            stock = trade["stock"]
            trade_counts[stock] = trade_counts.get(stock, 0) + 1
        return list(trade_counts.items())
    
    def set_username(self, username):
        print(f"Setting username to {username}")
        self.username = username

    def get_username(self):
        print(f"Returning username: {self.username}")
        return self.username

    def get_portfolio_data(self):
        print("Getting portfolio data from backend")
        # נניח שהמשתמש מחובר ויש לנו את user_id (אם לא, נשתמש ב-1 כברירת מחדל)
        user_id = getattr(self, "user_id", 1)
        try:
            url = f"{self.api_base_url}/Transaction/portfolio/{user_id}"
            print(f"Fetching portfolio data from: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                portfolio_items = response.json()
                print("Portfolio data received:", portfolio_items)
            else:
                print(f"Failed to get portfolio data: {response.status_code} - {response.text}")
                portfolio_items = []
        except Exception as e:
            print(f"Error getting portfolio data: {e}")
            portfolio_items = []
        
        # לאחר קבלת הנתונים – רשימה של פריטים עם: Symbol, Quantity, AverageBuyPrice
        result = []
        total_portfolio_value = 0.0
        for item in portfolio_items:
            # נסיון לקבל את הערכים – יתכן שהמפתחות שונים (עם אותיות גדולות או קטנות)
            symbol = item.get("Symbol") or item.get("symbol")
            quantity = float(item.get("Quantity") or item.get("quantity") or 0)
            avg_buy_price = float(item.get("AverageBuyPrice") or item.get("averageBuyPrice") or 0)
            # שליפת מחיר נוכחי באמצעות המתודה get_current_price
            current_price = self.get_current_price(symbol)
            market_value = current_price * quantity
            total_portfolio_value += market_value
            
            result.append({
                "symbol": symbol,
                "company_name": "",  # ניתן להוסיף קריאה ל-API לקבלת שם החברה במידה וזה נחוץ
                "quantity": quantity,
                "avg_buy_price": avg_buy_price,
                "current_price": current_price,
                "market_value": market_value,
                "unrealized_pl": (current_price - avg_buy_price) * quantity,
                "daily_change": None,  # ניתן להוסיף קריאה נוספת ל-API לקבלת שינוי יומי
            })
        
        # חשב אחוז הקצאה עבור כל פריט בהתבסס על שווי התיק הכולל
        for item in result:
            if total_portfolio_value > 0:
                item["allocation"] = (item["market_value"] / total_portfolio_value) * 100
            else:
                item["allocation"] = 0
        return result



    def buy_stock(self, stock, quantity, price):
        print(f"Buying stock: {stock}, quantity: {quantity}, price: {price}")

        
        transaction_data = {
            "UserId": getattr(self, "user_id", 1), 
            "Symbol": stock,
            "TransactionType": "BUY",
            "Quantity": float(quantity),
            "Price": float(price)
        }

        try:
            response = requests.post(f"{self.api_base_url}/Transaction", json=transaction_data)
            if response.status_code == 200 or response.status_code == 201:
                print("Transaction recorded in the database successfully.")
            else:
                print(f"Failed to record transaction: {response.status_code} - {response.text}")
                # אפשר להחליט אם ברצונך להחזיר False כדי שה-UI ידע שנכשל
                return False
        except Exception as e:
            print(f"Error calling Transaction API: {str(e)}")
            # כנ"ל - אפשר להחליט מה להחזיר
            return False

        # 2. עדכון ה"פורטפוליו" המקומי (אם עדיין רלוונטי):
        if stock in self.portfolio:
            self.portfolio[stock]["quantity"] += quantity
            self.portfolio[stock]["price"] = price
        else:
            self.portfolio[stock] = {"price": price, "quantity": quantity}

        # 3. הוספה ל-היסטוריית המסחר המקומית (לא חובה, תלוי אם רוצים להציג משהו ב-UI):
        self.trade_history.append({
            "date": datetime.now(),
            "stock": stock,
            "action": "Buy",
            "quantity": quantity,
            "price": price
        })

        return True


    def sell_stock(self, stock, quantity, price):
        print(f"Selling stock: {stock}, quantity: {quantity}, price: {price}")
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

    def get_trade_history(self, transactions, start_date=None, end_date=None, stocks=[], actions=[]):
        """Filter the provided trade transactions based on dates, stocks, and actions."""
        filtered_trades = [
            t for t in transactions
            if (start_date is None or start_date <= t["date"].date() <= end_date)
            and (not stocks or t["stock"] in stocks)
            and (not actions or t["action"] in actions)
        ]
        return filtered_trades


    def get_ai_advice(self, query):
        """Get AI trading advice (mock)"""
        advices = [
            "השוק תנודתי - שקול השקעה מבוזרת!",
            "האם בדקת את המדדים הטכניים לפני הרכישה?",
            "מומלץ להחזיק מניות לטווח ארוך כדי להפחית סיכונים.",
            "השקעה במניות טכנולוגיה היא מגמה עכשווית, אך יש לשים לב לסיכונים."
        ]
        return random.choice(advices)

    def login(self, username, password):
        """Authenticate user"""
        try:
            response = requests.post(
                f"{self.api_base_url}/Auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self.username = username
                
                if 'userId' in user_data:
                    self.user_id = user_data['userId']
                    
                return True
            else:
                # Fallback to mock data if API is unavailable
                if username in self.users and self.users[username] == password:
                    self.username = username
                    return True
                return False
                
        except Exception as e:
            print(f"Login API error: {str(e)}")
            
            # Fallback to mock data
            if username in self.users and self.users[username] == password:
                self.username = username
                return True
            return False
        
    def register(self, username, password, email):
        """Register a new user"""
        try:
            response = requests.post(
                f"{self.api_base_url}/Auth/register",
                json={"username": username, "password": password, "email": email}
            )
            
            return response.status_code == 200
                
        except Exception as e:
            print(f"Register API error: {str(e)}")
            return False
    
    def get_user_transactions(self, user_id):
        """
        Get all transactions from the server for the specified user_id.
        """
        try:
            url = f"{self.api_base_url}/Transaction/user/{user_id}"
            print(f"Fetching transactions from: {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                transactions = response.json()
                # כעת 'transactions' הוא list של דיקשנריז לפי המבנה בשרת
                # לדוגמה:
                # [
                #   {
                #     "transactionId": 123,
                #     "userId": 1,
                #     "symbol": "AAPL",
                #     "transactionType": "BUY",
                #     "quantity": 5.0,
                #     "price": 150.0,
                #     "transactionDate": "2025-03-26T10:15:00"
                #   },
                #   ...
                # ]
                
                # נהפוך את שדות התאריך (transactionDate) ל־datetime, אם רוצים:
                parsed_transactions = []
                for t in transactions:
                    parsed_transactions.append({
                        "date": datetime.fromisoformat(t["transactionDate"]),
                        "stock": t["symbol"],
                        "action": "Buy" if t["transactionType"].upper() == "BUY" else "Sell",
                        "quantity": float(t["quantity"]),
                        "price": float(t["price"])
                    })
                
                return parsed_transactions
            
            else:
                print(f"Failed to get user transactions: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error fetching user transactions: {str(e)}")
            return []
