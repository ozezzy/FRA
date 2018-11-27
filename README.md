# FRP 
[![codecov](https://codecov.io/gh/ozezzy/FRA/branch/master/graph/badge.svg)](https://codecov.io/gh/ozezzy/FRA)

Feature Request App is a simple Flask, SQLAlchemy, Bootstrap application that ebables users to capture Feature requests from client, and prioritise them.

Features
- User with credentials can login.
- Logged in user fill and submit feature request form.
- Logged in user can view current feature requests.
- If an already assigned priority is chosen for a new feature, existing request priorities are re-ordered 

# Technologies

- Python 3.7
- Flask
- SQLAlchemy
- Jquery
- Bootstrap

#Hosted at
App is hosted at https://my-feature-request.herokuapp.com

## Build Setup

clone repo and cd into directory

`git clone https://github.com/ozezzy/FRA`

# install dependencies

 `pip install -r requirements.txt`

# serve in development environment

run `python seed.py && python app.py `

## Testing

Testing with coverage data

`coverage run test.py && coverage report FRA/*.py`

## AUTHOR
Godswill 
