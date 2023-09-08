import functools
import logging
import os
from itertools import count
from dotenv import load_dotenv

import tweepy
from db.incomplete_profiles import get_incomplete_profile_ids
from db.latest_mention import get_latest_mention
from db.latest_quote import get_latest_quote
from db.latest_reply import get_latest_reply
from db.latest_retweet import get_latest_retweet
from db.latest_tweet import get_latest_tweet
from db.latest_tweet import get_days_ago_tweet_ids
from db.save_neo4j import save_tweets_in_neo4j, save_user_profile_neo4j, save_tweet_likes_neo4j



def retry_function_if_fail(func, /, *args, **keywords):
    retry_number = (
        keywords["retry_number"] if "retry_number" in keywords else 5
    )  # default retry number
    function = functools.partial(func, *args, **keywords)
    for counter in count(1):
        try:
            response = function()
            return response

        except Exception as ex:
            print("[Exception(retry_function_if_fail)]", ex)

        finally:
            if counter == retry_number:
                raise RuntimeError(
                    "Something went wrong when communicating with Twitter"
                )


load_dotenv()

# assign the values accordingly
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
print("consumer_key", consumer_key)
print("consumer_secret", consumer_secret)
print("bearer_token", bearer_token)
print("access_token", access_token)
print("access_token_secret", access_token_secret)

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True,
)

max_like_results = 10
max_tweet_results = 10
tweet_fields = [
    "id",
    "text",
    "entities",
    "created_at",
    "author_id",
    "conversation_id",
    "public_metrics",
    "referenced_tweets",
    "context_annotations",
    "in_reply_to_user_id",
]

user_fields = [
    "id",
    "name",
    "username",
    "created_at",
    "public_metrics",
    "description",
    "location",
    "profile_image_url",
    "protected",
    "url",
    "verified",
]


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
            client.search_recent_tweets,
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
            client.search_recent_tweets,
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
            client.search_recent_tweets,
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
            client.search_recent_tweets,
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


def get_retweets_of_tweet(tweet_id: str, since_id: str) -> list[tweepy.Tweet]:
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

    query = f"retweets_of_tweet_id:{tweet_id}"

    all_retweets: list[tweepy.Tweet] = []
    next_token = None
    for _ in count(1):
        tweets = retry_function_if_fail(
            client.search_recent_tweets,
            query=query,
            tweet_fields=tweet_fields,
            max_results=max_tweet_results,
            since_id=since_id,
            next_token=next_token,
        )
        retweet_list = tweets.data
        tweets_meta = tweets.meta

        retweet_list = retweet_list if retweet_list is not None else []
        all_retweets += retweet_list

        if not "next_token" in tweets_meta:
            break  # when we don't have "next_token" in meta object, there is no more data
        else:
            next_token = tweets_meta["next_token"]

    return all_retweets


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
            client.search_recent_tweets,
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


