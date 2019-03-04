import json

from .core import Core

__DEBUG__ = False


class APIException(Exception):
    """This is the base class for all exceptions raised by the JamaClient"""
    pass


class UnauthorizedException(APIException):
    """This exception is thrown whenever the api returns a 401 unauthorized response."""
    pass


class TooManyRequestsException(APIException):
    """This exception is thrown whenever the api returns a 429 too many requests response."""
    pass


class ResourceNotFoundException(APIException):
    """This exception is raised whenever the api returns a 404 not found response."""
    pass


class AlreadyExistsException(APIException):
    """This exception is thrown when the API returns a 400 response with a message that the resource already exists."""
    pass


class APIClientException(APIException):
    """This exception is thrown whenever a unknown 400 error is encountered."""
    pass


class APIServerException(APIException):
    """This exception is thrown whenever an unknown 500 response is encountered."""
    pass


class JamaClient:
    """A class to abstract communication with the Jama Connect API"""

    __allowed_results_per_page = 20  # Default is 20, Max is 50. if set to greater than 50, only 50 will items return.

    def __init__(self, host_domain, credentials=('username', 'password'), api_version='/rest/v1/', oauth=False):
        """Jama Client initializer
        :rtype: JamaClient
        :param host_domain: String The domain associated with the Jama Connect host
        :param credentials: the user name and password as a tuple
        :param api_version: valid args are '/rest/[v1|latest|labs]/' """
        self.__credentials = credentials
        self.__core = Core(host_domain, credentials, api_version=api_version, oauth=oauth)

    def get_projects(self):
        """This method will return all projects as JSON object
        :return: JSON Array of Item Objects.
        """
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

    def delete_item(self, item_id):
        """
        This method will delete an item in Jama Connect.

        Args:
            item_id: The jama connect API ID of the item to be deleted

        Returns: The success status code.
        """
        resource_path = 'items/' + str(item_id)
        response = self.__core.delete(resource_path)
        JamaClient.__handle_response_status(response)
        return response.status_code

    def post_testplans_testcycles(self, testplan_id, testcycle_name, start_date, end_date, testgroups_to_include=None, testrun_status_to_include=None):
        """
        This method will create a new Test Cycle.

        Args:
            testplan_id (int): The API_ID of the testplan to create the test cycle from.
            testcycle_name (str): The name you would like to set for the new Test Cycle
            start_date (str): Start date in 'yyyy-mm-dd' Format
            end_date (str): End date in 'yyyy-mm-dd' Format
            testgroups_to_include (int[]):  This array of integers specify the test groups to be included.
            testrun_status_to_include (str[]): Only valid after generating the first Test Cycle, you may choose to only
                generate Test Runs that were a specified status in the previous cycle. Do not specify anything to
                include all statuses

        Returns:
            (int): Returns the integer id for the newly created testcycle, or None if something went terribly wrong.
        """
        resource_path = 'testplans/' + str(testplan_id) + '/testcycles'
        headers = {'content-type': 'application/json'}
        fields = {
            'name': testcycle_name,
            'startDate': start_date,
            'endDate': end_date
        }
        test_run_gen_config = {}
        if testgroups_to_include is not None:
            test_run_gen_config['testGroupsToInclude'] = testgroups_to_include
        if testrun_status_to_include is not None:
            test_run_gen_config['testRunStatusesToInclude'] = testrun_status_to_include
        body = {
            'fields': fields,
            'testRunGenerationConfig': test_run_gen_config
        }

        # Make the API Call
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)

        # Validate response
        JamaClient.__handle_response_status(response)
        return response.json()['meta']['id']

    def patch_item(self, item_id, patches):
        """
        This method will patch an item.
        Args:
            item_id: the API ID of the item that is to be patched
            patches: An array of dicts, that represent patch operations each dict should have the following entries
             [
                {
                    "op": string,
                    "path": string,
                    "value": {}
                }
            ]

        Returns: The response status code

        """
        resource_path = 'items/' + str(item_id)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'
                   }
        data = json.dumps(patches)

        # Make the API Call
        response = self.__core.patch(resource_path, data=data, headers=headers)

        # validate response
        JamaClient.__handle_response_status(response)
        return response.json()['meta']['status']

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

    def post_relationship(self, from_item: int, to_item: int, relationship_type=None):
        """

        Args:
            from_item: integer API id of the source item
            to_item: integer API id of the target item
            relationship_type: Optional integer API id of the relationship type to create

        Returns: The integer ID of the newly created relationship.

        """
        body = {
          "fromItem": from_item,
          "toItem": to_item,
        }
        if relationship_type is not None:
            body['relationshipType'] = relationship_type
        resource_path = 'relationships/'
        headers = {'content-type': 'application/json'}
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)
        JamaClient.__handle_response_status(response)
        return response.json()['meta']['id']


    def post_item_attachment(self, item_id, attachment_id):
        """
        Add an existing attachment to the item with the specified ID
        :param item_id: this is the ID of the item
        :param attachment_id: The ID of the attachment
        :return: 201 if successful / the response status of the post operation
        """
        body = {"attachment": attachment_id}
        resource_path = 'items/' + str(item_id) + '/attachments'
        headers = {'content-type': 'application/json'}
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)
        JamaClient.__handle_response_status(response)
        return response.status_code

    def post_project_attachment(self, project_id, name, description):
        """
        This Method will make a new attachment object in the specified project
        :param project_id: The integer project ID to create the attachment in.
        :param name:  The name of the attachment
        :param description: The description of the attachment
        :return: Returns the ID of the newly created attachment object.
        """
        body = {
            "fields": {
                "name": name,
                "description": description
            }
        }

        resource_path = 'projects/' + str(project_id) + '/attachments'
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
            files = {'file': f}
            response = self.__core.put(resource_path, files=files)

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
                raise UnauthorizedException("Unauthorized: check credentials and permissions.")

            if status == 404:
                raise ResourceNotFoundException("Resource not found. check host url.")

            if status == 429:
                raise TooManyRequestsException("Too many requests.  API throttling limit reached, or system under "
                                               "maintenance.")

            try:
                response_json = json.loads(response.text)
                response_message = response_json.get('meta').get('message')

                if "already exists" in response_message:
                    raise AlreadyExistsException("Entity already Exists.")

            except json.JSONDecodeError:
                pass

            raise APIClientException("{} Client Error.  Bad Request.  ".format(status) + response.reason)

        if status in range(500, 600):
            """These are server errors and network errors."""
            raise APIServerException("{} Server Error.".format(status))



