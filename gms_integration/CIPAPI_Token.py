import time
import jwt # PyJWT package
import requests

class Token(object):
    def __init__(self, client_id, client_secret, auth_url):
        """
        Initialise with client id, client secret, and auth url
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_url = auth_url
        self._set_token()

    def _set_token(self):
        """
        setter method to fetch a new token from AD tenant
        """
        auth_response = requests.post(
            self._auth_url,
            data="grant_type=client_credentials",
            auth=(self._client_id, self._client_secret)
        ).json()
        self._token = auth_response['access_token']
        self._decoded_token = jwt.decode(self._token, verify=False)

    def token(self):
        """
        getter method for accessing the token. Triggers a token refresh if expired.
        """
        # If expired, or within 60 seconds of expiry, get a new token
        if time.time() > (self._decoded_token['exp'] - 60):
            self._set_token()
        # Return token
        return self._token