#!/usr/bin/python3
""" this module start a web app with flask """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """ a web page with a list of cities by state """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """ a web page with a list of cities by state """
    states = storage.all(State)
    asked_state = {}
    obj_id = 0
    for key, val in states.items():
        obj_id = key.split('.')
        if obj_id[1] == id:
            asked_state = {key: val}

    return render_template('9-states.html', states=asked_state, id=id)


@app.teardown_appcontext
def tear_down(e):
    """ close the actual session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
