import hashlib
import uuid
from flask import request, render_template


class CrossCheck(object):
    _instance = None

    class CrossCheckSingleton:

        def __init__(self):
            self._salt = str(uuid.uuid4())

        def generate_token(self):
            token = str(uuid.uuid4())
            return token, self._encode_token(token)

        def valid_token(self, token, hashed):
            return True if (hashed == self._encode_token(token)) else False

        def _encode_token(self, token):
            return hashlib.sha224(token + self._salt).hexdigest()

    def __init__(self):
        if CrossCheck._instance is None:
            CrossCheck._instance = CrossCheck.CrossCheckSingleton()
        self._EventHandler_instance = CrossCheck._instance

    def __getattr__(self, attr):
        return getattr(self._instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self._instance, attr, value)


def cross_check(handler):
    def decorator():
        cc = CrossCheck()
        token = request.args.get('cross_check', '')
        cookie = request.cookies.get('cross_check')
        result = None
        if cc.valid_token(token, cookie):
            result = handler()
        else:
            result = render_template('problem.html', problem='Request is not valid')
        return result
    return decorator


if __name__ == '__main__':
    cc1 = CrossCheck()
    cc2 = CrossCheck()
    t1, h1 = cc1.generate_token()
    t2, h2 = cc2.generate_token()
    print 'one: ' + cc1._salt + ' - ' + t1 + ' - ' + h1
    print 'two: ' + cc2._salt + ' - ' + t2 + ' - ' + h2
    print cc1.valid_token(t1, h1)
    print cc1.valid_token(t2, h1)