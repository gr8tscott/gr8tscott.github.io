import os
import psycopg2
from datetime import datetime
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Retrieve the Alpha Vantage API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_stock_price(ticker):
    # Set the date to today
    date_today = datetime.now().strftime('%Y-%m-%d')
    
    # Construct the URL for the API request
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{date_today}/{date_today}?adjusted=true&sort=asc&limit=50000&apiKey={alpha_vantage_api_key}'
   
    response = requests.get(url)
    data = response.json()
    
    # Check if the response contains the 'results' key
    if 'results' in data and data['results']:
        # Get the last data point
        last_data_point = data['results'][-2]
        # Extract the closing price ('c')
        closing_price = last_data_point['c']
        return closing_price
    else:
        return None


# Retrieve the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database
conn = psycopg2.connect(DATABASE_URL)
# conn = psycopg2.connect("postgresql://stockdata_t8jf_user:deZtjcbOA8mBLFXpioy1xDsaoVPb3I1B@dpg-cqt5q75svqrc73d0okm0-a.oregon-postgres.render.com:5432/stockdata_t8jf")
cur = conn.cursor()

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

 # Fetch current stock prices
aapl_price = get_stock_price('AAPL')
googl_price = get_stock_price('GOOGL')
msft_price = get_stock_price('MSFT')
lumn_price = get_stock_price('LUMN')
    
# Insert sample data
sample_data = [
        ('AAPL', aapl_price, 218.54, 'Buy', '2024-07-24'),
        ('GOOGL', googl_price, 172.63, 'Hold', '2024-07-24'),
        ('MSFT', msft_price, 428.90, 'Sell', '2024-07-24'),
        ('LUMN', lumn_price, 1.52, 'Buy', '2024-07-24')
]
# sample_data = [
#     ('AAPL', 150.00, 155.00, 'Buy', date(2024, 7, 24)),
#     ('GOOGL', 151.72, 172.63, 'Hold', date(2024, 7, 24)),
#     ('MSFT', 299.00, 310.00, 'Sell', date(2024, 7, 24))
# ]

for record in sample_data:
    cur.execute('''
        INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date)
        VALUES (%s, %s, %s, %s, %s);
    ''', record)

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Database reset and sample data inserted successfully.")

