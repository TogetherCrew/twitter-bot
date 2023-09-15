from typing import Any
import os

from dotenv import load_dotenv
from tc_messageBroker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue


def get_rabbit_mq_credentials() -> dict[str, Any]:
    """
    returns the rabbitMQ connection credentials

    Retuns:
    ----------
    rabbit_mq_creds : dict[str, Any]
        rabbitMQ credentials,
        a dictionary representive of
            `broker_url` : str
            `port` : int
            `username` : str
            `password` : str
    """
    load_dotenv()

    rabbit_mq_creds = {}

    rabbit_mq_creds["broker_url"] = os.getenv("RABBIT_HOST")
    rabbit_mq_creds["port"] = os.getenv("RABBIT_PORT")
    rabbit_mq_creds["password"] = os.getenv("RABBIT_PASSWORD")
    rabbit_mq_creds["username"] = os.getenv("RABBIT_USER")

    return rabbit_mq_creds


def prepare_rabbit_mq(rabbit_creds):
    rabbitmq = RabbitMQ(
        broker_url=rabbit_creds["broker_url"],
        port=rabbit_creds["port"],
        username=rabbit_creds["username"],
        password=rabbit_creds["password"],
    )
    rabbitmq.connect(queue_name=Queue.DISCORD_ANALYZER)

    return rabbitmq
