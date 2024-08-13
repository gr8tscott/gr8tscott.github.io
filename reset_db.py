import os
import psycopg2
from datetime import datetime
import requests
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# Set the local time zone to Denver
local_tz = pytz.timezone('America/Denver')  

# Retrieve the Alpha Vantage API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_stock_price(ticker):
    date_today = datetime.now(local_tz).strftime('%Y-%m-%d')
    print(f"Date: {date_today}")

    # Construct the URL for the API request
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{date_today}/{date_today}?adjusted=true&sort=asc&limit=50000&apiKey={alpha_vantage_api_key}'
    print(f"Request URL: {url}")

    response = requests.get(url)
    data = response.json()

    # Check if the response contains the 'results' key
    if 'results' in data and data['results']:
        # Get the last data point
        last_data_point = data['results'][-2]
        # Extract the closing price ('c')
        closing_price = last_data_point['c']
        print(f"Closing price for {ticker}: {closing_price}")
        return closing_price
    else:
        print(f"No results found for {ticker}")
        return None

# Retrieve the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DBURL: {DATABASE_URL}")

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    print("Connected to the database.")

    # Drop and create the stock_predictions table
    cur.execute('DROP TABLE IF EXISTS stock_predictions')
    cur.execute('''
        CREATE TABLE stock_predictions (
            id SERIAL PRIMARY KEY,
            ticker TEXT NOT NULL,
            current_price REAL NOT NULL,
            traded_price REAL NOT NULL,
            ai_response TEXT NOT NULL,
            date TEXT NOT NULL
        );
    ''')
    print("Table dropped and created.")

    # Fetch current stock prices
    aapl_price = get_stock_price('AAPL')
    googl_price = get_stock_price('GOOGL')
    msft_price = get_stock_price('MSFT')
    lumn_price = get_stock_price('LUMN')

    # Check if any price is None, if so, skip insertion
    if None in [aapl_price, googl_price, msft_price, lumn_price]:
        print("One or more stock prices could not be retrieved.")
    else:
        # Insert sample data
        sample_data = [
            ('AAPL', aapl_price, 218.54, 'Buy', '2024-07-24'),
            ('GOOGL', googl_price, 172.63, 'Hold', '2024-07-24'),
            ('MSFT', msft_price, 428.90, 'Sell', '2024-07-24'),
            ('LUMN', lumn_price, 1.52, 'Buy', '2024-07-24')
        ]
        print("Stock prices and sample data retrieved.")

        for record in sample_data:
            cur.execute('''
                INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date)
                VALUES (%s, %s, %s, %s, %s);
            ''', record)
        print("Data inserted into the database.")

    # Commit changes and close the connection
    conn.commit()
    print("Changes committed to the database.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cur.close()
    conn.close()
    print("Database connection closed.")

print("Database reset and sample data inserted successfully.")
