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
    expected_relation = (
        """MERGE (a:Tweet {authorId:"123321"}) MERGE (b:Tweet {authorId:"345543"})"""
    )
    expected_relation += " MERGE (a)-[r:QUOTED]->(b)"
    expected_relation += " SET r.createdAt=1681740235000"
    assert expected_relation in query


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
    expected_query = (
        """MERGE (a:Tweet {authorId:"123321"}) MERGE (b:Tweet {authorId:"345543"})"""
    )
    expected_query += " MERGE (a)-[r:QUOTED]->(b)"
    expected_query += " SET r.createdAt=1681740235000"
    expected_query += """, r.createdAt2="sample" """
    expected_query = expected_query[:-1]

    assert expected_query == query
