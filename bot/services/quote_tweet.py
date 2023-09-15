from itertools import count

import tweepy

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_quotes_of_tweet(tweet_id: str, since_id: str | None) -> list[tweepy.Tweet]:
    """
    Get all quotes of a tweet.

    Parameters:
    ------------
    tweet_id : str | int
        given the tweetID, find the all quotes
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all Quote Tweets in last 7 days will be returned
    """

    query = f"quotes_of_tweet_id:{tweet_id}"

    all_quotes: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        tweets = retry_function_if_fail(
            TwitterClient.client.search_recent_tweets,
            query=query,
            tweet_fields=FetchConfigs.tweet_fields,
            max_results=FetchConfigs.max_tweet_results,
            since_id=since_id,
            next_token=next_token,
        )
        quote_list = tweets.data
        tweets_meta = tweets.meta

        quote_list = quote_list if quote_list is not None else []
        all_quotes += quote_list

        if "next_token" not in tweets_meta:
            # when we don't have "next_token" in meta object, there is no more data
            break
        else:
            next_token = tweets_meta["next_token"]

    return all_quotes
