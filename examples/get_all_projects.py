import os
from py_jama_rest_client.client import JamaClient

# Setup your Jama instance url, username, and password.
# You may use environment variables, or enter your information directly.
# Reminder: Follow your companies security policies for storing passwords.
jama_url = os.environ['JAMA_API_URL']
jama_api_username = os.environ['JAMA_API_USERNAME']
jama_api_password = os.environ['JAMA_API_PASSWORD']

# Create the JamaClient
jama_client = JamaClient(host_domain=jama_url, credentials=(jama_api_username, jama_api_password))

# Get the list of projects from Jama
# The client will return to us a JSON array of Projects, where each project is a JSON object.
project_list = jama_client.get_projects()

#

# Print the data out for each project.
for project in project_list:
    project_name = project['fields']['name']
    print('\n---------------' + project_name + '---------------')

    # Print each field
    for field_name, field_data in project.items():

        # If one of the fields(i.e. "fields") is a dictionary then print it's sub fields indented.
        if isinstance(field_data, dict):
            print(field_name + ':')
            # Print each sub field
            for sub_field_name in field_data:
                sub_field_data = field_data[sub_field_name]
                print('\t' + sub_field_name + ': ' + str(sub_field_data))

        # If this field is not a dictionary just print its field.
        else:
            print(field_name + ': ' + str(field_data))

