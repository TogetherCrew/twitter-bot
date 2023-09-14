import logging
import time
from typing import Any
import functools

from redis import Redis
from rq import Queue as RQ_Queue

from tc_messageBroker.message_broker import RabbitMQ
from tc_messageBroker.rabbit_mq.queue import Queue
from tc_messageBroker.rabbit_mq.event import Event

from bot.utils.rabbitmq_connection import get_rabbit_mq_credentials
from bot.utils.redis_connection import get_redis_credentials

from bot.saga.extract_tweets import find_saga_and_fire_extract_tweets
from bot.saga.extract_profiles import find_saga_and_fire_extract_profiles
from bot.saga.extract_likes import find_saga_and_fire_extract_likes

from bot.saga.saga import publish_on_success

def twitter_bot():
    rabbit_mq_creds = get_rabbit_mq_credentials()
    redis_creds = get_redis_credentials()

    rabbit_mq = RabbitMQ(
        broker_url=rabbit_mq_creds["broker_url"],
        port=rabbit_mq_creds["port"],
        username=rabbit_mq_creds["username"],
        password=rabbit_mq_creds["password"],
    )

    redis = Redis(
        host=redis_creds["host"],
        port=redis_creds["port"],
        password=redis_creds["pass"],
    )

    # 24 hours equal to 86400 seconds
    rq_queue = RQ_Queue(connection=redis, default_timeout=86400)

    on_tweets_event_bind = functools.partial(
        on_tweets_event, redis_queue=rq_queue,
    )

    on_profiles_event_bind = functools.partial(
        on_profiles_event, redis_creds=rq_queue,
    )

    on_likes_event_bind = functools.partial(
        on_likes_event, redis_creds=rq_queue,
    )

    rabbit_mq.connect(queue_name=Queue.TWITTER_BOT)

    rabbit_mq.on_event(Event.TWITTER_BOT.EXTRACT.TWEETS, on_tweets_event_bind)
    rabbit_mq.on_event(Event.TWITTER_BOT.EXTRACT.PROFILES, on_profiles_event_bind)
    rabbit_mq.on_event(Event.TWITTER_BOT.EXTRACT.LIKES, on_likes_event_bind)

    if rabbit_mq.channel is None:
        logging.info("Error: was not connected to RabbitMQ broker!")
    else:
        time.sleep(3)
        rabbit_mq.publish(queue_name= Queue.TWITTER_BOT, event= Event.TWITTER_BOT.EXTRACT.TWEETS, content= { "uuid": "asdf-sdf", "username": "cyri113" })
        
        logging.info("Started Consuming!")
        rabbit_mq.channel.start_consuming()


def on_tweets_event(body: dict[str, Any], redis_queue: RQ_Queue):
    sagaId = body["content"]["uuid"]
    logging.info(f"SAGAID:{sagaId} recompute job Adding to queue")
 
    redis_queue.enqueue(
        find_saga_and_fire_extract_tweets,
        sagaId=sagaId,
        on_success=publish_on_success
    )


def on_profiles_event(body: dict[str, Any], redis_queue: RQ_Queue):
    sagaId = body["content"]["uuid"]
    logging.info(f"SAGAID:{sagaId} recompute job Adding to queue")
 
    redis_queue.enqueue(
        find_saga_and_fire_extract_profiles,
        sagaId=sagaId,
        on_success=publish_on_success
    )


def on_likes_event(body: dict[str, Any], redis_queue: RQ_Queue):
    sagaId = body["content"]["uuid"]
    logging.info(f"SAGAID:{sagaId} recompute job Adding to queue")
 
    redis_queue.enqueue(
        find_saga_and_fire_extract_likes,
        sagaId=sagaId,
        on_success=publish_on_success
    )


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    twitter_bot()



