# This is the main Flask router for the Stock Sentiment APP Application.
from flask import Flask, url_for
from flask import send_file
from flask import render_template, request, jsonify
import os
from Prefix import prefix
# from Frontend import adding_data
# import psycopg2
import subprocess
import urllib.parse
from openai import OpenAI
from dotenv import load_dotenv
import time
import requests
import sqlite3
from datetime import datetime



# create app to use in this Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from the environment variables
client = OpenAI()
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")


# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine:
prefix.use_PrefixMiddleware(app)   

#. venv/bin/activate
# export FLASK_DEBUG=true
# flask --app app.py run

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine
# prefix.use_PrefixMiddleware(app)   

# test route to show prefix settings
# @app.route('/prefix_url')  
# def prefix_url():
#     return 'The URL for this page is {}'.format(url_for('prefix_url'))


###############################################################################
## Required Routes from Flask Tutorial for Lab include:
##     1. static text page, "index"   @app.route('/')
##     2. static text page, "hello"   @app.route('/hello')
##     3. static text page, "project" @app.route('/projects/')
##     4. static text page, "about"   @app.route('/about')
##     5. dynamic text, route parameter, string  @app.route('/user/<username>')
##     6. dynamic text, route parameter, int     @app.route('/post/<int:post_id>')
##     7. dynamic text, route parameter, subpath @app.route('/path/<path:subpath>')
##
## Place your required routes here
##
def get_stock_predictions():
    conn = sqlite3.connect('stock_data.db')
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
    truncated_content = content[:300]
    
    # Call the OpenAI API with the extracted content
    # Process the response and insert into database
    try:
        conn = sqlite3.connect('stock_data.db')
        cur = conn.cursor()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You analyze news articles and give a sentiment: 'Buy', 'Sell', or 'Hold' based on the content. Output only the company ticker symbol and colon followed by your sentiment grade. Do not summarize."},
                {"role": "user", "content": truncated_content}
            ]
        )
        ai_response = response.choices[0].message.content
    # # try:
    # ai_response= "AAPL: buy"
    
        ticker, sentiment = ai_response.split(": ")
        # stock_price = get_stock_price(ticker) #BRING THIS BACK WHEN MORE API CALLS ALLOWED
        stock_price = 3.50
        # Get the current date and format it as 'YYYY-MM-DD'
        date_today = datetime.now().strftime('%Y-%m-%d')
        print("Stock Price: ", stock_price)
        if stock_price:
            ai_response = f"{ai_response} <br>Current stock price for {ticker}: ${stock_price}<br>"
            cur.execute('''
                INSERT INTO stock_predictions (ticker, current_price, traded_price, ai_response, date)
                VALUES (?, ?, ?, ?, ?);
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
    response = requests.get(url)
    data = response.json()
    if 'Time Series (1min)' in data:
        last_refreshed = data['Meta Data']['3. Last Refreshed']
        stock_price = data['Time Series (1min)'][last_refreshed]['4. close']
        return stock_price
    else:
        return None
    
@app.route('/stock_data', methods=['GET'])
def stock_data():
    conn = sqlite3.connect('stock_data.db')
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
            'current_price': f'${get_stock_price(row[0])}',
            'traded_price': f'${row[2]}',
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

    
@app.route('/hello')
def hello():
    """
    Route to display the hello page.

    Returns:
        str: HTML content for the hello page.
    """
    welcome = '''
        <h1>Hello new vistor!</h1>
        This is the welcome page for Lab 6 of CSPB 3308!
        '''
    return welcome

@app.route('/about')
def about():
    """
    Route to display the about page.

    Returns:
        str: HTML content for the about page.
    """
    lst = ''' 
        <ul>
            <li>Team 4</li>
            <li>CUid: masc6977</li>
            <li>Github: gr8tscott</li>
        </ul>
        '''
    return lst

from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    """
    Route to display the user profile page.

    Args:
        username (str): The username.

    Returns:
        str: HTML content for the user profile page.
    """
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    """
    Route to display a specific post.

    Args:
        post_id (int): The ID of the post.

    Returns:
        str: HTML content for the post.
    """
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    """
    Route to display the subpath.

    Args:
        subpath (str): The subpath.

    Returns:
        str: HTML content for the subpath.
    """
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
#########
# @app.route('/login')
# def login():
#     return 'login'

@app.route('/user/<username>')
def profile(username):
    """
    Route to display the user's profile.

    Args:
        username (str): The username.

    Returns:
        str: HTML content for the user's profile.
    """
    return f'{username}\'s profile'

from flask import request
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route to handle user login.

    Returns:
        str: HTML content for the login form or login action.
    """
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
    
# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('about'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='masc6977'))
    




    
# url_for('static', filename='style.css')

from flask import render_template

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)
###############################################################################
## Place your optional routes here
#A2: opens a file, then reads and returns the data from the file
# @app.route('/cart')
#     """
#     Route to display the content of the cart.

#     Returns:
#         str: Contents of the cart.
#     """
# def cart():
#     return render_template('cart.txt')

from flask import send_file

#B1: displays a static HTML page, reads data and ruturns the contents of the file
@app.route('/resorts')
def resorts():
    """
    Route to display the resorts page.

    Returns:
        file: The HTML content of the resorts page.
    """
    # filename = url_for('static', filename='resorts.html')
    filename = 'static/resorts.html'
    return send_file(filename)

#C4: this dynamic html route takes the key value pairs in the URL and passes them as arguments to the html page and displays the strings on the page.
@app.route('/movie')
def movie():
    """
    Route to display movie information.

    Returns:
        str: HTML content for the movie page.
    """
    # Extract the query parameters from the URL
    title = request.args.get('title')
    director = request.args.get('director')

    # html_content = f"<p>Title: {title}</p><p>Director: {director}</p>"

    return render_template('movie.html', title=title, director=director)
###############################################################################
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server using port 3308 instead of port 5000.
    with app.test_request_context():
        print(url_for('index'))
        print(url_for('about'))
        print(url_for('login'))
        print(url_for('login', next='/'))
        print(url_for('profile', username='masc6977'))
    app.run(host='0.0.0.0', port=3308)

