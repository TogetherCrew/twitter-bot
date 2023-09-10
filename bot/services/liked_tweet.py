import tweepy

from .tweeter_client import tweeter_client
from .utils import retry_function_if_fail, tweet_fields, max_tweet_results, user_fields, max_like_results

from itertools import count

def get_liked_tweets(user_id: str) -> list[tweepy.Tweet]:
    all_tweets: list[tweepy.Tweet] = []
    next_token = None

    for _ in count(1):
        tweets = retry_function_if_fail(
            tweeter_client.get_liked_tweets,
            id=user_id,
            tweet_fields=tweet_fields,
            max_results=max_tweet_results,
            pagination_token=next_token,
        )
        tweets_list = tweets.data
        tweets_meta = tweets.meta

        tweets_list = tweets_list if tweets_list is not None else []
        all_tweets += tweets_list

        if not "next_token" in tweets_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = tweets_meta["next_token"]

    return all_tweets


def get_likers_of_tweet(tweet_id: str) -> list[tweepy.User]:
    all_liker_users: list[tweepy.User] = []
    next_token = None
    for _ in count(1):
        users = retry_function_if_fail(
            tweeter_client.get_liking_users,
            id=tweet_id,
            max_results=max_like_results,
            pagination_token=next_token,
            user_fields=user_fields,
        )
        users_list = users.data
        users_meta = users.meta

        users_list = users_list if users_list is not None else []
        all_liker_users += users_list

        if not "next_token" in users_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = users_meta["next_token"]

    return all_liker_users

