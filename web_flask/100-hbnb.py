#!/usr/bin/python3
"""
Flask web app running on 0.0.0.0:5000
"""

from flask import Flask, render_template
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.user import User

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return html template of states"""
    states = [(i.id, i.name, [(c.id, c.name) for c in i.cities])
              for i in storage.all(State).values()]
    amenities = [(i.id, i.name)
                 for i in storage.all(Amenity).values()]
    places = [i for i in storage.all(Place).values()]
    owners = {j.id: f"{i.first_name} {i.last_name}"
              for i in storage.all(User).values()
              for j in places if j.user_id == i.id}
    return render_template('100-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           owners=owners)


@app.teardown_appcontext
def end_request(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
