import random
import requests
import os
import time
# RAG imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from datetime import datetime, timedelta

class MockStockModel:
    def __init__(self):
        # Base API URL
        self.api_base_url = "http://localhost:5124/api"

        self.users = {
        "maoz": "3242",
        "1": "1",
        "noam": "123"
    }
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
        # Initialize core properties
        self.rag_ready = False
        self.vectorstore = None
        self.embeddings = None

        print("📚 Initializing RAG system...")
        self._init_rag() 


    def search_symbol_by_name(self, company_name):
        """
        Search for a stock symbol by company name using the API
        Returns a tuple of (success, symbol, error_message)
        """
        try:
            print(f"Searching for symbol by company name: {company_name}")
            
            # Call the API endpoint
            response = requests.get(
            f"{self.api_base_url}/stock/queries/search",
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
            f"{self.api_base_url}/stock/queries/yahoo-history/{symbol}",
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
            response = requests.get(f"{self.api_base_url}/stock/queries/price/{symbol}")
            
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

    def get_portfolio_total_value(self, portfolio_data=None):
        """Calculate the total value of the portfolio and total unrealized P/L"""
        print("Calculating total portfolio value")
        
        # Use provided data or get it if not provided
        portfolio_items = portfolio_data if portfolio_data is not None else self.get_portfolio_data()
        
        # Sum up the market values and unrealized P/L
        total_value = sum(item["market_value"] for item in portfolio_items)
        total_unrealized_pl = sum(item["unrealized_pl"] for item in portfolio_items)
        
        print(f"Total portfolio value calculated: ${total_value:.2f}")
        print(f"Total unrealized P/L calculated: ${total_unrealized_pl:.2f}")
        
        return total_value, total_unrealized_pl
    
    def get_portfolio_data(self):
        print(f"TRACE: get_portfolio_data called from {self._get_caller_info()}")
        # Get user_id (default to 1 if not available)
        user_id = getattr(self, "user_id", 1)
        
        try:
            # Change the endpoint to use the new query controller
            url = f"{self.api_base_url}/transaction/queries/portfolio/{user_id}"
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
        
        # Process the data and calculate totals
        result = []
        total_portfolio_value = 0.0
        total_unrealized_pl = 0.0
        
        for item in portfolio_items:
            # Get values (handling different key cases)
            symbol = item.get("Symbol") or item.get("symbol")
            quantity = float(item.get("Quantity") or item.get("quantity") or 0)
            avg_buy_price = float(item.get("AverageBuyPrice") or item.get("averageBuyPrice") or 0)
            
            # Get current price
            current_price = self.get_current_price(symbol)
            
            # Calculate values for this position
            market_value = current_price * quantity
            unrealized_pl = (current_price - avg_buy_price) * quantity
            
            # Add to totals
            total_portfolio_value += market_value
            total_unrealized_pl += unrealized_pl
            
            # Add to result
            result.append({
                "symbol": symbol,
                "company_name": "",
                "quantity": quantity,
                "avg_buy_price": avg_buy_price,
                "current_price": current_price,
                "market_value": market_value,
                "unrealized_pl": unrealized_pl,
                "daily_change": None,
            })
        
        # Calculate allocation percentages
        for item in result:
            if total_portfolio_value > 0:
                item["allocation"] = (item["market_value"] / total_portfolio_value) * 100
            else:
                item["allocation"] = 0
        
        # Store totals for easy access
        self.total_portfolio_value = total_portfolio_value
        self.total_unrealized_pl = total_unrealized_pl
        
        return result

    def _get_caller_info(self):
        """Helper method to identify who is calling a method"""
        import traceback
        stack = traceback.extract_stack()
        # Get the second-to-last entry (the caller of the current method)
        caller = stack[-2]
        return f"{caller.filename}:{caller.lineno} in {caller.name}"

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
            # Change the endpoint to use the new command controller
            response = requests.post(f"{self.api_base_url}/transaction/commands/add", json=transaction_data)
            if response.status_code == 200 or response.status_code == 201:
                print("Transaction recorded in the database successfully.")
                
                # Notify any listeners that data has changed
                if hasattr(self, 'on_data_changed') and callable(self.on_data_changed):
                    self.on_data_changed()
                    
                # Update local portfolio
                if stock in self.portfolio:
                    self.portfolio[stock]["quantity"] += quantity
                    self.portfolio[stock]["price"] = price
                else:
                    self.portfolio[stock] = {"price": price, "quantity": quantity}
                    
                # Add to trade history
                self.trade_history.append({
                    "date": datetime.now(),
                    "stock": stock,
                    "action": "Buy",
                    "quantity": quantity,
                    "price": price
                })
                    
                return True
            else:
                print(f"Failed to record transaction: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error calling Transaction API: {str(e)}")
            return False

    def sell_stock(self, stock, quantity, price):
        print(f"Selling stock: {stock}, quantity: {quantity}, price: {price}")
        
        # 1. Record transaction via API
        transaction_data = {
            "UserId": getattr(self, "user_id", 1),
            "Symbol": stock,
            "TransactionType": "SELL",
            "Quantity": float(quantity),
            "Price": float(price)
        }
        
        try:
            # Change the endpoint to use the new command controller
            response = requests.post(f"{self.api_base_url}/transaction/commands/add", json=transaction_data)
            if response.status_code == 200 or response.status_code == 201:
                print("Transaction recorded in the database successfully.")
                
                # 2. Update the local portfolio (ONLY after successful API call)
                portfolio_updated = False
                
                if hasattr(self, 'on_data_changed') and callable(self.on_data_changed):
                    self.on_data_changed()

                # Check if we're using dictionary-based portfolio (with stock symbols as keys)
                if isinstance(self.portfolio, dict):
                    if stock in self.portfolio and self.portfolio[stock]["quantity"] >= quantity:
                        self.portfolio[stock]["quantity"] -= quantity
                        # Remove stock from portfolio if quantity becomes zero
                        if self.portfolio[stock]["quantity"] == 0:
                            del self.portfolio[stock]
                        portfolio_updated = True
                
                # Check if we're using list-based portfolio
                elif isinstance(self.portfolio, list):
                    for item in self.portfolio:
                        if item.get('symbol') == stock and item.get('quantity', 0) >= quantity:
                            item['quantity'] -= quantity
                            if item['quantity'] == 0:
                                self.portfolio.remove(item)
                            portfolio_updated = True
                            break
                
                # Even if local update failed, still add to trade history since API call succeeded
                self.trade_history.append({
                    "date": datetime.now(),
                    "stock": stock,
                    "action": "Sell",
                    "quantity": quantity,
                    "price": price
                })
                
                # Return success based on API call, not local portfolio update
                # This way UI shows success since database was updated
                return True
            else:
                print(f"Failed to record transaction: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error calling Transaction API: {str(e)}")
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

    def _init_rag(self):
        """Initialize the RAG components with careful error handling and timing"""
        start_time = time.time()
        
        try:
            # 1. Find the PDF file
            pdf_path = self._find_pdf_file()
            if not pdf_path:
                print("❌ Could not find the investment PDF file")
                return False
            
            print(f"📄 Found PDF at: {pdf_path}")
            
            # 2. Load the PDF content
            print("📖 Loading PDF content...")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            print(f"✅ Loaded {len(documents)} pages from PDF")
            
            # 3. Split into chunks for better retrieval
            print("✂️ Splitting document into chunks...")
            text_splitter = CharacterTextSplitter(
                chunk_size=500,  # Smaller chunks for more precise retrieval
                chunk_overlap=50, 
                separator="\n"
            )
            chunks = text_splitter.split_documents(documents)
            print(f"✅ Created {len(chunks)} text chunks")
            
            # 4. Create embeddings
            print("🔤 Initializing embeddings model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # 5. Create vector store
            print("🗄️ Creating vector store...")
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            print("✅ Vector store created successfully")
            
            self.rag_ready = True
            end_time = time.time()
            print(f"✅ RAG system initialized in {end_time - start_time:.2f} seconds")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing RAG: {e}")
            return False
    
    def _find_pdf_file(self):
        """Find the investment PDF file in various possible locations"""
        possible_paths = [
            # Common locations relative to the current file
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "gemma_value_investing_reference.pdf"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "gemma_value_investing_reference.pdf"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gemma_value_investing_reference.pdf"),
            # Add more possible locations if needed
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    def _get_relevant_context(self, query, max_chunks=5):
        """Get the most relevant context from the vector store"""
        if not self.rag_ready or not self.vectorstore:
            print("⚠️ RAG system not initialized, skipping context retrieval")
            return ""
        
        try:
            print(f"🔍 Finding relevant context for query: {query}")
            start_time = time.time()
            
            # Get documents from vector store
            relevant_docs = self.vectorstore.similarity_search(
                query, 
                k=max_chunks  # Limit to top relevant chunks
            )
            
            # Extract and join the content
            context = "\n".join([doc.page_content for doc in relevant_docs])
            
            end_time = time.time()
            print(f"✅ Retrieved {len(relevant_docs)} relevant chunks in {end_time - start_time:.2f} seconds")
            
            # Print a preview of the retrieved context
            preview = context[:100] + "..." if len(context) > 100 else context
            print(f"📑 Context preview: {preview}")
            
            return context
            
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return ""
    
    def get_ai_advice(self, query, context=None):
        """
        Get AI investment advice using RAG with PDF knowledge
        
        Args:
            query (str): The user's investment question
            context (dict, optional): Additional context like portfolio data
            
        Returns:
            str: Investment advice from the AI model
        """
        # Track execution time
        start_time = time.time()
        
        # Check for empty query
        if not query or query.strip() == "":
            print("⚠️ Empty query received")
            return "Please ask a specific investment question to get advice."
        
        print(f"❓ Processing query: '{query}'")
        
        try:
            # 1. Get relevant context from our knowledge base
            knowledge_context = self._get_relevant_context(query)
            
            # 2. Add user context if available
            user_context = ""
            if context:
                user_context = "User context: " + ". ".join([f"{key}: {value}" for key, value in context.items()])
                print(f"👤 Added user context: {user_context}")
            
            # 3. Prepare the prompt with context and clear instructions
            prompt = f"""Question: {query}

Knowledge context: {knowledge_context}

{user_context}

Based on the provided knowledge context, explain the main reasons why {query.lower()} Answer in 2-3 complete sentences without repetition."""
            
            # 4. Call Ollama API with timeout limit
            print("🤖 Calling Ollama API...")
            api_url = "http://localhost:11434/api/chat"
            
            payload = {
    "model": "gemma:2b",
    "messages": [
        {
            "role": "system",
            "content": "You are an investment advisor who provides concise, factual answers. Avoid repetition and focus on the most important points from the provided context."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "stream": False,
    "options": {
        "temperature": 0.2,    # Slightly higher to reduce repetition loops
        "max_tokens": 150,     # More limited to prevent runaway repetition 
        "top_p": 0.85,         # Slightly lower for more focused responses
        "frequency_penalty": 1.0  # Add this to discourage repetition
    }
}
            
            # Set a reasonable timeout to prevent UI freezing (adjust as needed)
            response = requests.post(api_url, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                if "message" in result and "content" in result["message"]:
                    answer = result["message"]["content"]
                    # Calculate and log the response time
                    end_time = time.time()
                    print(f"✅ Got response in {end_time - start_time:.2f} seconds")
                    print(f"📝 Response length: {len(answer)} characters")
                    return answer
                else:
                    print("⚠️ No content in Ollama response:", result)
            else:
                print(f"❌ Ollama API error: {response.status_code} - {response.text}")
            
            # If we get here, the Ollama API failed
            raise Exception(f"Failed to get response from Ollama API: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⚠️ Ollama API timeout - response took too long")
            return "I apologize, but the response is taking longer than expected. Please try a more specific question or try again later."
            
        except Exception as e:
            print(f"❌ Error getting AI advice: {e}")
            
            # Fallback to random advice messages
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
            f"{self.api_base_url}/auth/queries/login",  # Updated endpoint
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
                f"{self.api_base_url}/auth/commands/register",
                json={"username": username, "password": password, "email": email}
            )
            
            # If registration is successful, store user data including profile picture
            if response.status_code == 200:
                try:
                    user_data = response.json()
                    # Store profile picture URL if available in the response
                    if "profilePictureUrl" in user_data:
                        self.profile_picture_url = user_data["profilePictureUrl"]
                    # Store user ID if available
                    if "userId" in user_data:
                        self.user_id = user_data["userId"]
                except:
                    # If response doesn't contain JSON data, that's okay - just continue
                    pass
                    
                return True
            else:
                return False
            
        except Exception as e:
            print(f"Register API error: {str(e)}")
            return False
    
    def get_user_transactions(self, user_id):
        """
        Get all transactions from the server for the specified user_id.
        """
        try:
            # Change the endpoint to use the new query controller
            url = f"{self.api_base_url}/transaction/queries/user/{user_id}"
            print(f"Fetching transactions from: {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                transactions = response.json()
                
                # Parse the transactions
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
    
    def get_company_description(self, symbol):
        """Get company description for a stock symbol"""
        try:
            response = requests.get(f"{self.api_base_url}/stock/queries/description/{symbol}")
            if response.status_code == 200:
                description = response.text.strip('"')  # Remove quotes if the API returns JSON string
                print(f"Got description for {symbol}: {description[:50]}...")
                return description
            else:
                print(f"API error for {symbol} description: {response.status_code} - {response.text}")
                return "No company description available."
        except Exception as e:
            print(f"Error getting company description for {symbol}: {str(e)}")
            return "No company description available."

    def get_company_profile(self, symbol):
        """Get company profile information for a stock symbol"""
        try:
            response = requests.get(f"{self.api_base_url}/stock/queries/profile/{symbol}")
            if response.status_code == 200:
                profile = response.json()
                print("json is:", profile)
                print(f"Got profile for {symbol}: {profile.get('name', 'N/A')}")
                return profile
            else:
                print(f"API error for {symbol} profile: {response.status_code} - {response.text}")
                return {
                    "name": symbol,
                    "industry": "Unknown",
                    "logoUrl": "",
                    "exchange": "Unknown",
                    "webUrl": "",
                    "country": "Unknown"
                }
        except Exception as e:
            print(f"Error getting company profile for {symbol}: {str(e)}")
            return {
                "name": symbol,
                "industry": "Unknown",
                "logoUrl": "",
                "exchange": "Unknown",
                "webUrl": "",
                "country": "Unknown"
            }

    def get_profile_picture_url(self, user_id=None):
        try:
            print(f"API base URL: {self.api_base_url}")
            # If no user_id is specified, use the current logged-in user
            if user_id is None and hasattr(self, 'user_id'):
                user_id = self.user_id
                print(f"Using current user ID: {user_id}")
            elif user_id is None:
                print("No user ID available")
                return ""
                
            # Check if we already have the profile picture URL stored
            if hasattr(self, 'profile_picture_url') and self.profile_picture_url:
                print(f"Using cached profile picture URL: {self.profile_picture_url}")
                return self.profile_picture_url
                
            # Otherwise, fetch it from the API
            api_url = f"{self.api_base_url}/auth/queries/user/{user_id}"
            print(f"Fetching user data from: {api_url}")
            
            headers = self.get_auth_headers()
            print(f"Using headers: {headers}")
            
            response = requests.get(api_url, headers=headers)
            
            print(f"API response status: {response.status_code}")
            if response.status_code == 200:
                user_data = response.json()
                print(f"User data received: {user_data}")
                
                if "profilePictureUrl" in user_data and user_data["profilePictureUrl"]:
                    self.profile_picture_url = user_data["profilePictureUrl"]
                    print(f"Found profile picture URL: {self.profile_picture_url}")
                    return self.profile_picture_url
                else:
                    print("No profile picture URL in user data")
            else:
                print(f"Failed to get user data. Response: {response.text}")
                    
            return ""
            
        except Exception as e:
            print(f"Error getting profile picture URL: {str(e)}")
            return ""
            
    def get_auth_headers(self):
        """Get headers for authenticated API requests"""
        headers = {"Content-Type": "application/json"}
        if hasattr(self, 'token') and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    
if __name__ == "__main__":
    model = MockStockModel()
    # Wait a moment for initialization to complete
    time.sleep(2)
    
    # Test with a sample query
    test_query = "Why is chasing hot growth stocks or new IPOs so risky?"
    #How often should defensive investors rebalance?
    #When is a bear market good?
    #What stock P/E limit?
    print("\n" + "-"*50)
    print(f"TEST QUERY: {test_query}")
    print("-"*50)
    response = model.get_ai_advice(test_query)
    print("-"*50)
    print(f"RESPONSE: {response}")
    print("-"*50)