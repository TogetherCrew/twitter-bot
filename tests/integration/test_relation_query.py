from datetime import datetime

from bot.db.utils.enums_data import EdgeLabels, NodeLabels, Properties, TweetProperties
from bot.db.utils.query_create_relation import relation_query


def test_relation_query_single_property():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at,
                datetime.strptime("2023-04-17 14:03:55+00:00", "%Y-%m-%d %H:%M:%S%z"),
                datetime,
            ),
        ],
    )

    print("query: ", query)

    assert (
        """MERGE (a:Tweet {authorId:"123321"}) MERGE (b:Tweet {authorId:"345543"})"""
        in query
    )
    assert """MERGE (a)-[:QUOTED {createdAt: 1681740235000}]->(b)""" in query


def test_relation_query_multiple_properties():
    query = relation_query(
        NodeLabels.tweet,
        NodeLabels.tweet,
        Properties(TweetProperties.author_id, "123321", str),
        Properties(TweetProperties.author_id, "345543", str),
        relation_name=EdgeLabels.quoted,
        relation_properties=[
            Properties(
                TweetProperties.created_at,
                datetime.strptime("2023-04-17 14:03:55+00:00", "%Y-%m-%d %H:%M:%S%z"),
                datetime,
            ),
            Properties("createdAt2", "sample", str),
        ],
    )

    print("query: ", query)

    assert (
        """MERGE (a:Tweet {authorId:"123321"}) MERGE (b:Tweet {authorId:"345543"})"""
        in query
    )
    assert (
        """MERGE (a)-[:QUOTED {createdAt: 1681740235000, createdAt2: "sample"}]->(b)"""
        in query
    )
