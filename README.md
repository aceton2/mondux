# Mondu X

Simple Flask app created for _Mondu Coding Challenge_.

It runs in a docker container exposed on localhost port 5000It implements the 4 required endpoints

● Create an account
● Deposit money on a specific account
● Withdraw money from a specific account
● Get balance of a specific account

### Context

This was my first time writing a backend in `python` (my experience with python is mostly script-based). Luckily I found the `Flask` official documentation well written so the proccess was quite enjoyable. My implementation here is based pretty much straight from the `Quickstart` and `Tutorial` sections, though I wrote the actual code making sure to only include what I found neccesary.

## Quickstart
### Dev Server
To get the app up and running,

```shell
docker-compose -f dc-canon.yaml -f dc-dev.yaml up
```
This will start 2 containers. One running a `postgres` database , and a second container running the flask application via the `Werkzeug` development server.

A simple landing page can be checked to verify the api is reachable and functional.
``` 
http://localhost:5000/ 
```

### Testing

Two types of tests are implemeneted. Unit tests (`app/tests/test_unit_business.py`) as well as functional test (`app/tests/tests_api.py`). Given that the functional tests make connections to the database, it is neccesary to start up a postgres container for these.

``` shell
docker-compose -f dc-canon.yaml -f dc-test.yaml up
```

This command will handle the neccesary container setup, init a _temporary_ postgres database, run existing tests, and print coverage to the console.

Note: after the tests have run the database container will still be running. You will need to run ```docker-compose down``` to clean up. This is not ideal and should be refactored.

## Description
### Stack
For this challenge I chose Flask because 1) my familiarity with python vs go or ruby 2) Flask is lightweight and relatively simple to get started with, making it a good fit for a challenge like this.

Rather then using mysqlite3 as in the official tutorials I chose postgres as a backend since it is a more realistic database for banking.

On the other hand, for simplicities sake, I implemented `psycopg2` directly, rather than using a ORM like `SQLAlchemy`. This would possibly change in further development.

### App Architecture
Seperation of concerns here is simple: a controller layer, and a business logic layer, a database connection layer. In the case of this app these are represented by single classes

Controller - `accounts.py` which binds into the main app as a `Blueprint`
Business - `business.py` which is responsible for the business logic regarding accounts
Database - `db_connect.py` which handles requests to the database

Note: Queries are written directly in the `db_connect` class. In subsequent developements this would be refactored.

##### Database

The database contains a single table `accounts`. Fields are `id`, `account_number`, `balance_cents`. A minimal setup for the requested functionality.

Note: balance is in cents to avoid floating points.

### Docker

The image used for the Flask application is built on `python:3.6-slim` and subsequently installs python dependencies for this project via `requirements.txt`. One additional dependency is installed: `netcat` to handle scanning for the `postgres` service before starting the web app.

Since development was exclusively in containers, for flexibility I implemented an `extends` pattern allowing for different setups when running the containers.

##### Tests
For example, a volume is mounted in the `dc-dev` config but not in the `dc-test` config, meaning for tests the database is always in a virgin state and can be seeded accordingly.

Note: While writing tests I had the api command set to  `tail -f /dev/null` so that I could `docker exec` into the container and manually run tests as needed.

##### Database
Init of the database is handled by `db/init-user-db` which postgres runs when the database is first inited. This script creates at database for the app, as well as an app user. The variables for these are set in `api_database.env` which are passed into the container via docker-compose.

##### Deployment
Further steps here would be to create `db-prod.yaml`. For a local deployment this could spin up an additional `nginx` container pointing to the `web` service. The web service would run from a custom image (without the test libraries for example) and run the flask app behind a WSGI server like `gunicorn`.

## API Documentation
Responses are all in JSON format.

__Create Account__
_creates a new account_ 
```
/api/accounts/create
```
```
response: {
    balance: 0
}
```

__Deposit to Account__
_deposits transfer sum to the specified account and returns new balance_
```
/api/accounts/{account_number}/deposit?sum={transfer_sum}
```
```
response: {
    balance: 0
}
```
`account_number` __required__
`transfer_sum` __required__

__Withdraw from Account__
_withdraws transfer sum from the specified account and returns new balance_
```
/api/accounts/{account_number}/withdraw?sum={transfer_sum}
```
```
response: {
    balance: 10
}
```
`account_number` __required__
`transfer_sum` __required__

__Get Balance__
_returns balance for the specified account_
```
/api/accounts/{account_number}/balance
```
```
response: {
    balance: 10
}
```
`account_number` __required__

### Error handling

The API will explicitly return errors regarding non-existent accounts as `404`, and transfer sums that cannot be parsed to an integer as `400`. The response will return the corresponding error code, as well as a JSON with an error message.

```json
 {error: error message here}
```

If no account number is provided the API will return a `404` without additional error description.

# Open Issues

- Testing the database could be more thorough.
- ORM implementation is probably advised.
- Seperation of concerns: DB connect vs Query definitions.

