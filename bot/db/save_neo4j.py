from typing import Any

from numpy import unique
from .cypher_query_creator import create_twitter_data_query
from .neo4j_connection import connect_neo4j


def save_tweets_in_neo4j(twitter_data: list[dict[str, Any]], message: str = "") -> None:
    """
    save tweets data into neo4j

    Parameters:
    ------------
    twitter_data : list[dict[str, Any]]
        list of tweet dictionary
    message : str
        optional: additional info on what kind of data is being saved
        default is empty
    """
    # connect to neo4j
    neo4j_ops = connect_neo4j()
    # create related queries
    queries = create_twitter_data_query(twitter_data)
    # store data into database
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=message)
