import tweepy

from .tweeter_client import tweeter_client
from .utils import retry_function_if_fail, tweet_fields, max_tweet_results

from itertools import count

def get_all_replies_of_tweet(tweet_id: str, since_id: str) -> list[tweepy.Tweet]:
    """
    Get all replies (all depth) of a tweet or Quote tweets. The array will be empty
    if retweetID or replyID is passed

    Parameters:
    ------------
    tweet_id : str | int
        given the tweetID, find the all replies
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all Reply Tweets in last 7 days will be returned
    """

    query = f"conversation_id:{tweet_id}"

    all_reply: list[tweepy.Tweet] = []
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
        reply_list = tweets.data
        tweets_meta = tweets.meta

        reply_list = reply_list if reply_list is not None else []
        all_reply += reply_list

        if not "next_token" in tweets_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = tweets_meta["next_token"]

    return all_reply


def get_first_depth_replies_of_tweet(
    tweet_id: str, since_id: str
) -> list[tweepy.Tweet]:
    """
    Get all replies (first depth) of a tweet.

    Parameters:
    ------------
    tweet_id : str | int
        given the tweetID, find the all replies
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all Reply Tweets in last 7 days will be returned
    """

    query = f"in_reply_to_tweet_id:{tweet_id}"

    all_reply: list[tweepy.Tweet] = []
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
        reply_list = tweets.data
        tweets_meta = tweets.meta

        reply_list = reply_list if reply_list is not None else []
        all_reply += reply_list

        if not "next_token" in tweets_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = tweets_meta["next_token"]

    return all_reply
