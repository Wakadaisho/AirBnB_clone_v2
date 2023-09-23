#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask
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
    """Display url text"""
    return ('C %s' % text.replace("_", " "))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
