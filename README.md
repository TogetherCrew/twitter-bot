# Twitter Bot

[![Maintainability](https://api.codeclimate.com/v1/badges/639841a044d5a068ede1/maintainability)](https://codeclimate.com/github/TogetherCrew/twitter-bot/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/639841a044d5a068ede1/test_coverage)](https://codeclimate.com/github/TogetherCrew/twitter-bot/test_coverage)

## Description

This repository contains an application that extracts data from Twitter based on many factors and saves it into a Neo4j graph database. 
The application can be used to collect a wide range of data, including tweets, users, hashtags, and relationships between them.
Once the data has been extracted, it can be used to perform a variety of analyses, such as Account overview, your account activity, audience response, and engagement by account.

## Installation

```bash
pip install -r requirements.txt
```

## Running the app

```
# Run the server 
python server.py

# Run the worker
python worker.py
```

You can quickly launch the application using `Docker Compose`:
```
docker-compose -f docker-compose.example.yml up
```

## Running the CLI

To run the CLI, execute the following command from the root directory of the application:
```
python3 cli.py [twitter-username]
```

## Tests

To run all of the tests in the application, simply run the following command:

```bash
pytest tests
```

To view the coverage report in HTML format, run the following commands:

```bash
python3 -m coverage run --omit="tests/*" -m pytest tests
python3 -m coverage html
```
