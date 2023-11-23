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

## Run the API

First, don't forget to run the migrations to create and update necessary tables, via:

```
flask db init
flask db upgrade
```

To start the app, simple run:

```
flask run
```

## Running tests

Make sure you have pytest installed first.

```
pip install pytest
```

then simply run `pytest` to run all tests:

```
pytest
```
