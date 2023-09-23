#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Return html template of states and their cities"""
    states = [(i.id, i.name, [(c.id, c.name) for c in i.cities])
              for i in storage.all(State).values()]
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def end_request(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
