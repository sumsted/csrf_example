import hashlib
import uuid
from flask import request, render_template


class CrossCheck:

    def __init__(self):
        self._salt = str(uuid.uuid4())
        print 'salt: %s' % (self._salt)

    def generate_token(self):
        token = str(uuid.uuid4())
        return token, self._encode_token(token)

    def valid_token(self, token, hashed):
        return True if (hashed == self._encode_token(token)) else False

    def _encode_token(self, token):
        return hashlib.sha224(token + self._salt).hexdigest()


if __name__ == '__main__':
    cc1 = CrossCheck()
    cc2 = CrossCheck()
    t1, h1 = cc1.generate_token()
    t2, h2 = cc2.generate_token()
    print 'one: ' + cc1._salt + ' - ' + t1 + ' - ' + h1
    print 'two: ' + cc2._salt + ' - ' + t2 + ' - ' + h2
    print cc1.valid_token(t1, h1)
    print cc1.valid_token(t2, h1)