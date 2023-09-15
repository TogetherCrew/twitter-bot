import os

from dotenv import load_dotenv


def get_redis_credentials():
    """
    get redis credentials
    """
    load_dotenv()

    redis_creds = {}

    redis_creds["host"] = os.getenv("REDIS_HOST")
    redis_creds["port"] = os.getenv("REDIS_PORT")
    redis_creds["pass"] = os.getenv("REDIS_PASSWORD")

    return redis_creds
