import logging
from itertools import count

import tweepy

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_user_tweets(user_handler: str, since_id: str | None) -> list[tweepy.Tweet]:
    """
    To get the tweets of a user, get the user_handler

    Parameters:
    ------------
    user_handler : str | int
        given the user_handler, find the all related tweets
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all user's Tweets in last 7 days will be returned
    """
    logging.info(
        f"Start fetching `Tweets` of a User with ID/USERNAME {user_handler} , It might take long (because of twitter api limits)"
    )
    query = f"from:{user_handler}"

    all_tweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        logging.info(f"[TWEETS] Gathering data for the {_}st round")
        tweets = retry_function_if_fail(
            TwitterClient.client.search_recent_tweets,
            query=query,
            tweet_fields=FetchConfigs.tweet_fields,
            max_results=FetchConfigs.max_tweet_results,
            since_id=since_id,
            next_token=next_token,
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

    logging.info(
        f"All `Tweets` of the User with ID/USERNAME {user_handler} were fetched"
    )
    return all_tweets


def get_mentioned_tweets_by_username(
    username: str, since_id: str | None
) -> list[tweepy.Tweet]:
    """
    Get all tweets that user has mentioned.

    Parameters:
    ------------
    username : str | int
        given the tweetID, find the all retweets
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all Tweets that user has mentioned in last 7 days will be returned
    """
    logging.info(
        f"Start fetching `Mentioned Tweets` of a User with USERNAME {username} , It might take long (because of twitter api limits)"
    )
    query = f"@{username}"

    all_tweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        logging.info(f"[MENTIONED_TWEETS] Gathering data for the {_}st round")
        tweets = retry_function_if_fail(
            TwitterClient.client.search_recent_tweets,
            query=query,
            tweet_fields=FetchConfigs.tweet_fields,
            max_results=FetchConfigs.max_tweet_results,
            since_id=since_id,
            next_token=next_token,
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

    logging.info(
        f"All `Mentioned Tweets` of the User with USERNAME {username} were fetched"
    )
    return all_tweets
