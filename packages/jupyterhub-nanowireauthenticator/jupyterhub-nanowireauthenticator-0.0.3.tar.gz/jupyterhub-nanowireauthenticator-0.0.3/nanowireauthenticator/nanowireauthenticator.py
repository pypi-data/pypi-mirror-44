from traitlets import Unicode

from jupyterhub.auth import Authenticator
from tornado import gen
import requests

NANOWIRE_AUTH_URL = 'http://nanowire-backend.default/v1/users/login'

class NanowireAuthenticator(Authenticator):

    @gen.coroutine
    def authenticate(handler, data):
        print("Trying to auth with ", data)
        try:
            resp = requests.post(
                NANOWIRE_AUTH_URL,
                { 'email': data['username'], 'password': data['password'] }
            )
            if resp.status_code == 200:
                return data['username']
            return None
        except Exception as e:
            return None

