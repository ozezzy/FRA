# FRP 
[![codecov](https://codecov.io/gh/ozezzy/FRA/branch/master/graph/badge.svg)](https://codecov.io/gh/ozezzy/FRA)
[![Build Status](https://travis-ci.org/ozezzy/FRA.svg?branch=master)](https://travis-ci.org/ozezzy/FRA)

Feature Request App is a simple Flask, SQLAlchemy and Bootstrap application that enables users to capture Feature requests from clients and prioritize them.

Features
- A user with credentials can login.
- Logged in user fill and submit the feature request form.
- Logged in user can view current feature requests.
- If an already assigned priority is chosen for a new feature, existing request priorities are re-ordered 

#### Technologies

- Python 3.7
- Flask
- SQLAlchemy
- Jquery
- Bootstrap

#### Hosted at
The app is hosted at http://35.237.45.209/

## Deployment:

clone repo and cd into the directory

`git clone https://github.com/ozezzy/FRA`

`cd FRA`

change the value of `SQLALCHEMY_DATABASE_URI` in `config.py` to URI of DB you would like to use.
If not changed, the app will deploy successfully using SQLite but you will not be able to create features
run deploy script.

Note: the app is tested with Postgres, will work with any database but the driver requirement will need to be added to requirements.txt

#### `sudo ./deploy.sh`

Wait till you see "Deployment COMPLETE" and you are good to go.

(Deployment script tested on ubuntu16 and ubuntu18)



## Dev Setup

clone repo and cd into the directory

`git clone https://github.com/ozezzy/FRA`

and checkout development branch

#### install dependencies

 `pip install -r requirements.txt`

#### serve in development environment

run `python seed.py && python app.py `

##### Testing with coverage data

`coverage run test.py && coverage report FRA/*.py`

#### AUTHOR
Godswill 
