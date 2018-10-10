import json

from jama.core import Core

__DEBUG__ = False


class JamaClient:
    """A class to abstract communication with the Jama Connect API"""

    __allowed_results_per_page = 20  # Default is 20, Max is 50. if set to greater than 50, only 50 will items return.

    def __init__(self, host_domain, credentials=('username', 'password'), api_version='/rest/v1/'):
        """Jama Client initializer
        :param host_domain The domain associated with the jama connect host
        :param credentials the user name and password as a tuple
        :param api_version valid args are '/rest/[v1|latest|labs]/' """
        self.__credentials = credentials
        self.__core = Core(host_domain, credentials, api_version=api_version)

    def get_projects(self):
        """This method will return all projects as JSON object"""
        resource_path = 'projects'
        project_data = self.__get_all(resource_path)
        return project_data

    def get_items(self, project_id):
        """This method will return all items in the specified project.  it will return a Json array of item objects"""
        resource_path = 'items'
        params = {'project': project_id}
        item_data = self.__get_all(resource_path, params=params)
        return item_data

    def get_abstract_items_from_doc_key(self, doc_key_list):
        """This method will take in a list of document keys and return an array of JSON Objects associated with the
        document keys."""
        resource_path = 'abstractitems'
        params = {'documentKey': doc_key_list}
        abstract_items = self.__get_all(resource_path, params=params)
        return abstract_items

    def get_testruns(self, test_cycle_id):
        """This method will return all test runs associated with the specified test cycle.  Test runs will be returned
        as a list of json objects."""
        resource_path = 'testcycles/' + str(test_cycle_id) + '/testruns'
        testrun_data = self.__get_all(resource_path)
        return testrun_data

    def get_test_cycle(self, test_cycle_id):
        """ This method will return JSON data about the test cycle specified by the test cycle id."""
        resource_path = 'testcycles/' + str(test_cycle_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def post_item(self, project, item_type_id, child_item_type_id, location, fields):
        """ This method will post a new item to Jama Connect.
        :param project integer representing the project to which this item is to be posted
        :param item_type_id integer ID of an Item Type.
        :param child_item_type_id integer ID of an Item Type.
        :param location dictionary with integer ID of the parent item or project.
        :param fields dictionary item field data.
        :return integer ID of the successfully posted item or None if there was an error."""

        body = {
            "project": project,
            "itemType": item_type_id,
            "childItemType": child_item_type_id,
            "location": {
                "parent": location
            },
            "fields": fields
        }
        resource_path = 'items/'
        headers = {'content-type': 'application/json'}
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)
        JamaClient.__handle_response_status(response)
        return response.json()['meta']['id']

    def put_attachments_file(self, attachment_id, file_path):
        """
        Upload a file to a jama attachment
        :param attachment_id: the integer ID of the attachment item to which we are uploading the file
        :param file_path: the file path of the file to be uploaded
        :return: returns the status code of the call
        """
        resource_path = 'attachments/' + str(attachment_id) + '/file'
        with open(file_path, 'rb') as f:
            response = self.__core.put(resource_path, data=f)

        self.__handle_response_status(response)
        return response.status_code

    def put_test_run(self, test_run_id, data=None):
        """ This method will post a test run to Jama through the API"""
        resource_path = 'testruns/' + str(test_run_id)
        headers = {'content-type': 'application/json'}
        response = self.__core.put(resource_path, data=data, headers=headers)
        return self.__handle_response_status(response)

    def __get_all(self, resource, params=None, **kwargs):
        """This method will get all of the resources specified by the resource parameter, if an id or some other parameter
        is required for the resource, include it in the params parameter.
        Returns a single JSON array with all of the retrieved items."""

        start_index = 0
        result_count = -1
        allowed_results_per_page = 20

        data = []

        while result_count != 0:
            page_response = self.__get_page(resource, start_index, params=params, **kwargs)
            page_json = page_response.json()

            page_info = page_json['meta']['pageInfo']
            start_index = page_info['startIndex'] + allowed_results_per_page
            result_count = page_info['resultCount']

            page_data = page_json.get('data')
            data.extend(page_data)

        return data

    def __get_page(self, resource, start_at, params=None, **kwargs):
        """This method will return one page of results from the specified resource type.
        Pass any needed parameters along
        The response object will be returned"""
        parameters = {
            'startAt': start_at,
            'maxResults': self.__allowed_results_per_page
        }

        if params is not None:
            for k, v in params.items():
                parameters[k] = v

        response = self.__core.get(resource, params=parameters, **kwargs)
        JamaClient.__handle_response_status(response)
        return response

    @staticmethod
    def __handle_response_status(response):
        """ Utility method for checking http status codes.
        If the response code is not in the 200 range, An exception will be thrown."""

        status = response.status_code

        if status in range(200, 300):
            return status

        if status in range(400, 500):
            """These are client errors. It is likely that something is wrong with the request."""
            if status == 401:
                raise Exception("Unauthorized: check credentials and permissions.")

            if status == 404:
                raise Exception("Resource not found. check host url.")

            if status == 429:
                raise Exception("Too many requests.  API throttling limit reached, or system under maintenance.")

            raise Exception("{} Client Error.  Bad Request.".format(status))

        if status in range(500, 600):
            """These are server errors and network errors."""
            raise Exception("{} Server Error.".format(status))



