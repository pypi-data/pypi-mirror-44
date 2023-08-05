# TMG ETL Library
**Authors**:  TMG Data team


This library is under development and it will contain all the functionalities need to interact with cloud and not cloud 
services allowing to develop more reliable and standard data pipelines.


## Overview

Work in progress, for now only a basic structure has been defined and needs team review.


## Using the TMG Pip Repository

#### Initial Setup
First Copy the below text to ~/.pypirc
```
[local]
username = username
password = password
repository = https://project.appspot.com

```
#### To Upload
```
python setup.py sdist upload -r local
``` 

#### To Clone
```
pip install -i https://tmg-plat-dev.appspot.com/pypi [package-name]
``` 