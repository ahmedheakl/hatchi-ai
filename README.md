![tests](https://github.com/ahmedheakl/hatchi/workflows/test/badge.svg)
# Hatchi: Smart Database Interface Dashboard for Querying numerous Data Sources.

The project is developed with the motivation to obstain from writing boilerplate code and focusing on designing machine learning models and pipelines. We are currently targeting three main features: 

- Text-based query to get insights from any data source (SQL, no-SQL, CSV, parquert, feather ... etc)
- Drag and drop pre-processing pipeline GUI
- Drag and drop ML/DL models GUI


> **Note: This project is under active development**


## How to contribute

### As a library maintainer
Start by cloning the project into your local, and creating your virtual environemnt. 

```bash
$ sudo apt-get update # update current packages
$ sudo apt-get install -y virtualenv python3-virtualenv # install python virtualenv
$ virtualenv ~/hatchivenv --python=python3.8 # create dronevis virtual env
$ source ~/hatchivenv/bin/activate # activate virtualenv
```


Installing the requriments:

```bash
(.hatchivenv) $ pip install -r requirements.txt
```

Create a new local branch for your modifications, and start developing. After you're done, push the code to the remote origin, and create your pull request, and we will take it from there :)
