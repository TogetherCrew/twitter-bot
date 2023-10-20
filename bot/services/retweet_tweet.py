import logging
from itertools import count

import tweepy

from .twitter_client import TwitterClient
from .utils import FetchConfigs, retry_function_if_fail


def get_retweets_of_tweet(tweet_id: str, since_id: str | None) -> list[tweepy.Tweet]:
    """
    Get all retweets of a tweet.

    Parameters:
    ------------
    tweet_id : str | int
        given the tweetID, find the all retweets
    since_id :  str | None
        Returns results with a Tweet ID greater than (that is, more recent
        than) the specified ID. The ID specified is exclusive and responses
        will not include it.

    Returns:
    ---------
    all_tweets : list[tweepy.Tweet]
        all Retweet Tweets in last 7 days will be returned
    """
    logging.info(
        f"""Start fetching `Retweets` of a Tweet with ID {tweet_id}, 
        It might take long (because of twitter api limits)"""
    )
    query = f"retweets_of_tweet_id:{tweet_id}"

    all_retweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        logging.info(f"[RETWEETS] Gathering data for the {_}st round")
        tweets = retry_function_if_fail(
            TwitterClient.client.search_recent_tweets,
            query=query,
            tweet_fields=FetchConfigs.tweet_fields,
            max_results=FetchConfigs.max_tweet_results,
            since_id=since_id,
            next_token=next_token,
        )
        retweet_list = tweets.data
        tweets_meta = tweets.meta

        retweet_list = retweet_list if retweet_list is not None else []
        all_retweets += retweet_list

        if "next_token" not in tweets_meta:
            # when we don't have "next_token" in meta object, there is no more data
            break
        else:
            next_token = tweets_meta["next_token"]

    logging.info(f"All `Retweets` of the Tweet with ID {tweet_id} were fetched")
    return all_retweets
