#!/usr/bin/python3
""" this module start a web app with flask """
from flask import Flask, abort, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_route():
    """  a hello word page """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hello_routehbnb_route():
    """ prints hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """  revive a text variable """
    text = text.replace('_', ' ')
    return f'C {text}'


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text_sroute(text):
    """  revive a text variable and have a default value"""
    text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<n>', strict_slashes=False)
def is_number(n):
    """ display if the number parameter is a number """
    if n.isdigit():
        int_n = int(n)
        return f'{int_n} is a number'
    abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def display_number(n):
    """ display if the number parameter is a number """
    if n.isdigit():
        int_n = int(n)
        return render_template('5-number.html', n=int_n)
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
