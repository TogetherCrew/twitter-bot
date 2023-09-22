import logging

from bot.services.user_info import get_twitter_user
from bot.twitter import extract_and_save_liked_tweets, extract_and_save_liker_users
from bot.utils.mongo_connection import get_saga_db_location
from bot.saga.saga import get_saga_instance


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
        twitter_user = get_twitter_user(username=twitter_username)
        twitter_id = twitter_user.id

        def extract_and_save_likes_information_wrapper(**kwargs):
            extract_and_save_liker_users(user_id=twitter_id)
            extract_and_save_liked_tweets(user_id=twitter_id)

        def publish_wrapper(**kwargs):
            pass

        saga.next(
            publish_method=publish_wrapper,
            call_function=extract_and_save_likes_information_wrapper,
            mongo_creds=saga_mongo_creds,
        )

    return sagaId, saga_mongo_creds
