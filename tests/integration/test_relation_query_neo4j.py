from datetime import datetime

from query_creator.enums_data import EdgeLabels, NodeLabels, Properties, TweetProperties
from query_creator.utils import relation_query
from neo4j_connection import connect_neo4j


def test_relation_query_single_property_no_previous_data():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at, "2023-04-17 14:03:55+00:00", datetime
            )
        ],
    )
    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j(
        [query], message="test_relation_query_single_property_no_previous_data"
    )

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH ()-[r:QUOTED]->()
        RETURN
        r{.*} as quote
        """
    )
    assert len(results) == 1
    data = results["quote"].values[0]
    assert data["createdAt"] == 1681740235000


def test_relation_query_single_property_with_previous_data():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at, "2023-04-17 14:03:55+00:00", datetime
            )
        ],
    )
    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    queries = [
        "CREATE (:Tweet {authorId:'123321'})",
        "CREATE (:Tweet {authorId:'345543'})",
        query,
    ]
    neo4j_ops.store_data_neo4j(
        queries, message="test_relation_query_single_property_with_previous_data"
    )

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH ()-[r:QUOTED]->()
        RETURN
        r{.*} as quote
        """
    )
    assert len(results) == 1
    data = results["quote"].values[0]
    assert data["createdAt"] == 1681740235000


def test_relation_query_multiple_properties_no_past_data():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at, "2023-04-17 14:03:55+00:00", datetime
            ),
            Properties("createdAt2", "sample", str),
        ],
    )

    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    neo4j_ops.store_data_neo4j(
        [query], message="test_relation_query_multiple_properties_no_past_data"
    )

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH ()-[r:QUOTED]->()
        RETURN
        r{.*} as quote
        """
    )
    assert len(results) == 1
    data = results["quote"].values[0]
    assert data["createdAt"] == 1681740235000
    assert data["createdAt2"] == "sample"


def test_relation_query_multiple_properties_with_past_data():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at, "2023-04-17 14:03:55+00:00", datetime
            ),
            Properties("createdAt2", "sample", str),
        ],
    )

    neo4j_ops = connect_neo4j()
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    queries = [
        "CREATE (:Tweet {authorId:'123321'})",
        "CREATE (:Tweet {authorId:'345543'})",
        query,
    ]
    neo4j_ops.store_data_neo4j(
        queries, message="test_relation_query_multiple_properties_with_past_data"
    )

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH ()-[r:QUOTED]->()
        RETURN
        r{.*} as quote
        """
    )
    assert len(results) == 1
    data = results["quote"].values[0]
    assert data["createdAt"] == 1681740235000
    assert data["createdAt2"] == "sample"
