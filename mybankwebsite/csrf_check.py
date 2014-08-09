import hashlib
import uuid
import logging
from flask import request, render_template
from mybankwebsite import app


class CsrfCheck:
    def __init__(self):
        self._salt = app.config['CSRF_SALT']

    def generate_token(self):
        token = str(uuid.uuid4())
        return token, self._encode_token(token)

    def valid_token(self, token, hashed):
        try:
            return True if (hashed == self._encode_token(token)) else False
        except Exception, e:
            logging.info('valid_token: %s', e.message)
            return False

    def _encode_token(self, token):
        return hashlib.sha224(token + self._salt).hexdigest()


def csrf_check(handler):
    def decorator():
        cc = CsrfCheck()
        token = None
        cookie = request.cookies.get('csrf_check')
        if request.method == 'GET':
            token = request.args.get('csrf_check', None)
        elif request.method == 'POST':
            try:
                token = request.form['csrf_check']
            except Exception, e:
                logging.error('cc: unable to retrieve token, %s', e.message)
                token = None
        result = None
        if cc.valid_token(token, cookie):
            result = handler()
        else:
            logging.error('cc: no match, %s, %s', token, cookie)
            result = render_template('problem.html', message='Your request is not valid.')
        return result
    return decorator