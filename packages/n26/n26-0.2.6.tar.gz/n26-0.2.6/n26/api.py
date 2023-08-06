import time

import requests
from n26 import config

BASE_URL = 'https://api.tech26.de'
BASIC_AUTH_HEADERS = {'Authorization': 'Basic YW5kcm9pZDpzZWNyZXQ='}

GET = "get"
POST = "post"

EXPIRATION_TIME_KEY = "expiration_time"
ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"


class Api(object):
    """
    Api class can be imported as a library in order to use it within applications
    """

    def __init__(self, cfg=None):
        """
        # constructor accepting None to maintain backward compatibility
        :param cfg: configuration object
        """
        if not cfg:
            cfg = config.get_config()
        self.config = cfg
        self._token_data = {}

    # IDEA: @get_token decorator
    def get_account_info(self):
        return self._do_request(GET, BASE_URL + '/api/me')

    def get_account_statuses(self):
        return self._do_request(GET, BASE_URL + '/api/me/statuses')

    def get_addresses(self):
        return self._do_request(GET, BASE_URL + '/api/addresses')

    def get_balance(self):
        return self._do_request(GET, BASE_URL + '/api/accounts')

    def get_spaces(self):
        return self._do_request(GET, BASE_URL + '/api/spaces')

    def barzahlen_check(self):
        return self._do_request(GET, BASE_URL + '/api/barzahlen/check')

    def get_cards(self):
        return self._do_request(GET, BASE_URL + '/api/v2/cards')

    def get_account_limits(self):
        return self._do_request(GET, BASE_URL + '/api/settings/account/limits')

    def get_contacts(self):
        return self._do_request(GET, BASE_URL + '/api/smrt/contacts')

    def get_standing_orders(self):
        return self._do_request(GET, BASE_URL + '/api/transactions/so')

    def get_transactions(self, from_time=None, to_time=None, limit=None, pending=None, categories=None,
                         text_filter=None, last_id=None):
        """
        Get a list of transactions.

        Note that some parameters can not be combined in a single request (like text_filter and pending) and
        will result in a bad request (400) error.

        :param from_time: earliest transaction time as a Timestamp - milliseconds since 1970 in CET
        :param to_time: latest transaction time as a Timestamp - milliseconds since 1970 in CET
        :param limit: Limit the number of transactions to return to the given amount
        :param pending: show pending or not pending only
        :param categories: Comma separated list of category IDs
        :param text_filter: Query string to search for
        :param last_id: ??
        :return: list of transactions
        """
        return self._do_request(GET, BASE_URL + '/api/smrt/transactions', {
            'from': from_time,
            'to': to_time,
            'limit': limit,
            'pending': pending,
            'categories': categories,
            'textFilter': text_filter,
            'lastId': last_id
        })

    def get_transactions_limited(self, limit=5):
        import warnings
        warnings.warn(
            "get_transactions_limited is deprecated, use get_transactions(limit=5) instead",
            DeprecationWarning
        )
        return self.get_transactions(limit=limit)

    def get_statements(self):
        return self._do_request(GET, BASE_URL + '/api/statements')

    def block_card(self, card_id):
        return self._do_request(POST, BASE_URL + '/api/cards/%s/block' % card_id)

    def unblock_card(self, card_id):
        return self._do_request(POST, BASE_URL + '/api/cards/%s/unblock' % card_id)

    def get_savings(self):
        return self._do_request(GET, BASE_URL + '/api/hub/savings/accounts')

    def get_statistics(self, from_time=0, to_time=int(time.time()) * 1000):
        """
        Get statistics in a given time frame
        :param from_time: Timestamp - milliseconds since 1970 in CET
        :param to_time: Timestamp - milliseconds since 1970 in CET
        """

        if not from_time:
            from_time = 0

        if not to_time:
            to_time = int(time.time()) * 1000

        return self._do_request(GET, BASE_URL + '/api/smrt/statistics/categories/%s/%s' % (from_time, to_time))

    def get_available_categories(self):
        return self._do_request(GET, BASE_URL + '/api/smrt/categories')

    def get_invitations(self):
        return self._do_request(GET, BASE_URL + '/api/aff/invitations')

    def _do_request(self, method=GET, url="/", params={}):
        access_token = self.get_token()
        headers = {'Authorization': 'bearer' + str(access_token)}

        first_param = True
        for k, v in params.items():
            if not v:
                # skip None values
                continue

            if first_param:
                url += '?'
                first_param = False
            else:
                url += '&'

            url += "%s=%s" % (k, v)

        if method is GET:
            response = requests.get(url, headers=headers)
        elif method is POST:
            response = requests.post(url, headers=headers)
        else:
            return None

        response.raise_for_status()
        return response.json()

    def get_token(self):
        """
        Returns the access token to use for api authentication.
        If a token has been requested before it will be reused if it is still valid.
        If the previous token has expired it will be refreshed.
        If no token has been requested it will be requested from the server.

        :return: the access token
        """
        if not self._validate_token(self._token_data):
            if REFRESH_TOKEN_KEY in self._token_data:
                refresh_token = self._token_data[REFRESH_TOKEN_KEY]
                self._token_data = self._refresh_token(refresh_token)
            else:
                self._token_data = self._request_token(self.config.username, self.config.password)

            # add expiration time to expiration in _validate_token()
            self._token_data[EXPIRATION_TIME_KEY] = time.time() + self._token_data["expires_in"]

        # if it's still not valid, raise an exception
        if not self._validate_token(self._token_data):
            raise PermissionError("Unable to request authentication token")

        return self._token_data[ACCESS_TOKEN_KEY]

    @staticmethod
    def _request_token(username, password):
        """
        Request an authentication token from the server
        :return: the token or None if the response did not contain a token
        """
        values_token = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }

        response = requests.post(BASE_URL + '/oauth/token', data=values_token, headers=BASIC_AUTH_HEADERS)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _refresh_token(refresh_token):
        """
        Refreshes an authentication token
        :param refresh_token: the refresh token issued by the server when requesting a token
        :return: the refreshed token data
        """
        values_token = {
            'grant_type': REFRESH_TOKEN_KEY,
            'refresh_token': refresh_token
        }

        response = requests.post(BASE_URL + '/oauth/token', data=values_token, headers=BASIC_AUTH_HEADERS)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _validate_token(token_data):
        """
        Checks if a token is valid
        :param token_data: the token data to check
        :return: true if valid, false otherwise
        """

        if EXPIRATION_TIME_KEY not in token_data:
            # there was a problem adding the expiration_time property
            return False
        elif time.time() >= token_data[EXPIRATION_TIME_KEY]:
            # token has expired
            return False

        return ACCESS_TOKEN_KEY in token_data and token_data[ACCESS_TOKEN_KEY]
