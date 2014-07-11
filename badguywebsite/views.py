__author__ = 'scottumsted'
from flask import render_template
from badguywebsite import app


@app.route('/', methods=['GET'])
def landing():
    return render_template('index.html')
