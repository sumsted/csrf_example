__author__ = 'scottumsted'
import random
from flask import render_template, request
from badguywebsite import app


@app.route('/', methods=['GET'])
def landing():
    return render_template('index.html')

@app.route('/detail', methods=['GET'])
def detail():
    request_type = request.args.get('type', 'CSRF_UNSECURE')
    url = (app.config[request_type] if request_type in app.config else app.config['CSRF_UNSECURE']) + \
          str(random.randint(80, 110))
    return render_template('detail.html', csrf_url=url)
