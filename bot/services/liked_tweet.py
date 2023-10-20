from itertools import count

import tweepy
import logging

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_liked_tweets(user_id: str) -> list[tweepy.Tweet]:
    logging.info(
        f"Start fetching `Tweets` that a user with ID {user_id} liked, It might take long (because of twitter api limits)"
    )
    all_tweets: list[tweepy.Tweet] = []
    next_token = None

    for _ in count(1):
        logging.info(f"[LIKED_TWEET] Gathering data for the {_}st round")
        tweets = retry_function_if_fail(
            TwitterClient.client.get_liked_tweets,
            id=user_id,
            tweet_fields=FetchConfigs.tweet_fields,
            max_results=FetchConfigs.max_tweet_results,
            pagination_token=next_token,
        )
        tweets_list = tweets.data
        tweets_meta = tweets.meta

        tweets_list = tweets_list if tweets_list is not None else []
        all_tweets += tweets_list

        if "next_token" not in tweets_meta:
            # when we don't have "next_token" in meta object, there is no more data
            break
        else:
            next_token = tweets_meta["next_token"]

    logging.info(f"All `Tweets` that the user with ID {user_id} liked were fetched")
    return all_tweets


def get_liked_tweets_since(user_id: str, since: int | None = None):
    logging.info(f"Start fetching `Tweets` that a user with ID {user_id} liked")
    all_tweets: list[tweepy.Tweet] = []
    next_token = None

    for _ in count(1):
        logging.info(f"[USER_LIKED_TWEET] Gathering data for the {_}st round")
        tweets, tweets_meta = fetch_liked_tweets(user_id, next_token)
        all_tweets += tweets

        if since and any(
            tweet.created_at.timestamp() * 1000 < since for tweet in tweets
        ):
            break

        if "next_token" not in tweets_meta:
            # when we don't have "next_token" in meta object, there is no more data
            break
        else:
            next_token = tweets_meta["next_token"]

    logging.info(f"All `Tweets` that the user with ID {user_id} liked were fetched")
    return all_tweets


def get_likers_of_tweet(tweet_id: str) -> list[tweepy.User]:
    logging.info(f"Start fetching `ّUsers` that liked a tweet with ID {tweet_id}")
    all_liker_users: list[tweepy.User] = []
    next_token = None

    for _ in count(1):
        logging.info(f"[TWEET_LIKER_USER] Gathering data for the {_}st round")
        users = retry_function_if_fail(
            TwitterClient.client.get_liking_users,
            id=tweet_id,
            max_results=FetchConfigs.max_like_results,
            pagination_token=next_token,
            user_fields=FetchConfigs.user_fields,
        )
        users_list = users.data
        users_meta = users.meta

        users_list = users_list if users_list is not None else []
        all_liker_users += users_list

        if "next_token" not in users_meta:
            # when we don't have "next_token" in meta object, there is no more data
            break
        else:
            next_token = users_meta["next_token"]

    logging.info(f"All `Users` that liked the tweet with ID {tweet_id} were fetched")
    return all_liker_users


def fetch_liked_tweets(user_id, next_token):
    max_results = FetchConfigs.max_tweet_results
    tweets = TwitterClient.client.get_liked_tweets(
        id=user_id,
        tweet_fields=FetchConfigs.tweet_fields,
        max_results=max_results,
        pagination_token=next_token,
    )

    tweets_meta = tweets.meta
    tweets_list = tweets.data or []

    return tweets_list, tweets_meta
