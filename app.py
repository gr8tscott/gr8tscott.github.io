# This is the main Flask router for the Cut n Pasta Application.

from flask import Flask, url_for
from flask import send_file
from flask import render_template, request, jsonify
import os
from Prefix import prefix
# from Frontend import adding_data
# import psycopg2
import subprocess

from flask import Flask, url_for

# create app to use in this Flask application
app = Flask(__name__)

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
            <li>{}</li>
        </ul>
        '''.format(url_for('index'),url_for('hello'),url_for('projects'),url_for('about'))
    # return lst
    return render_template('index.html')

# Adapted from this stack overflow: https://stackoverflow.com/questions/52183357/flask-user-input-to-run-a-python-script
@app.route('/generate', methods=['GET'])
def generate():
    prefix = request.args.get('prefix')
    print(f"User input received: {prefix}")
    urls = []
    for number in range(1, 7):
        urls.append('https://example.com/{p}-{n}.jpg'.format(p=prefix, n=number))
    print("hello")
    # return jsonify(result=urls)
    return jsonify(result = prefix)

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

@app.route('/projects/')
def projects():
    """
    Route to display the projects page.

    Returns:
        str: HTML content for the projects page.
    """
    lst = ''' 
        <h1>Optional Routes</h1>
        <ul>
            <li>{}</li>
            - Cart is a static ascii text page where the text is read from a known filename in templates directory.
            <br></br>
            <li>{}</li>
            - Resorts is a table of ski resorts and is a static HTML page where the HTML reads from file specified in a route parameterwhich is in the static directory.
            <br></br>
            <li>{}</li>
            - Movies displays the title of a film and it's director's name by way of dynamic text where it displays from data received in the URL.
        </ul>
        '''.format(url_for('cart'),url_for('resorts'),'/movie?title=Avatar&director=James%20Cameron')
    return lst

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

