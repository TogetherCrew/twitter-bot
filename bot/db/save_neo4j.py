from typing import Any

from numpy import unique
from tweepy import User, Tweet

from .neo4j_connection import Neo4jConnection
from .twitter_data_to_cypher import create_twitter_data_query
from .user_profile_to_cypher import create_twitter_user_profile_query
from .tweet_likes_to_cypher import create_query_tweet_likes, create_query_user_likes


def save_tweets_in_neo4j(
    twitter_data: list[dict[str, Any]], message: str | None = None
) -> None:
    """
    save tweets data into neo4j

    Parameters:
    ------------
    twitter_data : list[dict[str, Any]]
        list of tweet dictionary
    message : str | None
        optional: additional info on what kind of data is being saved
        default is None
    """
    # connect to neo4j
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    # create related queries
    queries = create_twitter_data_query(twitter_data)
    # store data into database
    msg = "saving tweets data into neo4j: "
    if message is not None:
        msg += f"{message}: "
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=msg)


def save_user_profile_neo4j(user_data: list[User], message: str | None = None) -> None:
    """
    save user profile data into neo4j

    Parameters:
    ------------
    twitter_data : list[dict[str, Any]]
        list of tweet dictionary
    message : str | None
        optional: additional info on what kind of data is being saved
        default is None
    """
    # connect to neo4j
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    # create related queries
    queries = create_twitter_user_profile_query(user_data)
    # store data into database
    msg = "saving users profile data: "
    if message is not None:
        msg += f"{message}: "
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=msg)


def save_tweet_likes_neo4j(
    tweet_id: str, users_liked: list[User], message: str | None = None
) -> None:
    """
    save the likes of a tweet within neo4j

    Patameters:
    -----------
    tweet_id : str
        the tweet_id which the logs belong to
    users_liked : list[tweepy.User]
        the list of users liking a tweet
    message : str | None
        optional: additional info on what kind of data is being saved
        default None
    """
    # connect to neo4j
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    # create related queries
    queries = create_query_tweet_likes(tweet_id, users_liked)
    # store data into database
    msg = "saving tweets like data: "
    if message is not None:
        msg += f"{message}: "
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=msg)


def save_user_likes_neo4j(
    user_id: str, tweets_liked: list[Tweet], message: str | None = None
) -> None:
    """
    save the likes a user did on tweets

    Parameters:
    ------------
    user_id : str
        the user_id which did the like of tweets
    tweets_liked : list[tweepy.User]
        the list of tweets liked by the user
    message : str | None
        optional: additional info on what kind of data is being saved
        default is None
    """
    # connect to neo4j
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    # create related queries
    queries = create_query_user_likes(user_id, tweets_liked)
    # store data into database
    msg = "saving users liked tweets data: "
    if message is not None:
        msg += f"{message}: "
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=msg)
