# Ody API

A simple Flask API to manage job applications.

## Installation

### Database initialization

Install psql if necessary, then in the psql console, run:

```
CREATE DATABASE ody_db;
CREATE USER <username> WITH PASSWORD <password>;
GRANT ALL PRIVILEGES ON DATABASE ody_db TO <username>;
ALTER  DATABASE  ody_db OWNER TO <username>;
```

Then, set as SQLALCHEMY_DATABASE_URI:

```
postgresql://<username>:<password>@localhost/ody_db
```

### Setting up the app

Set up a virtual environment using:

```
python -m venv env
source env/bin/activate # to activate the venv
```

Then install dependencies:

```
pip install -r requirements.txt
```

## Running the API

First, don't forget to run the migrations to create and update necessary tables, via:

```
flask db init
flask db upgrade
```

Before starting the app, set the ENV variable manually:

```
export FLASK_ENV=development
```

Then, simply run:

```
flask run
```

If you'd like to activate the debugger in dev mode (recommended while developping locally):

```
flask run --debug
```

## Running tests

Simply run `pytest` to run all tests:

```
pytest
```

(or FLASK_ENV=testing pytest depending on how you set up FLASK_ENV)
