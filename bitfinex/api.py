import requests
import urllib
from .exceptions import ApiError


class BitfinexApi(object):
    def __init__(self):
        self.host = 'https://api.bitfinex.com'
        self.version = 'v1'

    def orderbook(self, symbol='btcusd'):
        return self._get_api('book/' + symbol)

    def _get_api(self, action):
        print('{}/{}/{}'.format(self.host, self.version, action))
        response = requests.get('{}/{}/{}'.format(self.host, self.version, action))

        if response.status_code == 400:
            raise ApiError(response.json()['message'])
        else:
            return response.json()
