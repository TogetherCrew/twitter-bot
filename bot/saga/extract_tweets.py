from typing import Any
import logging

from saga import get_saga_instance
from bot.twitter import extract_and_save_tweets

from tc_messageBroker.rabbit_mq.queue import Queue
from tc_messageBroker.rabbit_mq.event import Event

from bot.utils.mongo_connection import get_saga_db_location
from bot.utils.rabbitmq_connection import prepare_rabbit_mq


def find_saga_and_fire_extract_tweets(sagaId: str):
    saga_mongo_creds = get_saga_db_location()

    saga = get_saga_instance(
        sagaId=sagaId,
        connection=saga_mongo_creds["connection_str"],
        saga_db=saga_mongo_creds["db_name"],
        saga_collection=saga_mongo_creds["collection_name"],
    )
    if saga is None:
        logging.warn(
            f"Warn: Saga not found!, stopping the recompute for sagaId: {sagaId}"
        )
    else:
        twitter_username = saga.data["twitter_username"]
        saga.data["counter"] = 0
        saga.data["twitter_id"] = 11166

        def extract_and_save_tweets_wrapper(**kwargs):
            extract_and_save_tweets(username=twitter_username)

        def publish_wrapper(**kwargs):
            pass

        saga.next(
            publish_method=publish_wrapper,
            call_function=extract_and_save_tweets_wrapper,
            mongo_creds=saga_mongo_creds,
        )

    return sagaId, saga_mongo_creds


def on_extract_tweets_success(connection, result, *args, **kwargs):
    # After this step, we will fire both the Like and Profile events simultaneously
    # So, I'll write custom on_success
    try:
        rabbit_creds = args[0][0]
        sagaId = args[0][1]
        mongo_creds = args[0][2]
        logging.info(f"SAGAID: {sagaId}: ON_SUCCESS callback! ")

        saga = get_saga_instance(
            sagaId=sagaId,
            connection=mongo_creds["connection_str"],
            saga_db=mongo_creds["db_name"],
            saga_collection=mongo_creds["collection_name"],
        )
        rabbitmq = prepare_rabbit_mq(rabbit_creds)

        rabbitmq.connect(Queue.TWITTER_BOT)
        logging.info(f"SAGAID: {sagaId}: Publishing for {Queue.TWITTER_BOT} onEvent {Event.TWITTER_BOT.EXTRACT.PROFILES}")
        logging.info(f"SAGAID: {sagaId}: Publishing for {Queue.TWITTER_BOT} onEvent {Event.TWITTER_BOT.EXTRACT.LIKES}")
        
        rabbitmq.publish(
            queue_name=Queue.TWITTER_BOT,
            event=Event.TWITTER_BOT.EXTRACT.PROFILES,
            content={"uuid": sagaId, "data": saga.data}
        )
        rabbitmq.publish(
            queue_name=Queue.TWITTER_BOT,
            event=Event.TWITTER_BOT.EXTRACT.LIKES,
            content={"uuid": sagaId, "data": saga.data}
        )
    except Exception as exp:
        logging.info(f"Exception occured in job on_success callback: {exp}")

