import requests
import json
import base64
import hmac
import time
import hashlib


class BitfinexTradingApi(object):

    def __init__(self, auth_key, auth_secret):
        self.api_key = auth_key
        self.api_secret = auth_secret
        self.host = 'https://api.bitfinex.com'
        self.version = 'v1'

    def balances(self):
        payload = {
            'request': '/{}/balances'.format(self.version),
            'nonce': self.__class__._get_nonce()
        }
        return self._get_api('balances', payload)

    def _get_api(self, action, payload):
        url = '{}/{}/{}'.format(self.host, self.version, action)
        response = requests.post(url, headers=self._pack_payload(payload), verify=True)
        return response.json()

    def _pack_payload(self, payload):
        encoded_payload = base64.standard_b64encode(json.dumps(payload))
        return {
            'X-BFX-APIKEY': self.api_key,
            'X-BFX-SIGNATURE': self._sign_payload(encoded_payload),
            'X-BFX-PAYLOAD': encoded_payload
        }

    def _sign_payload(self, encoded_payload):
        return hmac.new(self.api_secret, encoded_payload, hashlib.sha384).hexdigest()

    @staticmethod
    def _get_nonce():
        return str(time.time() * 1000)
