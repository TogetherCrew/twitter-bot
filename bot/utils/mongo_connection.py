import os
from typing import Any

from dotenv import load_dotenv


def get_mongo_credentials():
    """
    load mongo db credentials from .env

    Returns:
    ---------
    mongo_creds : dict[str, Any]
        mongodb credentials
        a dictionary representive of
            `user`: str
            `password` : str
            `host` : str
            `port` : int
    """
    load_dotenv()

    mongo_creds = {}

    mongo_creds["user"] = os.getenv("MONGODB_USER")
    mongo_creds["password"] = os.getenv("MONGODB_PASS")
    mongo_creds["host"] = os.getenv("MONGODB_HOST")
    mongo_creds["port"] = os.getenv("MONGODB_PORT")

    return mongo_creds

def get_mongo_connection(mongo_creds: dict[str, Any] | None = None) -> str:
    if mongo_creds is None: 
        mongo_creds = get_mongo_credentials()

    user = mongo_creds["user"]
    password = mongo_creds["password"]
    host = mongo_creds["host"]
    port = mongo_creds["port"]

    connection = f"mongodb://{user}:{password}@{host}:{port}"

    return connection

def get_saga_db_location(mongo_creds: dict[str, Any] | None = None):
    """
    get the saga location in database
    """
    if mongo_creds is None:
        mongo_creds = get_mongo_credentials()

    load_dotenv()

    saga_db = {}

    saga_db["db_name"] = os.getenv("SAGA_DB_NAME")
    saga_db["collection_name"] = os.getenv("SAGA_DB_COLLECTION")
    saga_db["connection_str"] = get_mongo_connection(mongo_creds)

    return saga_db
