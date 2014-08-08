import hashlib
import uuid

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
