# Contributors Guide

## Adding New Endpoints
If you would like to contribute additional endpoint please do the following:
1) Write the endpoint code in client.py following the syntax swagger uses for paramaters.
2) Write some tests to show the endpoint works like expected
3) Update the readme with the added endpoints
4) Submit a pull request

## Updating documentation
Use pdoc to build HTML documentation from Docstrings with the following command:

`pdoc --html py_jama_rest_client --html-dir docs --overwrite`

## Create a new version and upload to PyPi
The general process for creating a release and uploading it to pypi can be found here: 
https://packaging.python.org/tutorials/packaging-projects/

1) Open `setup.py` and edit the version string to reflect the next desired release number.  

2) Generate the distribution archives
    1) open a terminal to the root of the project
    2) Generate the distribution archive with the command 
    
        `python3 setup.py sdist bdist_wheel`

3) Upload the distribution archive
    1) `python3 -m twine upload dist/*`
