#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Return html template of states"""
    states = [(i.id, i.name, [(c.id, c.name) for c in i.cities])
              for i in storage.all(State).values()]
    amenities = [(i.id, i.name)
                 for i in storage.all(Amenity).values()]

    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def end_request(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
