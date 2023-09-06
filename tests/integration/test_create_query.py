from datetime import datetime

from bot.db.utils.enums_data import NodeLabels, Properties, TwitterAccountProperties
from bot.db.utils.query_create_entity import create_query


def test_create_query_single_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_name, "sepehr", str),
        properties=[],
    )

    print(query)
    assert query == """MERGE (a:TwitterAccount {userName: "sepehr"}) """


def test_create_query_double_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_name, "sepehr", str),
        properties=[
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
        ],
    )

    print(query)

    expected_query = """MERGE (a:TwitterAccount {userName: "sepehr"})"""
    expected_query += """ SET a.bio="My Age is 22 :)" """
    expected_query = expected_query[:-1]
    assert query == expected_query


def test_create_query_multiple_property():
    query = create_query(
        node_label=NodeLabels.twitter_account,
        merge_property=Properties(TwitterAccountProperties.user_id, "123456", str),
        properties=[
            Properties(TwitterAccountProperties.user_name, "sepehr", str),
            Properties(TwitterAccountProperties.bio, "My Age is 22 :)", str),
            Properties(
                TwitterAccountProperties.created_at,
                datetime.strptime(
                    "2023-04-17 14:03:55+00:00", 
                    "%Y-%m-%d %H:%M:%S%z"
                ),
                datetime,
            ),
        ],
    )

    print(query)
    expected_query = """MERGE (a:TwitterAccount {userId: "123456"}) """
    expected_query += """SET a.userName="sepehr", """
    expected_query += """a.bio="My Age is 22 :)", a.createdAt=1681740235000"""

    assert query == expected_query
