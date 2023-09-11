from itertools import count

import tweepy

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_liked_tweets(user_id: str) -> list[tweepy.Tweet]:
    all_tweets: list[tweepy.Tweet] = []
    next_token = None

    for _ in count(1):
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

    return all_tweets


def get_likers_of_tweet(tweet_id: str) -> list[tweepy.User]:
    all_liker_users: list[tweepy.User] = []
    next_token = None
    for _ in count(1):
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

    return all_liker_users
