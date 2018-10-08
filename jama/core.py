import requests

__DEBUG__ = False


class Core:
    """ This Class will contain a collection of methods that interact directly with the Jama API and return A Requests
    Response Object.  This class will give the user more fine grained access to the JAMA API.  For more information
    on the Requests library visit: http://docs.python-requests.org/en/master/"""

    def __init__(self, host_name, user_credentials, api_version='/rest/v1/'):
        # Class variables
        self.__api_version = api_version
        self.__host_name = host_name + self.__api_version
        self.__credentials = user_credentials

    def delete(self, resource, **kwargs):
        """ This method will perform a delete operation on the specified resource"""
        url = self.__host_name + resource
        return requests.delete(url, auth=self.__credentials, **kwargs)

    def get(self, resource, params=None, **kwargs):
        """ This method will perform a get operation on the specified resource"""
        url = self.__host_name + resource
        return requests.get(url, auth=self.__credentials, params=params, **kwargs)

    def patch(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a patch operation to the specified resource"""
        url = self.__host_name + resource
        return requests.patch(url, auth=self.__credentials, params=params, data=data, json=json, **kwargs)

    def post(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a post operation to the specified resource."""
        url = self.__host_name + resource
        return requests.post(url, auth=self.__credentials, params=params, data=data, json=json, **kwargs)

    def put(self, resource, params=None, data=None, json=None, **kwargs):
        """ This method will perform a put operation to the specified resource"""
        url = self.__host_name + resource
        return requests.put(url, auth=self.__credentials, data=data, params=params, json=json, **kwargs)
