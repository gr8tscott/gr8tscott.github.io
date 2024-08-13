import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz


# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Check if the API key was loaded correctly
if not alpha_vantage_api_key:
    raise ValueError("API key not found. Please check your .env file.")
else:
    print('The API key exists.\n')

# def get_stock_price(ticker):
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={alpha_vantage_api_key}'
#     response = requests.get(url)
#     data = response.json()
#     if 'Time Series (1min)' in data:
#         last_refreshed = data['Meta Data']['3. Last Refreshed']
#         stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
#         return stock_price
#     else:
#         return None
# {'v': 45668, 'vw': 216.9298, 'o': 216.84, 'c': 216.9701, 'h': 217.04, 'l': 216.7557, 't': 1723486800000, 'n': 694},

import requests
from datetime import datetime

def get_stock_price(tickers):
    # Set the local time zone to Denver
    local_tz = pytz.timezone('America/Denver')  
    date_today = datetime.now(local_tz).strftime('%Y-%m-%d')

    print('date_today: ', date_today)
    
    # Construct the URL for the API request
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{date_today}/{date_today}?adjusted=true&sort=asc&limit=50000&apiKey={alpha_vantage_api_key}'
    
    # Make the API request
    response = requests.get(url)
    print('url: ', url)
    print('response: ', response)
    
    # Parse the JSON response
    data = response.json()
    print('data: ', data)
    
    # Check if the response contains the 'results' key
    if 'results' in data and data['results']:
        # Get the last data point
        last_data_point = data['results'][-2]
        # Extract the closing price ('c')
        closing_price = last_data_point['c']
        return closing_price
    else:
        return None

# # Example usage:
# alpha_vantage_api_key = 'YOUR_API_KEY_HERE'
# ticker = 'AAPL'
# closing_price = get_stock_price(ticker, alpha_vantage_api_key)
# print(f'The closing price of {ticker} is {closing_price}')


# Replace 'AAPL' with the ticker symbol you want to test
ticker = 'AAPL'
stock_price = get_stock_price(ticker)

if stock_price:
    print(f"The current stock price for {ticker} is: ${stock_price}")
else:
    print(f"Could not fetch the current stock price for {ticker}.")
