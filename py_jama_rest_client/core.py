import math
import urllib3
import ssl
import requests
import time
import logging
from py_jama_rest_client.exceptions import UnauthorizedTokenException

__DEBUG__ = False

py_jama_rest_client_logger = logging.getLogger("py_jama_rest_client-core")

# disable warnings for ssl verification
urllib3.disable_warnings()


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    """
    Custom HTTP transport adapter class which allows us to use custom
    ssl_context to bypass 'SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED' error
    """

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def get_session(
    ctx: ssl.SSLContext = None, verify: bool = False, **kwargs
) -> requests.Session:
    """
    Getter function to return session object which implements
    CustomHttpAdapter
    """
    if ctx is None:
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    if not verify:
        ctx.check_hostname = False  # allows user to disable ssl verification
    session = requests.Session(**kwargs)
    session.mount("https://", CustomHttpAdapter(ctx))
    return session


class Core:
    """
    This Class will contain a collection of methods that interact directly with the Jama API and return A Requests
    Response Object.  This class will give the user more fine grained access to the JAMA API.  For more information
    on the Requests library visit: http://docs.python-requests.org/en/master/
    """

    def __init__(
        self,
        host_name,
        user_credentials,
        api_version="/rest/v1/",
        oauth=False,
        verify=True,
    ):
        # Instance variables
        self.__api_version = api_version
        self.__host_name = host_name + self.__api_version
        self.__credentials = user_credentials
        self.__oauth = oauth
        self.__verify = verify
        self._session = get_session()

        # Setup OAuth if needed.
        if self.__oauth:
            self.__token_host = host_name + "/rest/oauth/token"
            self.__token = None
            self.__get_fresh_token()

    def close(self) -> None:
        """Method to close underlying session"""
        self._session.close()

    def delete(self, resource, **kwargs):
        """This method will perform a delete operation on the specified resource"""
        url = self.__host_name + resource
        kwargs["verify"] = self.__verify

        if self.__oauth:
            self.__check_oauth_token()
            kwargs["headers"] = self.__add_auth_header(**kwargs)
            return self._session.delete(url, **kwargs)

        return self._session.delete(url, auth=self.__credentials, **kwargs)

    def get(self, resource, params=None, **kwargs):
        """This method will perform a get operation on the specified resource"""
        url = self.__host_name + resource
        kwargs["verify"] = self.__verify

        if self.__oauth:
            self.__check_oauth_token()
            kwargs["headers"] = self.__add_auth_header(**kwargs)
            return self._session.get(url, params=params, **kwargs)

        return self._session.get(url, auth=self.__credentials, params=params, **kwargs)

    def patch(self, resource, params=None, data=None, json=None, **kwargs):
        """This method will perform a patch operation to the specified resource"""
        url = self.__host_name + resource
        kwargs["verify"] = self.__verify

        if self.__oauth:
            self.__check_oauth_token()
            kwargs["headers"] = self.__add_auth_header(**kwargs)
            return self._session.patch(
                url, params=params, data=data, json=json, **kwargs
            )

        return self._session.patch(
            url, auth=self.__credentials, params=params, data=data, json=json, **kwargs
        )

    def post(self, resource, params=None, data=None, json=None, **kwargs):
        """This method will perform a post operation to the specified resource."""
        url = self.__host_name + resource
        kwargs["verify"] = self.__verify

        if self.__oauth:
            self.__check_oauth_token()
            kwargs["headers"] = self.__add_auth_header(**kwargs)
            return self._session.post(
                url, params=params, data=data, json=json, **kwargs
            )

        return self._session.post(
            url, auth=self.__credentials, params=params, data=data, json=json, **kwargs
        )

    def put(self, resource, params=None, data=None, json=None, **kwargs):
        """This method will perform a put operation to the specified resource"""
        url = self.__host_name + resource
        kwargs["verify"] = self.__verify

        if self.__oauth:
            self.__check_oauth_token()
            kwargs["headers"] = self.__add_auth_header(**kwargs)
            return self._session.put(url, data=data, params=params, json=json, **kwargs)

        return self._session.put(
            url, auth=self.__credentials, data=data, params=params, json=json, **kwargs
        )

    def __check_oauth_token(self):
        if self.__token is None:
            self.__get_fresh_token()

        else:
            time_elapsed = time.time() - self.__token_acquired_at
            time_remaining = self.__token_expires_in - time_elapsed
            if time_remaining < 60:
                # if less than a minute remains, just get another token.
                self.__get_fresh_token()

    def __get_fresh_token(self):
        """This method will fetch a new oauth bearer token from the oauth token server."""
        data = {"grant_type": "client_credentials"}

        # By getting the system time before we get the token we avoid a potential bug where the token may be expired.
        time_before_request = time.time()

        # Post to the token server, check if authorized
        try:
            response = requests.post(
                self.__token_host,
                auth=self.__credentials,
                data=data,
                verify=self.__verify,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            message = "Unable to fetch token: "
            raise UnauthorizedTokenException(message + str(err), response.status_code)

        # If success get relevant data
        if response.status_code in [200, 201]:
            response_json = response.json()
            self.__token = response_json["access_token"]
            self.__token_expires_in = response_json["expires_in"]
            self.__token_acquired_at = math.floor(time_before_request)

        else:
            py_jama_rest_client_logger.error("Failed to retrieve OAuth Token")

    def __add_auth_header(self, **kwargs):
        headers = kwargs.get("headers")
        if headers is None:
            headers = {}
        headers["Authorization"] = "Bearer " + self.__token
        return headers
