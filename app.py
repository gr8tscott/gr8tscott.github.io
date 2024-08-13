# This is the main Flask router for the Stock Sentiment APP Application.
from flask import Flask, url_for
from flask import send_file
from flask import render_template, request, jsonify
import os
# from Prefix import prefix
import psycopg2
import subprocess
import urllib.parse
from openai import OpenAI
from dotenv import load_dotenv
import time
import requests
import sqlite3
from datetime import datetime
import pytz


# Create app to use in this Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from the environment variables
client = OpenAI()
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Retrieve the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Set the local time zone to Denver
local_tz = pytz.timezone('America/Denver') 
# Get todays date for stock calculations and adding to database:
date_today = datetime.now(local_tz).strftime('%Y-%m-%d')

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine:
# prefix.use_PrefixMiddleware(app)   

#. venv/bin/activate
# export FLASK_DEBUG=true
# flask --app app.py run


###############################################################################

def get_stock_predictions():
    # conn = sqlite3.connect('stock_data.db')
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT ticker, current_price, traded_price, ai_response, date FROM stock_predictions")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    stock_predictions = get_stock_predictions()
    return render_template('index.html', stock_predictions=stock_predictions)


# Adapted from this stack overflow: https://stackoverflow.com/questions/52183357/flask-user-input-to-run-a-python-script
@app.route('/generate', methods=['GET'])
def generate():
    url = request.args.get('prefix')
    if not url:
        return jsonify(error="No URL provided"), 400
    
    print(f"User URL: {url}")
    
    try:
        title_file_path, text_file_path = run_extraction_script(url)
    except Exception as e:
        return jsonify(error=f"Failed to run extraction script: {str(e)}"), 500

    print(f"Title file path: {title_file_path}")
    print(f"Text file path: {text_file_path}")

    try:
        with open(text_file_path, 'r') as file:
            content = file.read()
    except Exception as e:
        return jsonify(error=f"Failed to read text file: {str(e)}"), 500

    try:
        with open(title_file_path, 'r') as file:
            article_title = file.read().strip()
    except Exception as e:
        return jsonify(error=f"Failed to read title file: {str(e)}"), 500

        
    # Truncate the content to the first 500 characters
    truncated_content = content[:500]
    
    # Call the OpenAI API with the extracted content
    # Process the response and insert into database
    try:
        # conn = sqlite3.connect('stock_data.db')
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You analyze news articles and give a sentiment: 'Buy', 'Sell', or 'Hold' based on the content. Output only the company ticker symbol and colon followed by your sentiment grade. Do not summarize."},
                {"role": "user", "content": truncated_content}
            ]
        )
        ai_response = response.choices[0].message.content
        print(ai_response)
    # # try:
    # ai_response= "AAPL: buy"
        
        ticker, sentiment = ai_response.split(": ")
        stock_price = get_stock_price(ticker) #BRING THIS BACK WHEN MORE API CALLS ALLOWED

        # Get the current date and format it as 'YYYY-MM-DD'
        # date_today = datetime.now().strftime('%Y-%m-%d')
        print("Stock Price: ", stock_price)
        if stock_price:
            ai_response = f"{ai_response}"
            current_price = f"Current stock price for {ticker}: $"'{:.2f}'.format(row[2])
            cur.execute('''
                INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date)
                VALUES (%s, %s, %s, %s, %s);
            ''', (ticker, stock_price, stock_price, sentiment, date_today))
            conn.commit()
        else:
            ai_response = f"{ai_response}\nCould not fetch the current stock price for {ticker}."
    # except Exception as e:
    #     ai_response = str(e)
    except sqlite3.Error as e:
        return jsonify(error=f"Database error: {str(e)}"), 500

    finally:
        cur.close()
        conn.close()

    print(f"AI Response: {ai_response}")
    
    return jsonify(
        user_input=url, 
        article_title=article_title, 
        article_content=truncated_content, 
        ai_response=ai_response,
        current_price=current_price,
        refresh_table=True # Refresh the table after stock is added to db
    )


def run_extraction_script(url):
    script_path = "extract_scripts/scraper.sh"
    print(f"Running extraction script: {script_path} with URL: {url}")
    result = subprocess.run([script_path, url], capture_output=True, text=True)
    print(f"Script output: {result.stdout}")
    output = result.stdout.strip().split('\n')

    if len(output) < 3:
        raise RuntimeError("Extraction script did not provide sufficient output.")

    title_file_path = output[-1]
    text_file_path = output[-2]

    # Ensure the paths are correct and wait for the files to be created if necessary
    while not os.path.exists(text_file_path) or not os.path.exists(title_file_path):
        print(f"Waiting for files: {text_file_path}, {title_file_path}")
        time.sleep(1)
    
    return title_file_path, text_file_path

def get_stock_price(ticker):
    # Construct the URL for the API request
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/{date_today}/{date_today}?adjusted=true&sort=asc&limit=50000&apiKey={alpha_vantage_api_key}'
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={alpha_vantage_api_key}'
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
    
@app.route('/stock_data', methods=['GET'])
def stock_data():
    # conn = sqlite3.connect('stock_data.db')
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute('''
        SELECT ticker, current_price, traded_price, ai_response, date
        FROM stock_predictions
    ''')
    rows = cur.fetchall()
    
    # Process the rows into a list of dictionaries
    stock_data = []
    for row in rows:
        stock_data.append({
            'ticker': row[0],
            'current_price': "$"'{:.2f}'.format(get_stock_price(row[0])),
            'traded_price': "$"'{:.2f}'.format(row[2]),
            'ai_response': row[3],
            'date': row[4],
            'correct_prediction': get_correct_prediction(row)
        })
    
    cur.close()
    conn.close()
    
    return jsonify(stock_data)

def get_correct_prediction(row):
    ticker, current_price, traded_price, ai_response, date = row
    if ai_response == 'Buy' and current_price > traded_price:
        return True
    if ai_response == 'Hold' and current_price >= traded_price:
        return True
    if ai_response == 'Sell' and current_price < traded_price:
        return True
    return False



@app.route('/about')
def about():
    """
    Route to display the about page.

    Returns:
        str: HTML content for the about page.
    """
    lst = ''' 
        <ul>
            <li>Github: gr8tscott</li>
        </ul>
        '''
    return lst



###############################################################################
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server using port 3308 instead of port 5000.
    with app.test_request_context():
        # print(url_for('index'))
        # print(url_for('about'))
        # print(url_for('login'))
        # print(url_for('login', next='/'))
        print(url_for('profile', username='masc6977'))
    app.run(host='0.0.0.0', port=3308)

