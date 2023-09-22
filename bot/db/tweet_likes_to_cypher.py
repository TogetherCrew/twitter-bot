from datetime import datetime, timezone

from tweepy import Tweet, User

from .utils.enums_data import (
    EdgeLabels,
    NodeLabels,
    Properties,
    TweetProperties,
    TwitterAccountProperties,
)
from .utils.query_create_relation import relation_query


def create_query_tweet_likes(tweet_id: str, users_liked: list[User]) -> list[str]:
    """
    create query to save the likes of a tweet

    Patameters:
    -----------
    tweet_id : str
        the tweet_id which the likes belong to
    users_liked : list[tweepy.User]
        the list of users liking a tweet

    Returns:
    ---------
    cypher_queries : list[str]
        a list of cypher queries to save the tweet likes data
    """
    cypher_queries = []

    for user in users_liked:
        query = relation_query(
            NodeLabels.twitter_account,
            NodeLabels.tweet,
            Properties(TwitterAccountProperties.user_id, user["id"], str),
            Properties(TweetProperties.tweet_id, tweet_id, str),
            relation_name=EdgeLabels.liked,
            relation_properties=[
                Properties(
                    TweetProperties.latest_saved_at,
                    datetime.now(tz=timezone.utc),
                    datetime,
                ),
            ],
        )
        cypher_queries.append(query)

    return cypher_queries


def create_query_user_likes(user_id: str, tweets_liked: list[Tweet]) -> list[str]:
    """
    create query to save the likes a user did on tweets

    Patameters:
    -----------
    user_id : str
        the user_id which did the like of tweets
    tweets_liked : list[tweepy.User]
        the list of tweets liked by the user

    Returns:
    ---------
    cypher_queries : list[str]
        a list of cypher queries to save the likes of the user
    """
    cypher_queries = []

    for tweet in tweets_liked:
        query = relation_query(
            NodeLabels.twitter_account,
            NodeLabels.tweet,
            Properties(TwitterAccountProperties.user_id, user_id, str),
            Properties(TweetProperties.tweet_id, tweet["id"], str),
            relation_name=EdgeLabels.liked,
            relation_properties=[
                Properties(
                    TweetProperties.latest_saved_at,
                    datetime.now(tz=timezone.utc),
                    datetime,
                ),
            ],
        )
        cypher_queries.append(query)

    return cypher_queries
