#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Return html template of states"""
    states = [(i.id, i.name) for i in storage.all(State).values()]
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def end_request(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
