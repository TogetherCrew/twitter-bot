from datetime import datetime

from bot.db.neo4j_connection import Neo4jConnection
from bot.db.utils.enums_data import NodeLabels, Properties, TwitterAccountProperties
from bot.db.utils.query_create_entity import create_query


def test_create_query_single_property_neo4j():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_name, "sepehr", str),
        properties=[],
    )

    print(query)
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops

    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )

    neo4j_ops.store_data_neo4j([query], message="test_create_query_single_property")

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN
        a{.*} as user
        """
    )
    data = results["user"].values[0]
    assert data["userName"] == "sepehr"


def test_create_query_double_property_neo4j():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_name, "sepehr", str),
        properties=[
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
        ],
    )

    print(query)
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j([query], message="test_create_query_double_property")

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN
        a{.*} as user
        """
    )
    data = results["user"].values[0]
    assert data["userName"] == "sepehr"
    assert data["bio"] == "My Age is 22 :)"


def test_create_query_multiple_property_neo4j():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_id, "123456", str),
        properties=[
            Properties(TwitterAccountProperties.user_name, "sepehr", str),
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
            Properties(
                TwitterAccountProperties.created_at,
                datetime.strptime("2023-04-17 14:03:55+00:00", "%Y-%m-%d %H:%M:%S%z"),
                datetime,
            ),
        ],
    )

    print(query)
    neo4j_connection = Neo4jConnection()
    neo4j_ops = neo4j_connection.neo4j_ops
    neo4j_ops.gds.run_cypher(
        """
        MATCH (n) DETACH DELETE (n)
        """
    )
    neo4j_ops.store_data_neo4j([query], message="test_create_query_multiple_property")

    results = neo4j_ops.gds.run_cypher(
        """
        MATCH (a:TwitterAccount)
        RETURN
        a{.*} as user
        """
    )
    data = results["user"].values[0]
    assert data["userName"] == "sepehr"
    assert data["userId"] == "123456"
    assert data["bio"] == "My Age is 22 :)"
    assert data["createdAt"] == 1681740235000
