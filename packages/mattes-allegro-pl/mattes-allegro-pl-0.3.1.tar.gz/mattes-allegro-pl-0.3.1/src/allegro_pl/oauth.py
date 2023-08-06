import abc
import concurrent.futures
import json
import logging
import typing
from dataclasses import dataclass

import allegro_api.rest
import oauthlib.oauth2
import requests.exceptions
import requests_oauthlib
import zeep.exceptions

URL_TOKEN = 'https://allegro.pl/auth/oauth/token'
logger = logging.getLogger(__name__)


@dataclass
class TokenStore(abc.ABC):
    def __init__(self):
        self._access_token: typing.Optional[str] = None
        self._refresh_token: typing.Optional[str] = None

    @abc.abstractmethod
    def save(self):
        logger.debug('save tokens')

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self._access_token = access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token: str) -> None:
        self._refresh_token = refresh_token

    @classmethod
    def from_dict(cls: typing.Type['TokenStore'], data: dict) -> 'TokenStore':
        ts = cls()
        ts.update_from_dict(data)
        return ts

    def update_from_dict(self, data: dict) -> None:
        self.access_token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')

    def to_dict(self):
        d = {}
        if self._access_token:
            d['access_token'] = self.access_token
        if self._refresh_token:
            d['refresh_token'] = self.refresh_token
        return d


class PassTokenStore(TokenStore):
    """In-memory Token store implementation"""

    def save(self):
        pass


class AllegroAuth:
    """Handle acquiring and refreshing access_token"""

    def __init__(self, client_id: str, client_secret: str, token_store: TokenStore):
        self.client_id: str = client_id
        self.client_secret: str = client_secret

        assert token_store is not None
        self._token_store = token_store

        self._notify_token_updated: typing.Callable[[], None] = self._on_token_updated_pass

    def _on_token_updated(self, token):
        logger.debug('token updated')
        self._token_store.update_from_dict(token)
        self._token_store.save()
        self._notify_token_updated()

    def _on_token_updated_pass(self):
        pass

    def set_token_update_handler(self, f: typing.Callable[[], None]) -> None:
        self._notify_token_updated = f

    @property
    def token_store(self) -> TokenStore:
        return self._token_store

    @staticmethod
    def token_needs_refresh(retry_state) -> bool:
        x = retry_state.outcome.exception(0)
        if x is None:
            return False
        if isinstance(x, allegro_api.rest.ApiException) and x.status == 401:
            body = json.loads(x.body)
            return body['error'] == 'invalid_token' and body['error_description'].startswith('Access token expired: ')
        elif isinstance(x, zeep.exceptions.Fault):
            if x.code == 'ERR_INVALID_ACCESS_TOKEN':
                return True
            else:
                raise x
        elif isinstance(x, requests.exceptions.ConnectionError):
            return x.args[0].args[0] == 'Connection aborted.'
        else:
            raise x

    @abc.abstractmethod
    def fetch_token(self):
        logger.info('fetch token')

    @abc.abstractmethod
    def refresh_token(self):
        logger.info('refresh token')


class ClientCredentialsAuth(AllegroAuth):
    """Authenticate with Client credentials flow"""

    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, PassTokenStore())

        client = oauthlib.oauth2.BackendApplicationClient(self.client_id, access_token=self.token_store.access_token)

        self.oauth = requests_oauthlib.OAuth2Session(client=client, token_updater=self._on_token_updated)

    def fetch_token(self):
        token = self.oauth.fetch_token(URL_TOKEN, client_id=self.client_id, client_secret=self.client_secret)
        self._on_token_updated(token)

    def refresh_token(self):
        return self.fetch_token()
