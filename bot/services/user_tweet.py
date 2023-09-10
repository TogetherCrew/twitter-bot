import tweepy

from .tweeter_client import tweeter_client
from .utils import retry_function_if_fail, tweet_fields, max_tweet_results

from itertools import count

def get_user_tweets(user_handler: str, since_id: str) -> list[tweepy.Tweet]:
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

    query = f"from:{user_handler}"

    all_tweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        tweets = retry_function_if_fail(
            tweeter_client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_tweet_results,
            since_id=since_id,
            next_token=next_token,
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


def get_mentioned_tweets_by_username(
    username: str, since_id: str
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

    query = f"@{username}"
    print(query)

    all_tweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        tweets = retry_function_if_fail(
            tweeter_client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_tweet_results,
            since_id=since_id,
            next_token=next_token,
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
