import logging

from saga import get_saga_instance
from bot.twitter import extract_and_save_liker_users, extract_and_save_liked_tweets

from tc_messageBroker.rabbit_mq.queue import Queue
from tc_messageBroker.rabbit_mq.event import Event

from bot.utils.mongo_connection import get_saga_db_location
from bot.utils.rabbitmq_connection import prepare_rabbit_mq

def find_saga_and_fire_extract_likes(sagaId: str):
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
        twitter_id = saga.data["twitter_id"]

        def extract_and_save_likes_information_wrapper(**kwargs):
            extract_and_save_liker_users(user_id= twitter_id)
            extract_and_save_liked_tweets(user_id= twitter_id)

        def publish_wrapper(**kwargs):
            pass

        saga.next(
            publish_method=publish_wrapper,
            call_function=extract_and_save_likes_information_wrapper,
            mongo_creds=saga_mongo_creds,
        )

    return sagaId, saga_mongo_creds
