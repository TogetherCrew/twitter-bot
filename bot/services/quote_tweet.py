import tweepy

from .tweeter_client import tweeter_client
from .utils import retry_function_if_fail, tweet_fields, max_tweet_results

from itertools import count

def get_quotes_of_tweet(tweet_id: str, since_id: str) -> list[tweepy.Tweet]:
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
            tweeter_client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_tweet_results,
            since_id=since_id,
            next_token=next_token,
        )
        quote_list = tweets.data
        tweets_meta = tweets.meta

        quote_list = quote_list if quote_list is not None else []
        all_quotes += quote_list

        if not "next_token" in tweets_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = tweets_meta["next_token"]

    return all_quotes

