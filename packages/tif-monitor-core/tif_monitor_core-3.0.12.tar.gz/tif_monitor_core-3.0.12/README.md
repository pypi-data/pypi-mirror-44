# monitor core package

####Deployment Instructions

The deployment is now automated in Jenkins. The only difference is that in the setup.py you need to update the version
number. 

Once the changes have been made and the version number updated, committing to the master branch will trigger Jenkins to 
build and save the changes [this url](https://pypipackages.tif-plc.eu/simple/)

More details about the monitor can be found on the [WIKI](http://devwiki.tif-it.co.uk/product-documentation/monitor/)

####Old Deployment Instructions
_A PyPi package. To publish a new version:_

* Create an account on pypi.org and ask Sam to add you to the project as a collaborator
* Install setuptools, wheel and twine - ** pip install --upgrade setuptools wheel twine **
* Increment the package version in setup.py
* Create package - ** python setup.py sdist bdist_wheel **
* Ensure that only your newly created package is in the dist directory (2 files). Delete any old packages.
* Upload package to pypi - ** twine upload dist/* **

Run ** pip install --upgrade monitor-core ** to install the latest version in your project