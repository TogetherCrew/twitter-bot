from bot.db.incomplete_profiles import get_incomplete_profile_ids
from bot.db.latest_mention import get_latest_mention
from bot.db.latest_quote import get_latest_quote
from bot.db.latest_reply import get_latest_reply
from bot.db.latest_retweet import get_latest_retweet
from bot.db.latest_tweet import get_days_ago_tweet_ids, get_latest_tweet
from bot.db.save_neo4j import (
    save_tweet_likes_neo4j,
    save_tweets_in_neo4j,
    save_user_likes_neo4j,
    save_user_profile_neo4j,
)
from bot.services.liked_tweet import get_liked_tweets, get_likers_of_tweet
from bot.services.quote_tweet import get_quotes_of_tweet
from bot.services.reply_tweet import (
    get_all_replies_of_tweet,
    get_first_depth_replies_of_tweet,
)
from bot.services.retweet_tweet import get_retweets_of_tweet
from bot.services.user_info import get_twitter_user, get_twitter_users
from bot.services.user_tweet import get_mentioned_tweets_by_username, get_user_tweets


def extract_and_save_tweets(
    user_id: str | int | None = None, username: str = None
) -> None:
    """
    steps to follow
    ?get all tweets that user has mentioned in it
    ?get all tweets of the user

    for each Tweet
    1. if "Tweet" or "Quote Tweet"
      -> get its all Replies
      -> get its Quotes
      -> get its ReTweets
      -> get its liker users
    2. if "ReTweet"
      -> we don't need to do anything
    3. if "Reply"
      -> get its all Replies
      -> get its Quotes
      -> get its ReTweets
      -> get its liker users

    finally get all users's infos that we don't have

    Parameters:
    -------------
    user_id : str | int
        the user account twitter id, can be both string or integer
    username : str
        the user account username

    *Note:* Either one of the `user_id` or the `username` should be given.
    If not given, a TypeError would be raised.
    """

    if user_id is None and username is not None:
        user = get_twitter_user(username=username)
        user_id = user.id
        username = user.username
    elif user_id is not None and username is None:
        user = get_twitter_user(id=user_id)
        user_id = user.id
        username = user.username
    elif user_id is None and username is None:
        raise TypeError("Expected ID or username or both, not none of them")

    latest_mention_id = get_latest_mention(user_id=str(user_id))
    mentioned_tweets = get_mentioned_tweets_by_username(
        username=username, since_id=latest_mention_id
    )
    save_tweets_in_neo4j(mentioned_tweets)

    latest_tweet_id = get_latest_tweet(user_id=str(user_id))
    user_tweets = get_user_tweets(user_handler=str(user_id), since_id=latest_tweet_id)
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
            replies_of_reply = get_all_replies_of_tweet(
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


def extract_and_save_user_information():
    users_id = get_incomplete_profile_ids()

    chunk_size = 100
    users_id_chunk = [
        users_id[i : i + chunk_size] for i in range(0, len(users_id), chunk_size)
    ]

    for users_id in users_id_chunk:
        users = get_twitter_users(ids=users_id)
        save_user_profile_neo4j(users)


def extract_and_save_liker_users(user_id: str):
    tweet_ids = get_days_ago_tweet_ids(user_id=user_id)

    for tweet_id in tweet_ids:
        liker_users = get_likers_of_tweet(tweet_id=tweet_id)
        save_tweet_likes_neo4j(tweet_id, liker_users)
        save_user_profile_neo4j(liker_users)


def extract_and_save_liked_tweets(user_id: str):
    liked_tweets = get_liked_tweets(user_id=user_id)
    save_user_likes_neo4j(user_id=user_id, tweets_liked=liked_tweets)
    save_tweets_in_neo4j(liked_tweets)
