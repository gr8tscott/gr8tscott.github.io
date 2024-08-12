# This is the main Flask router for the Cut n Pasta Application.

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
@app.route('/')
def index():
    """
    Route to display the index page.

    Returns:
        str: HTML content for the index page.
    """
    lst = ''' 
        <h1>Required Routes</h1>
        <ul>
            <li>{}</li>
            <li>{}</li>
            <li>{}</li>
        </ul>
        '''.format(url_for('index'),url_for('hello'),url_for('about'))
    # return lst
    return render_template('index.html')

# Adapted from this stack overflow: https://stackoverflow.com/questions/52183357/flask-user-input-to-run-a-python-script
# @app.route('/generate', methods=['GET'])
# def generate():
#     prefix = request.args.get('prefix')
#     print(f"User input received: {prefix}")
#     urls = []
#     for number in range(1, 7):
#         urls.append('https://example.com/{p}-{n}.jpg'.format(p=prefix, n=number))
#     print("hello")
#     print(urls)
#     # return jsonify(result=urls)
#     return jsonify(result = prefix)
# @app.route('/generate', methods=['GET'])
# def generate():
#     url = request.args.get('prefix')
#     print(f"User input received: {url}")

#     # Ensure the URL is properly encoded
#     encoded_url = urllib.parse.quote(url, safe=':/')

#     script_path = os.path.join('extract_scripts', 'scraper.sh')

#     try:
#         # Run the script
#         result = subprocess.run([script_path, encoded_url], check=True, capture_output=True, text=True)
#         output = result.stdout.strip().splitlines()[-1]  # Get the last line of the output
#         error = result.stderr.strip()

#         print(f"Script output: {output}")
#         print(f"Script error: {error}")

#         # Check if the script output is a valid file path and the file exists
#         if os.path.isfile(output):
#             print(f"File found: {output}")
#             with open(output, 'r') as file:
#                 file_content = file.read()
#             return jsonify(result=file_content)
#         else:
#             print(f"File not found: {output}")
#             return jsonify(result=f"Text file not found at the expected path: {output}"), 500
#     except subprocess.CalledProcessError as e:
#         print(f"Script execution failed: {e}")
#         print(f"Script stderr: {e.stderr}")
#         return jsonify(result=f"Script execution failed with error: {e.stderr}"), 500
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return jsonify(result=f"Unexpected error: {e}"), 500
@app.route('/generate', methods=['GET'])
def generate():
    url = request.args.get('prefix')
    # Run your extraction script here and get the path to the text file
    text_file_path = run_extraction_script(url)

    # Read the content of the text file
    with open(text_file_path, 'r') as file:
        content = file.read()
        
    # Read the title of the article
    with open(title_file_path, 'r') as file:
        article_title = file.read().strip()
    # return jsonify(result=article_title)
        
    # Truncate the content to the first 500 characters
    truncated_content = content[:250]
    
    # Call the OpenAI API with the extracted content
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-4o-mini",
    #         messages=[
    #             {"role": "system", "content": "You analyze news articles and give a sentiment: 'buy', 'sell', or 'hold' based on the content. Output only the company ticker symbol and colon followed by your sentiment grade. Do not summarize."},
    #             {"role": "user", "content": truncated_content}
    #         ]
    #     )
    #     ai_response = response.choices[0].message.content
    # try:
    ai_response= "AAPL: buy"
        
        # Example response: "AAPL: buy"
    ticker, sentiment = ai_response.split(": ")
    stock_price = get_stock_price(ticker)

    if stock_price:
        ai_response = f"{ai_response}\nCurrent stock price for {ticker}: ${stock_price}"
    else:
        ai_response = f"{ai_response}\nCould not fetch the current stock price for {ticker}."
    # except Exception as e:
    #     ai_response = str(e)
    print(url)
    print(article_title)
    print(truncated_content)
    print(ai_response)

    return jsonify(user_input=url, article_title=article_title, article_content=truncated_content, ai_response=ai_response)

            
#     except Exception as e:
#         ai_response = str(e)
    
#     return jsonify(result=result)

def run_extraction_script(url):
    script_path = "extract_scripts/scraper.sh"
    result = subprocess.run([script_path, url], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')

    # Assuming the last two lines of the script output are the title file path and the text file path
    title_file_path = output[-2]
    text_file_path = output[-1]

    # Ensure the paths are correct and wait for the files to be created if necessary
    while not os.path.exists(text_file_path) or not os.path.exists(title_file_path):
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

