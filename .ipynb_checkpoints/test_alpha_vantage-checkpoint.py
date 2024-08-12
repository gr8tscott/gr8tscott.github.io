import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Check if the API key was loaded correctly
if not alpha_vantage_api_key:
    raise ValueError("API key not found. Please check your .env file.")
else:
    print('The API key exists.\n')

def get_stock_price(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={alpha_vantage_api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
        return stock_price
    else:
        return None

# Replace 'AAPL' with the ticker symbol you want to test
ticker = 'AAPL'
stock_price = get_stock_price(ticker)

if stock_price:
    print(f"The current stock price for {ticker} is: ${stock_price}")
else:
    print(f"Could not fetch the current stock price for {ticker}.")
