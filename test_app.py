from flask import Flask, request, jsonify, render_template, url_for
import subprocess
import os
import time
import requests
from dotenv import load_dotenv
from Prefix import prefix


app = Flask(__name__)

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine:
prefix.use_PrefixMiddleware(app) 

# Load environment variables from .env file
load_dotenv()

# Retrieve the Alpha Vantage API key from the environment variables
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f"Alpha Vantage API Key: {alpha_vantage_api_key}")

@app.route('/')
def index():
    """
    Route to display the index page.

    Returns:
        str: HTML content for the index page.
    """
    
    return render_template('index.html')

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

    truncated_content = content[:500]
    
    print(f"Truncated Content: {truncated_content}")

    ai_response = "AAPL: buy"
    
    ticker, sentiment = ai_response.split(": ")
    stock_price = get_stock_price(ticker)

    if stock_price:
        ai_response = f"{ai_response}\nCurrent stock price for {ticker}: ${stock_price}"
    else:
        ai_response = f"{ai_response}\nCould not fetch the current stock price for {ticker}."

    print(f"AI Response: {ai_response}")

    return jsonify(
        user_input=url, 
        article_title=article_title, 
        article_content=truncated_content, 
        ai_response=ai_response
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
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&apikey={alpha_vantage_api_key}'
    print(f"Fetching stock price from: {url}")
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
        return stock_price
    else:
        return None

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server using port 3308 instead of port 5000.
    # with app.test_request_context():
    #     print(url_for('index'))
    #     print(url_for('about'))
    #     print(url_for('login'))
    #     print(url_for('login', next='/'))
    #     print(url_for('profile', username='masc6977'))
    app.run(host='0.0.0.0', port=3308)