import math

import requests
import time

__DEBUG__ = False


class Core:
    """ This Class will contain a collection of methods that interact directly with the Jama API and return A Requests
    Response Object.  This class will give the user more fine grained access to the JAMA API.  For more information
    on the Requests library visit: http://docs.python-requests.org/en/master/"""

    def __init__(self, host_name, user_credentials, api_version='/rest/v1/', oauth=False):
        # Class variables
        self.__api_version = api_version
        self.__host_name = host_name + self.__api_version
        self.__credentials = user_credentials
        self.__oauth = oauth

        # Setup OAuth if needed.
        if self.__oauth:
            self.__token_host = host_name + '/rest/oauth/token'
            self.__token = None
            self.__get_fresh_token()

    def delete(self, resource, **kwargs):
        """ This method will perform a delete operation on the specified resource"""
        url = self.__host_name + resource

        if self.__oauth:
            self.__check_oauth_token()
            kwargs['headers'] = self.__add_auth_header(**kwargs)
            return requests.delete(url, **kwargs)

        return requests.delete(url, auth=self.__credentials, **kwargs)

    def get(self, resource, params=None, **kwargs):
        """ This method will perform a get operation on the specified resource"""
        url = self.__host_name + resource

        if self.__oauth:
            self.__check_oauth_token()
            kwargs['headers'] = self.__add_auth_header(**kwargs)
            return requests.get(url, params=params, **kwargs)

        return requests.get(url, auth=self.__credentials, params=params, **kwargs)

    def patch(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a patch operation to the specified resource"""
        url = self.__host_name + resource

        if self.__oauth:
            self.__check_oauth_token()
            kwargs['headers'] = self.__add_auth_header(**kwargs)
            return requests.patch(url, params=params, data=data, json=json, **kwargs)

        return requests.patch(url, auth=self.__credentials, params=params, data=data, json=json, **kwargs)

    def post(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a post operation to the specified resource."""
        url = self.__host_name + resource

        if self.__oauth:
            self.__check_oauth_token()
            kwargs['headers'] = self.__add_auth_header(**kwargs)
            return requests.post(url, params=params, data=data, json=json, **kwargs)

        return requests.post(url, auth=self.__credentials, params=params, data=data, json=json, **kwargs)

    def put(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a put operation to the specified resource"""
        url = self.__host_name + resource

        if self.__oauth:
            self.__check_oauth_token()
            kwargs['headers'] = self.__add_auth_header(**kwargs)
            return requests.put(url, data=data, params=params, json=json, **kwargs)

        return requests.put(url, auth=self.__credentials, data=data, params=params, json=json, **kwargs)

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
        data = {
            'grant_type': 'client_credentials'
        }

        # By getting the system time before we get the token we avoid a potential bug where the token may be expired.
        time_before_request = time.time()

        # Post to the token server
        response = requests.post(self.__token_host, auth=self.__credentials, data=data)

        # If success get relevant data
        if response.status_code in [200, 201]:
            response_json = response.json()
            self.__token = response_json['access_token']
            self.__token_expires_in = response_json['expires_in']
            self.__token_acquired_at = math.floor(time_before_request)

        else:
            print('Failed to retrieve OAuth Token')

    def __add_auth_header(self, **kwargs):
        headers = kwargs.get('headers')
        if headers is None:
            headers = {}
        headers['Authorization'] = 'Bearer ' + self.__token
        return headers

