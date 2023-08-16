#!/usr/bin/python3
""" this module start a web app with flask """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ a web page with a list of state objects """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def tear_down(e):
    """ close the actual session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
