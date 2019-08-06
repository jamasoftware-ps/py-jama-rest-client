import json
import logging

from .core import Core

# This is the py_jama_rest_client logger.
py_jama_rest_client_logger = logging.getLogger('py_jama_rest_client')


class APIException(Exception):
    """This is the base class for all exceptions raised by the JamaClient"""

    def __init__(self, message, status_code=None, reason=None):
        super(APIException, self).__init__(message)
        self.status_code = status_code
        self.reason = reason


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

    def __init__(self, host_domain, credentials=('username|clientID', 'password|clientSecret'), api_version='/rest/v1/',
                 oauth=False):
        """Jama Client initializer
        :rtype: JamaClient
        :param host_domain: String The domain associated with the Jama Connect host
        :param credentials: the user name and password as a tuple or client id and client secret if using Oauth.
        :param api_version: valid args are '/rest/[v1|latest|labs]/' """
        self.__credentials = credentials
        self.__core = Core(host_domain, credentials, api_version=api_version, oauth=oauth)

        # Log client creation
        py_jama_rest_client_logger.info('Created a new JamaClient instance. Domain: {} '
                                        'Connecting via Oauth: {}'.format(host_domain, oauth))

    def get_available_endpoints(self):
        """
        Returns a list of all the available endpoints.

        Returns: an array of available endpoints for this API

        """
        response = self.__core.get('')
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_projects(self):
        """This method will return all projects as JSON object
        :return: JSON Array of Item Objects.
        """
        resource_path = 'projects'
        project_data = self.__get_all(resource_path)
        return project_data

    def get_filter_results(self, filter_id, project_id=None):
        """
        Get all results items for the filter with the specified ID

        Args:
            filter_id: The ID of the filter to fetch the results for.
            project_id: Use this only for filters that run on any project, where projectScope is CURRENT

        Returns:
            A List of items that match the filter.

        """
        resource_path = 'filters/' + str(filter_id) + '/results'
        params = None
        if project_id is not None:
            params = {'project': str(project_id)}
        filter_results = self.__get_all(resource_path, params=params)
        return filter_results

    def get_items(self, project_id):
        """
        This method will return all items in the specified project.
        Args:
            project_id: the project ID

        Returns: a Json array of item objects

        """
        resource_path = 'items'
        params = {'project': project_id}
        item_data = self.__get_all(resource_path, params=params)
        return item_data

    def get_item(self, item_id):
        """
        This method will return a singular item of a specified item id
        Args:
            item_id: the item id of the item to fetch

        Returns: a dictonary object representing the item

        """
        resource_path = 'items/' + str(item_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_item_lock(self, item_id):
        """
        Get the locked state, last locked date, and last locked by user for the item with the specified ID
        Args:
            item_id: The API ID of the item to get the lock info for.

        Returns:
            A JSON object with the lock information for the item with the specified ID.

        """
        resource_path = 'items/' + str(item_id) + '/lock'
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def put_item_lock(self, item_id, locked):
        """
        Update the locked state of the item with the specified ID
        Args:
            item_id: the API id of the item to be updated
            locked: boolean lock state to apply to this item

        Returns:
            response status 200

        """
        body = {
            "locked": locked,
        }
        resource_path = 'items/' + str(item_id) + '/lock'
        headers = {'content-type': 'application/json'}
        response = self.__core.put(resource_path, data=json.dumps(body), headers=headers)
        return self.__handle_response_status(response)

    def get_attachment(self, attachment_id):
        """
        This method will return a singular attachment of a specified attachment id
        Args:
            attachment_id: the attachment id of the attachment to fetch

        Returns: a dictonary object representing the attachment

        """
        resource_path = 'attachments/' + str(attachment_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_abstract_items_from_doc_key(self, doc_key_list):
        """ DEPRECATED INSTEAD USE get_abstract_items below.
        This method will take in a list of document keys and return an array of JSON Objects associated with the
        document keys."""
        resource_path = 'abstractitems'
        params = {'documentKey': doc_key_list}
        abstract_items = self.__get_all(resource_path, params=params)
        return abstract_items

    def get_relationship_types(self):
        """
        This method will return all relationship types of the across all projects of the Jama Connect instance.

        Returns: An array of dictionary objects

        """
        resource_path = 'relationshiptypes/'
        item_types = self.__get_all(resource_path)
        return item_types

    def get_relationship_type(self, relationship_type_id):
        """
        Gets relationship type information for a specific relationship type id.

        Args:
            relationship_type_id: The api id of the item type to fetch

        Returns: JSON object

        """
        resource_path = 'relationshiptypes/' + str(relationship_type_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_item_types(self):
        """
        This method will return all item types of the across all projects of the Jama Connect instance.

        Returns: An array of dictionary objects

        """
        resource_path = 'itemtypes/'
        item_types = self.__get_all(resource_path)
        return item_types

    def get_item_type(self, item_type_id):
        """
        Gets item type information for a specific item type id.

        Args:
            item_type_id: The api id of the item type to fetch

        Returns: JSON object

        """
        resource_path = 'itemtypes/' + str(item_type_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_items_synceditems(self, item_id):
        """
        Get all synchronized items for the item with the specified ID

        Args:
            item_id: The API id of the item being

        Returns: A list of JSON Objects representing the items that are in the same synchronization group as the
        specified item.

        """
        resource_path = 'items/' + str(item_id) + '/synceditems'
        synced_items = self.__get_all(resource_path)
        return synced_items

    def get_items_synceditems_status(self, item_id, synced_item_id):
        """
        Get the sync status for the synced item with the specified ID

        Args:
            item_id: The id of the item to compare against
            synced_item_id: the id of the item to check if it is in sync

        Returns: The response JSON from the API which contains a single field 'inSync' with a boolean value.

        """
        resource_path = 'items/' + str(item_id) + '/synceditems/' + str(synced_item_id) + '/syncstatus'
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_pick_lists(self):
        """
        Returns a list of all the pick lists

        Returns: an array of dictionary objects

        """
        resource_path = 'picklists/'
        pick_lists = self.__get_all(resource_path)
        return pick_lists

    def get_pick_list(self, pick_list_id):
        """
        Gets all a singular picklist

        Args:
            pick_list_id: The API id of the pick list to fetch

        Returns: a dictionary object representing the picklist.

        """
        resource_path = 'picklists/' + str(pick_list_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_pick_list_options(self, pick_list_id):
        """
        Gets all all the picklist options for a single picklist
        Args:
            pick_list_id: the api id of the picklist to fetch options for.

        Returns: an array of dictionary objects that represent the picklist options.

        """
        resource_path = 'picklists/' + str(pick_list_id) + '/options'
        pick_list_options = self.__get_all(resource_path)
        return pick_list_options

    def get_pick_list_option(self, pick_list_option_id):
        """
        Fetches a single picklist option from the API
        Args:
            pick_list_option_id: The API ID of the picklist option to fetch

        Returns: A dictonary object representing the picklist option.

        """
        resource_path = 'picklistoptions/' + str(pick_list_option_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_relationships(self, project_id):
        """
        Returns a list of all relationships of a specified project

        Args:
            project_id: the api project id of a project

        Returns: a list of dictionary objects that represents a relationships

        """
        resource_path = 'relationships'
        params = {'project': project_id}
        relationship_data = self.__get_all(resource_path, params=params)
        return relationship_data

    def get_relationship(self, relationship_id):
        """
        Returns a specific relationship object of a specified relationship ID

        Args:
            relationship_id: the api project id of a relationship

        Returns: a dictionary object that represents a relationship

        """
        resource_path = 'relationships/' + str(relationship_id)
        response = self.__core.get(resource_path)
        JamaClient.__handle_response_status(response)
        return response.json()['data']

    def get_abstract_items(self,
                           project=None,
                           item_type=None,
                           document_key=None,
                           release=None,
                           created_date=None,
                           modified_date=None,
                           last_activity_date=None,
                           contains=None,
                           sort_by=None):
        """
        This method will return all items that match the query parameters entered.

        Args:
            project:            Array[integer]
            item_type:          Array[integer]
            document_key:       Array[string]
            release:            Array[integer]
            created_date:       Array[string]
            modified_date:      Array[string]
            last_activity_date: Array[string]
            contains:           Array[string]
            sort_by:            Array[string]

        Returns:
            A JSON Array of items.

        """
        resource_path = 'abstractitems'

        # Add each parameter that is not null to the request.
        params = {}

        if project is not None:
            params['project'] = project

        if item_type is not None:
            params['itemType'] = item_type

        if document_key is not None:
            params['documentKey'] = document_key

        if release is not None:
            params['release'] = release

        if created_date is not None:
            params['createdDate'] = created_date

        if modified_date is not None:
            params['modifiedDate'] = modified_date

        if last_activity_date is not None:
            params['lastActivityDate'] = last_activity_date

        if contains is not None:
            params['contains'] = contains

        if sort_by is not None:
            params['sortBy'] = sort_by

        abstract_items = self.__get_all(resource_path, params=params)
        return abstract_items

    def get_item_children(self, item_id):
        """
        This method will return list of the child items of the item passed to the function.
        Args:
            item_id: (int) The id of the item for which children items should be fetched

        Returns: a List of Objects that represent the children of the item passed in.
        """
        resource_path = 'items/' + str(item_id) + '/children'
        child_items = self.__get_all(resource_path)
        return child_items

    def get_testruns(self, test_cycle_id):
        """This method will return all test runs associated with the specified test cycle.  Test runs will be returned
        as a list of json objects."""
        resource_path = 'testcycles/' + str(test_cycle_id) + '/testruns'
        testrun_data = self.__get_all(resource_path)
        return testrun_data

    def get_items_upstream_relationships(self, item_id):
        """
        Returns a list of all the upstream relationships for the item with the specified ID.
        Args:
            item_id: the api id of the item

        Returns: an array of dictionary objects that represent the upstream relationships for the item.

        """
        resource_path = 'items/' + str(item_id) + '/upstreamrelationships'
        return self.__get_all(resource_path)

    def get_items_downstream_relationships(self, item_id):
        """
        Returns a list of all the downstream relationships for the item with the specified ID.

        Args:
            item_id: the api id of the item

        Returns: an array of dictionary objects that represent the downstream relationships for the item.

        """
        resource_path = 'items/' + str(item_id) + '/downstreamrelationships'
        return self.__get_all(resource_path)

    def get_tags(self, project):
        """
        Get all tags for the project with the specified id
        Args:
            project: The API ID of the project to fetch tags for.

        Returns: A Json Array that contains all the tag data for the specified project.

        """
        resource_path = 'tags'
        params = {'project': project}
        tag_data = self.__get_all(resource_path, params=params)
        return tag_data

    def get_test_cycle(self, test_cycle_id):
        """
        This method will return JSON data about the test cycle specified by the test cycle id.

        Args:
            test_cycle_id: the api id of the test cycle to fetch

        Returns: a dictionary object that represents the test cycle

        """
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

    def delete_relationships(self, relationship_id):
        """
        Deletes a relationship with the specified relationship ID

        Args:
            relationship_id: the api project id of a relationship

        Returns: The success status code.

        """
        resource_path = 'relationships/' + str(relationship_id)
        response = self.__core.delete(resource_path)
        JamaClient.__handle_response_status(response)
        return response.status_code

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

    def post_tag(self, name: str, project: int):
        """
        Create a new tag in the project with the specified ID
        Args:
            name: The display name for the tag
            project: The project to create the new tag in

        Returns: The integer API ID fr the newly created Tag.
        """
        resource_path = 'tags'
        body = {
            'name': name,
            'project': project
        }
        headers = {'content-type': 'application/json'}
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)
        JamaClient.__handle_response_status(response)
        return response.json()['meta']['id']

    def post_testplans_testcycles(self, testplan_id, testcycle_name, start_date, end_date, testgroups_to_include=None,
                                  testrun_status_to_include=None):
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

    def post_item_tag(self, item_id, tag_id):
        """
        Add an existing tag to the item with the specified ID
        Args:
            item_id: The API ID of the item to add a tag.
            tag_id: The API ID of the tag to add to the item.

        Returns: 201 if successful

        """
        body = {
            "tag": tag_id
        }
        resource_path = 'items/' + str(item_id) + '/tags'
        headers = {'content-type': 'application/json'}
        response = self.__core.post(resource_path, data=json.dumps(body), headers=headers)
        JamaClient.__handle_response_status(response)
        return response.status_code

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

    def put_item(self, project, item_id, item_type_id, child_item_type_id, location, fields):
        """ This method wil
         PUT a new item to Jama Connect.
        :param project integer representing the project to which this item is to be posted
        :param item_id integer representing the item which is to be updated
        :param item_type_id integer ID of an Item Type.
        :param child_item_type_id integer ID of an Item Type.
        :param location dictionary  with a key of 'item' or 'project' and an value with the ID of the parent
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
        resource_path = 'items/' + str(item_id)
        headers = {'content-type': 'application/json'}
        response = self.__core.put(resource_path, data=json.dumps(body), headers=headers)
        return self.__handle_response_status(response)

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
        """This method will get all of the resources specified by the resource parameter, if an id or some other
        parameter is required for the resource, include it in the params parameter.
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

            response_message = 'None'

            try:
                response_json = json.loads(response.text)
                response_message = response_json.get('meta').get('message')

            except json.JSONDecodeError:
                pass

            # Log the error
            py_jama_rest_client_logger.error('API Client Error. Status: {} Message: {}'.format(status,
                                                                                               response_message))

            if "already exists" in response_message:
                raise AlreadyExistsException("Entity already exists.",
                                             status_code=status,
                                             reason=response_message)

            if status == 401:
                raise UnauthorizedException("Unauthorized: check credentials and permissions.  "
                                            "API response message {}".format(response_message),
                                            status_code=status,
                                            reason=response_message)

            if status == 404:
                raise ResourceNotFoundException("Resource not found. check host url.",
                                                status_code=status,
                                                reason=response_message)

            if status == 429:
                raise TooManyRequestsException("Too many requests.  API throttling limit reached, or system under "
                                               "maintenance.",
                                               status_code=status,
                                               reason=response_message)

            raise APIClientException("{} {} Client Error.  Bad Request.  "
                                     "API response message: {}".format(status, response.reason, response_message),
                                     status_code=status,
                                     reason=response_message)

        if status in range(500, 600):
            """These are server errors and network errors."""

            # Log The Error
            py_jama_rest_client_logger.error('{} Server error. {}'.format(status, response.reason))
            raise APIServerException("{} Server Error.".format(status),
                                     status_code=status,
                                     reason=response.reason)

        # Catch anything unexpected
        py_jama_rest_client_logger.error('{} error. {}'.format(status, response.reason))
        raise APIException("{} error".format(status),
                           status_code=status,
                           reason=response.reason)

