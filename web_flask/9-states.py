#!/usr/bin/python3
""" this module start a web app with flask """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


# @app.route('/states', strict_slashes=False)
# def states_list():
#     """ a web page with a list of cities by state """
#     states = storage.all(State)
#     return render_template('8-cities_by_states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """ a web page with a list of cities by state """
    states = storage.all(State)
    state = {}
    for key, val in states.items():
        the_id = key.split('.')
        if the_id[1] == id:
            state.update(key, **val)

    return render_template('8-cities_by_states.html', states=state, id=id)


@app.teardown_appcontext
def tear_down(e):
    """ close the actual session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
