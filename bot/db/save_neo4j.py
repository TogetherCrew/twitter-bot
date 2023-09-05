from typing import Any

from numpy import unique
from .twitter_data_to_cypher import create_twitter_data_query
from .neo4j_connection import Neo4jConnection


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
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    # create related queries
    queries = create_twitter_data_query(twitter_data)
    # store data into database
    neo4j_ops.store_data_neo4j(query_list=unique(queries), message=message)
