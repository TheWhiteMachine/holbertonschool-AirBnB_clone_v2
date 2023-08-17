#!/usr/bin/python3
""" this module start a web app with flask """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """ a web page that shows different filtered data from db"""
    states = storage.all(State)
    return render_template('10-hbnb_filters.html', states=states)


@app.teardown_appcontext
def tear_down(e):
    """ close the actual session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
