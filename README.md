# Jama Software
Jama Software is the definitive system of record and action for product development. The company’s modern requirements 
and test management solution helps enterprises accelerate development time, mitigate risk, slash complexity and verify 
regulatory compliance. More than 600 product-centric organizations, including NASA, Boeing and Caterpillar use Jama to 
modernize their process for bringing complex products to market. The venture-backed company is headquartered in 
Portland, Oregon. For more information, visit [jamasoftware.com](http://jamasoftware.com).

Please visit [dev.jamasoftware.com](http://dev.jamasoftware.com) for additional resources and join the discussion in our
 community [community.jamasoftware.com](http://community.jamasoftware.com).
 

# py-jama-rest-client
py-jama-rest-client by Jama Software is a Python REST API client for Jama Connect™.  The client will allow customers to 
easily access the REST API to retrieve, and modify data within their Jama Instance. 

Please note that this client is distributed as-is as an example and will likely require modification to work for your 
specific use-case.

## Requirements
- [Python 3.7](https://www.python.org/downloads/release/python-372/)
- [Pipenv(recommended)](https://pipenv.readthedocs.io/en/latest/)

## Setup
Create a new directory and install py-jama-rest-client using pipenv.
 ```bash
 mkdir example_project
 cd example_project
 pipenv --python 3.7
 pipenv install py-jama-rest-client
```

### REST Calls Supported in the Client

##### API information
- GET available endpoints

##### Abstract Items
- ~~GET abstract items by document key~~(Deprecated)
- GET abstract items(second method added to support all parameter options.  Previous method left to preserve backwards 
compatibility)

##### Attachments
- PUT attachment file, uploads content to an attachment object by attachmentID
- GET a specific attachment by ID

##### Items
- GET filter results, gets all results for the specified filter.

##### Items
- GET all items by project 
- GET a specific item by ID
- GET all downstream relationships for an item by item ID
- GET all upstream relationships for an item by item ID
- GET all children of an item
- GET all synced items
- GET synced item sync status
- GET Locked state of an item
- DELETE an Item by ID
- PATCH an Item
- POST an item to a project
- POST item attachment
- POST a tag to an item
- PUT an item
- PUT item lock

##### Relationship Types
- GET all relationship types
- GET a specific relationship type by ID

##### Item Types
- GET all item types
- GET a specific item type by ID

##### Pick lists
- GET all pick lists
- GET a specific pick list by ID
- GET all pick list options for a specific pick list by pick list ID

##### Pick list options
- GET a specific pick list option by pick list option ID

##### Projects: 
- GET all projects
- POST new attachment item

##### Tags
- GET all tags for a specific project
- POST a new tag to a specific project

##### Test Cycles
- GET test cycle by test cycle id

##### Test Plans
- POST a new test cycle to a test plan by test plan id

##### Test Runs
- GET all test runs associated with a particular test cycle id
- PUT test runs by id. Allows updating of test run fields.

##### Relationships
- POST relationship
- GET relationship by id
- GET relationships by project id
- DELETE relationship by id

## Usage Examples

#### Client instantiation
To instantiate a Basic authentication client:
```python

basic_auth_client = JamaClient('https://yourdomain.jamacloud.com', credentials=('username', 'password'))
```

To instantiate a OAuth authenticated client: 
```python
oauth_client = JamaClient('https://yourdomain.jamacloud.com', credentials=('clientID', 'ClientSecret'), oauth=True)
```


#### Logging
The Py Jama Rest Client will log API messages to the logger 'py_jama_rest_client' you can get this logger for 
setup / customization by calling `logging.getLogger('py_jama_rest_client')`


#### Get all projects
1) Download [get_all_projets.py](examples/get_all_projects.py) to your example_project directory
2) Enter your Jama URL, username, and password into the corrisponding variables at the top of the file.
3) To execute the script execute the following form your example_project directory: 
    ```bash
    pipenv run python get_all_projects.py
    ```

## Additional Documentation
https://jamasoftware.github.io/py-jama-rest-client/