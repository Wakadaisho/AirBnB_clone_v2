#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', strict_slashes=False)
def hello_route():
    """Display text"""
    return ('Hello HBNB!')


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """Display text"""
    return ('HBNB')


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """Display text based on url path"""
    return ('C %s' % text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is cool"):
    """Display text based on url path"""
    return ('Python %s' % text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Display if path value is an integer"""
    return ('%s is a number' % n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Return html template if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Return html template if n is an integer
        Show whether it is odd or even
    """
    return render_template('6-number_odd_or_even.html',
                           n=n, parity=n % 2 and "odd" or "even")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
