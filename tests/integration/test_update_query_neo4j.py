from neo4j_connection import connect_neo4j
from query_creator.enums_data import NodeLabels, Properties, TweetProperties
from query_creator.utils import update_query


def test_update_query_single_add_properties_neo4j():
    query = update_query(
        NodeLabels.tweet,
        match_properties=Properties(TweetProperties.author_id, "123321", str),
        add_properties=[Properties(TweetProperties.text, "Happy Day!", str)],
    )

    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(
        [query], message="test_update_query_single_add_properties_neo4j"
    )

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (t:Tweet)
        RETURN t{.*} as tweet
        """
    )

    assert len(results) == 1
    data = results["tweet"].values[0]
    assert data["authorId"] == "123321"
    assert data["text"] == "Happy Day!"


def test_update_query_multiple_add_properties_neo4j():
    query = update_query(
        NodeLabels.tweet,
        match_properties=Properties(TweetProperties.author_id, "123321", str),
        add_properties=[
            Properties(TweetProperties.text, "Happy Day!", str),
            Properties(TweetProperties.like_counts, 5, int),
        ],
    )

    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(
        [query], message="test_update_query_multiple_add_properties_neo4j"
    )
    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (t:Tweet)
        RETURN t{.*} as tweet
        """
    )
    assert len(results) == 1
    data = results["tweet"].values[0]
    assert data["authorId"] == "123321"
    assert data["likeCounts"] == 5
