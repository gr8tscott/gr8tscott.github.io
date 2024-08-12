from datetime import date
import os
import psycopg2
from dotenv import load_dotenv
import requests
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Retrieve the Alpha Vantage API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f"Alpha Vantage API Key: {alpha_vantage_api_key}")

def get_stock_price(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={alpha_vantage_api_key}'
    print(f"Fetching stock price from: {url}")
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
        return float(stock_price)
    else:
        print(f"Failed to fetch stock price for {ticker}")
        return None

# Connect to the PostgreSQL database
# conn = psycopg2.connect(
#     dbname="stock_data",
#     user="your_username",
#     password="your_password",
#     host="localhost"
# )
conn = sqlite3.connect('stock_data.db')
cur = conn.cursor()

try:
    # Fetch current stock prices
    aapl_price = get_stock_price('AAPL')
    googl_price = get_stock_price('GOOGL')
    msft_price = get_stock_price('MSFT')
    
    # Insert sample data
    data = [
        ('AAPL', aapl_price, 152.28, 'Buy', '2024-07-24'),
        ('GOOGL', googl_price, 150.21, 'Hold', '2024-07-24'),
        ('MSFT', msft_price, 299.09, 'Sell', '2024-07-24')
    ]
    
    for record in data:
        if record[2] is not None:  # Ensure traded_price is valid
            cur.execute('''
                INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date)
                VALUES (?, ?, ?, ?, ?);
            ''', record)
    
    # Commit the changes
    conn.commit()
    print("Data inserted successfully.")
    
except psycopg2.Error as e:
    print(f"The error '{e}' occurred")

finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
