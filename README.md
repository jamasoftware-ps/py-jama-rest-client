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
- Python 3.7
- Pipenv(recommended)

## Setup
Create a new directory and install py-jama-rest-client using pipenv.
 ```bash
 mkdir example_project
 cd example_project
 pipenv --python 3.7
 pipenv install py-jama-rest-client
```

### REST Calls Supported in the Client

##### Abstract Items
- GET abstract items by document key

##### Attachments
- PUT attachment file, uploads content to an attachment object by attachmentID

##### Projects: 
- GET all projects
- POST new attachment item

##### Items
- GET all items by project 
- POST an item to a project
- POST item attachment

##### Test Cycles
- GET test cycle by test cycle id

##### Test Plans
- POST a new test cycle to a test plan by test plan id

##### Test Runs
- GET all test runs associated with a particular test cycle id
- PUT test runs by id. Allows updating of test run fields.

## Usage Examples

#### Get all projects
1) Download [get_all_projets.py](examples/get_all_projects.py) to your example_project directory
2) Enter your Jama URL, username, and password into the corrisponding variables at the top of the file.
3) To execute the script execute the following form your example_project directory: 
    ```bash
    pipenv run python get_all_projects.py
    ```