def get_liked_tweets(user_id: str):
    all_tweets: list[tweepy.Tweet] = []
    next_token = None
    
    for _ in count(1):
        tweets = retry_function_if_fail(
            client.get_liked_tweets,
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


def get_likers_of_tweet(tweet_id: str) -> list[tweepy.User]:
    all_liker_users: list[tweepy.User] = []
    next_token = None
    for _ in count(1):
        users = retry_function_if_fail(
            client.get_liking_users,
            id=tweet_id,
            max_results=max_like_results,
            pagination_token=next_token,
            user_fields=user_fields
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


def get_user(id=None, username=None) -> tweepy.User:
    if id is not None and username is not None:
        raise TypeError("Expected ID or username, not both")

    user = retry_function_if_fail(
        client.get_user,
        id=id,
        username=username,
        user_fields=user_fields,
    )

    user_data: tweepy.User = user.data
    return user_data


def get_users(ids=None, usernames=None) -> list[tweepy.User]:
    if ids is not None and usernames is not None:
        raise TypeError("Expected IDs or usernames, not both")

    ids = ','.join(ids) if ids else None
    usernames = ','.join(usernames) if usernames else None

    users = retry_function_if_fail(
        client.get_users,
        ids=ids,
        usernames=usernames,
        user_fields=user_fields,
    )

    user_data: list[tweepy.User] = users.data
    return user_data


def save_liker_user_neo4j(users):
    print(len(users), "Users were saved!")


katerina_user_id = 2220997760

# Tweet, Quote Tweet, ReTweet, Replay


def extract_twitter_user_information(user_id=None, username=None):
    # steps to follow
    # ?get all tweets that user has mentioned in it
    # ?get all tweets of the user
    #
    # for each Tweet
    # 1. if "Tweet" or "Quote Tweet"
    #   -> get its all Replies
    #   -> get its Quotes
    #   -> get its ReTweets
    #   -> get its liker users
    # 2. if "ReTweet"
    #   -> we don't need to do anything
    # 3. if "Reply"
    #   -> get its all Replies
    #   -> get its Quotes
    #   -> get its ReTweets
    #   -> get its liker users
    #
    #
    # finally get all users's infos that we don't have

    if user_id is None and username is not None:
        user = get_user(username=username)
        user_id = user.id
        username = user.username
    elif user_id is not None and username is None:
        user = get_user(id=user_id)
        user_id = user.id
        username = user.username
    elif user_id is None and username is None:
        raise TypeError("Expected ID or username or both, not none of them")

    latest_mention_id = get_latest_mention(user_id=user_id)
    mentioned_tweets = get_mentioned_tweets_by_username(
        username=username, since_id=latest_mention_id
    )
    save_tweets_in_neo4j(mentioned_tweets)

    latest_tweet_id = get_latest_tweet(user_id=user_id)
    user_tweets = get_user_tweets(user_handler=user_id, since_id=latest_tweet_id)
    save_tweets_in_neo4j(user_tweets)

    for tweet in user_tweets:
        referenced_tweets = (
            list(
                map(
                    lambda referenced_tweets: referenced_tweets.type,
                    tweet.referenced_tweets,
                )
            )
            if tweet.referenced_tweets
            else None
        )

        if referenced_tweets and "retweeted" in referenced_tweets:
            pass
        elif referenced_tweets and "replied_to" in referenced_tweets:
            print("'Replied'")

            latest_reply_id = get_latest_reply(tweet_id=tweet.id)
            replies_of_reply = get_first_depth_replies_of_tweet(
                tweet_id=tweet.id, since_id=latest_reply_id
            )
            save_tweets_in_neo4j(replies_of_reply)

            latest_quote_id = get_latest_quote(tweet_id=tweet.id)
            quotes_of_reply = get_quotes_of_tweet(
                tweet_id=tweet.id, since_id=latest_quote_id
            )
            save_tweets_in_neo4j(quotes_of_reply)

            latest_retweet_id = get_latest_retweet(tweet_id=tweet.id)
            retweets_of_reply = get_retweets_of_tweet(
                tweet_id=tweet.id, since_id=latest_retweet_id
            )
            save_tweets_in_neo4j(retweets_of_reply)

        elif referenced_tweets is None or "quoted" in referenced_tweets:
            print("'Tweet' or 'Quote'")

            latest_reply_id = get_latest_reply(tweet_id=tweet.id)
            replies_of_reply = get_first_depth_replies_of_tweet(
                tweet_id=tweet.id, since_id=latest_reply_id
            )
            save_tweets_in_neo4j(replies_of_reply)

            latest_quote_id = get_latest_quote(tweet_id=tweet.id)
            quotes_of_reply = get_quotes_of_tweet(
                tweet_id=tweet.id, since_id=latest_quote_id
            )
            save_tweets_in_neo4j(quotes_of_reply)

            latest_retweet_id = get_latest_retweet(tweet_id=tweet.id)
            retweets_of_reply = get_retweets_of_tweet(
                tweet_id=tweet.id, since_id=latest_retweet_id
            )
            save_tweets_in_neo4j(retweets_of_reply)


# katerina_user_id = 2220997760
# extract_twitter_user_information(katerina_user_id)


def extract_user_information():
    users_id = get_incomplete_profile_ids()

    chunk_size = 100
    users_id_chunk = [
        users_id[i : i + chunk_size] for i in range(0, len(users_id), chunk_size)
    ]

    for users_id in users_id_chunk:
        users = get_users(ids=users_id)
        save_user_profile_neo4j(users)


def get_liker_users(user_id: str):
    tweet_ids = get_days_ago_tweet_ids(user_id= user_id)

    for tweet_id in tweet_ids:
        liker_users = get_likers_of_tweet(tweet_id=tweet_id)
        save_tweet_likes_neo4j(tweet_id, liker_users)
