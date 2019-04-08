# Contributors Guide

# Create a new version and upload to PyPi
The general process for creating a relase and uploading it to pypi can be found here: 
https://packaging.python.org/tutorials/packaging-projects/

1) Open `setup.py` and edit the version string to reflect the next desired release number.  

2) Generate the distribution archives
    1) open a terminal to the root of the project
    2) Generate the distribution archive with the command `python3 setup.py sdist bdist_wheel`

3) Upload the distribution archive
    1) `python3 -m twine upload dist/*`
