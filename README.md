# Twitter Bot

[![Maintainability](https://api.codeclimate.com/v1/badges/639841a044d5a068ede1/maintainability)](https://codeclimate.com/github/TogetherCrew/twitter-bot/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/639841a044d5a068ede1/test_coverage)](https://codeclimate.com/github/TogetherCrew/twitter-bot/test_coverage)

## Description

This repository contains an application that extracts data from Twitter based on many factors and saves it into a Neo4j graph database.
The application can be used to collect a wide range of data, including tweets, users, hashtags, and relationships between them.
Once the data has been extracted, it can be used to perform a variety of analyses, such as Account overview, your account activity, audience response, and engagement by account.

## Installation

To install the required dependencies run

```bash
pip install -r requirements.txt
```
## Running the CLI

To run the CLI, make sure you have configure your environment variables (see [.env.example](https://github.com/TogetherCrew/twitter-bot/blob/main/.env.example)).

Twitter-Bot requires Redis and Neo4j. If you don't have Redis and Neo4j instances running already, you can launch them using:

```bash
docker-compose -f docker-compose.dev.yml up
```

Execute the following command from the root directory of the application:

```bash
python3 cli.py [twitter-username]
```

Note: Make sure your have run the installation command.

## Environment variables

Add your environmental variables in `.env.example`. Rename it to `.env`. 

- Neo4j: Data about nodes and their relationships (edges) are stored in neo4j
- Twitter api: access to twitter's API to extract the data. Go to developers.twitter.com and create your account
- RabbitMQ: This is used for queuing of external tasks
- Reddis: This is used for queuing of internal tasks
- MongoDB: This is used to store the computed metrics


## Running the app

```bash
# Run the server 
python server.py

# Run the worker
python worker.py
```

You can quickly launch the application using `Docker Compose`:

```bash
docker-compose -f docker-compose.example.yml up
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
